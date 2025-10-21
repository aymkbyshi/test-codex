# Ocean Booking データ仕様テンプレート

## 概要
- **システム名**: Ocean Booking
- **対象範囲**: 予約・来店管理（オンライン・ウォークイン）
- **主テーブル**: `ocean_booking_records`

## フィールド定義
| フィールド名 | 説明 | データ型 | NULL可否 | 更新頻度 | 備考 |
| --- | --- | --- | --- | --- | --- |
| booking_no | 予約番号 | STRING | NOT NULL | 30分毎インクリメンタル | 予約サイト連番 |
| location_code | ロケーションコード | STRING | NOT NULL | 30分毎インクリメンタル | POS店舗コードと1:1 |
| service_date | 利用日 | DATE | NOT NULL | 30分毎インクリメンタル | |
| service_start | 開始時刻 | TIMESTAMP | NOT NULL | 30分毎インクリメンタル | タイムゾーンUTC |
| pax | 来店人数 | INTEGER | NOT NULL | 30分毎インクリメンタル | |
| area | 席エリア | STRING | NULLABLE | 30分毎インクリメンタル | |
| booking_source | 予約ソース | STRING | NOT NULL | 30分毎インクリメンタル | API/Web/Walk-in |
| lead_time_minutes | 予約リードタイム | INTEGER | NOT NULL | 30分毎インクリメンタル | 作成時刻との差分 |
| guest_token | ゲストトークン | STRING | NULLABLE | 30分毎インクリメンタル | 匿名来店時NULL |
| guest_name | 氏名 | STRING | NOT NULL | 30分毎インクリメンタル | |
| guest_contact | 連絡先 | STRING | NOT NULL | 30分毎インクリメンタル | 電話またはメール |
| status | ステータス | STRING | NOT NULL | 30分毎インクリメンタル | Booked/Seated/No-show 等 |
| seated_at | 着席時刻 | TIMESTAMP | NULLABLE | 30分毎インクリメンタル | 当日更新 |
| no_show_flag | ノーショーフラグ | BOOLEAN | NOT NULL | 30分毎インクリメンタル | true/false |
| created_at | 作成日時 | TIMESTAMP | NOT NULL | 30分毎インクリメンタル | |
| modified_at | 更新日時 | TIMESTAMP | NOT NULL | 30分毎インクリメンタル | |

## 共通キーと差異
- **共通キー候補**: `location_code` はPOSの `store_code` とマッピング可能。`service_date` + `service_start` で来店スロットを特定。
- **差異**:
  - タイムスタンプはUTCで提供されるため、他システムと比較する際に変換が必要。
  - `no_show_flag` が明示的に提供され、Auroraには存在しない。
  - 匿名客は `guest_token` のみで識別し、個人情報が欠落するケースあり。

## 備考
- 過去180日のみ保持。拡張保管は追加契約が必要。
- フィールド追加は四半期ごとにリリースノートで通知。
