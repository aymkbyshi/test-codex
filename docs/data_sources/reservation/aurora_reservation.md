# Aurora Reservation データ仕様テンプレート

## 概要
- **システム名**: Aurora Reservation
- **対象範囲**: 店舗予約情報（確定・仮押さえ・キャンセル）
- **主テーブル**: `aurora_reservations`

## フィールド定義
| フィールド名 | 説明 | データ型 | NULL可否 | 更新頻度 | 備考 |
| --- | --- | --- | --- | --- | --- |
| reservation_id | 予約一意キー | STRING | NOT NULL | 15分毎インクリメンタル | UUID形式 |
| store_id | 店舗識別子 | STRING | NOT NULL | 15分毎インクリメンタル | POSと共通マスタ |
| reservation_date | 予約日 | DATE | NOT NULL | 15分毎インクリメンタル | |
| reservation_time | 予約開始時刻 | TIME | NOT NULL | 15分毎インクリメンタル | 24時間表記 |
| party_size | 人数 | INTEGER | NOT NULL | 15分毎インクリメンタル | |
| duration_minutes | 滞在予定分数 | INTEGER | NULLABLE | 15分毎インクリメンタル | 未設定時NULL |
| booking_channel | 予約経路 | STRING | NOT NULL | 15分毎インクリメンタル | Web/Phone/Partner等 |
| customer_id | 顧客ID | STRING | NULLABLE | 15分毎インクリメンタル | 会員登録時のみ |
| customer_name | 予約者氏名 | STRING | NOT NULL | 15分毎インクリメンタル | |
| customer_phone | 電話番号 | STRING | NOT NULL | 15分毎インクリメンタル | 国番号含む |
| customer_email | メール | STRING | NULLABLE | 15分毎インクリメンタル | 未入力可 |
| status | ステータス | STRING | NOT NULL | 15分毎インクリメンタル | Confirmed/Hold/Cancelled |
| cancellation_reason | キャンセル理由 | STRING | NULLABLE | 15分毎インクリメンタル | status=Cancelled時のみ |
| notes | 特記事項 | STRING | NULLABLE | 15分毎インクリメンタル | アレルギー等 |
| created_at | 予約作成日時 | TIMESTAMP | NOT NULL | 15分毎インクリメンタル | |
| updated_at | 最終更新日時 | TIMESTAMP | NOT NULL | 15分毎インクリメンタル | |

## 共通キーと差異
- **共通キー候補**: `store_id`, `reservation_date` はPOS売上との突合で利用可能。`customer_phone` はCRMとの共通キー候補。
- **差異**:
  - `duration_minutes` など滞在予定情報はAurora固有。
  - キャンセル理由は `cancellation_reason` に文字列で格納され、コードマスタは別途提供なし。

## 備考
- 過去2年分の履歴を保持。日次フルエクスポートはS3経由で提供。
- タイムゾーンは全てJST固定。
