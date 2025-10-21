# POS・予約システム連携サマリー

## 共通キー
- `store_id` / `store_code` / `location_code`: 店舗マスタ上の共通キー。Maple POS と Ocean Booking はコード体系が一致、Sunflower POS と Aurora Reservation はUUID形式の `store_id` を採用しているため、店舗マスタにて両者を突合するクロスリファレンステーブルが必須。
- 取引/予約日時: POS側の `business_date` / `trade_timestamp` と予約側の `reservation_date` / `service_start` が来店実績との突合候補。
- 顧客識別子: `loyalty_id`, `customer_id`, `customer_phone`, `guest_token` などが顧客単位分析のキー候補。電話番号は両予約システムで共通利用可能。

## システム差異の概要
- **金額構成**: Sunflower POS は税込・値引後金額を別カラムで保持、Maple POS は税込と税額を分離。統一した売上金額の算出ロジックが必要。
- **タイムゾーン**: POSは店舗ローカル、AuroraはJST固定、OceanはUTC。分析基盤で統一タイムゾーンに変換する標準処理を定義する。
- **顧客情報粒度**: Sunflower POS の `loyalty_id` と Auroraの `customer_id` は会員前提、Oceanは匿名トークンを許容。顧客統合には外部CRMからの補完が前提。

## データ更新頻度の比較
| システム | インクリメンタル頻度 | フルリフレッシュ |
| --- | --- | --- |
| Sunflower POS | 5分毎 | 過去日オプションあり | 
| Maple POS | 10分毎 | 日次クローズ後 | 
| Aurora Reservation | 15分毎 | 日次フル（S3） |
| Ocean Booking | 30分毎 | なし（180日保持） |

## 推奨連携方針
1. 店舗マスタに `store_id_uuid` と `store_code` のクロスウォークを保持し、すべてのデータ取込時に付与。
2. タイムゾーン統一を行うETLレイヤーで `business_timestamp_utc` を算出し、予約→来店→売上の時間照合を実現。
3. 顧客キーは電話番号を第一候補とし、会員ID・ゲストトークンは補助キーとしてハッシュ化して保持。
