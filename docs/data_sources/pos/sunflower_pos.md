# Sunflower POS データ仕様テンプレート

## 概要
- **システム名**: Sunflower POS
- **対象範囲**: 売上トランザクション明細
- **主テーブル**: `sunflower_pos_transactions`

## フィールド定義
| フィールド名 | 説明 | データ型 | NULL可否 | 更新頻度 | 備考 |
| --- | --- | --- | --- | --- | --- |
| transaction_id | 取引一意キー | STRING | NOT NULL | 5分毎インクリメンタル | UUID形式 |
| store_id | 店舗識別子 | STRING | NOT NULL | 5分毎インクリメンタル | 自社マスタと連携 |
| terminal_id | 端末識別子 | STRING | NOT NULL | 5分毎インクリメンタル | |
| business_date | 営業日 | DATE | NOT NULL | 5分毎インクリメンタル | 店舗ローカルタイム基準 |
| check_open_time | 取引開始時刻 | TIMESTAMP | NOT NULL | 5分毎インクリメンタル | |
| check_close_time | 取引終了時刻 | TIMESTAMP | NULLABLE | 5分毎インクリメンタル | オープン中はNULL |
| item_id | 商品識別子 | STRING | NOT NULL | 5分毎インクリメンタル | |
| item_name | 商品名 | STRING | NOT NULL | 5分毎インクリメンタル | 多言語対応 |
| category_code | カテゴリコード | STRING | NULLABLE | 1日1回フル | 商品マスタ同期 |
| quantity | 数量 | INTEGER | NOT NULL | 5分毎インクリメンタル | |
| gross_amount | 税込金額 | DECIMAL(10,2) | NOT NULL | 5分毎インクリメンタル | 円建て |
| discount_amount | 割引額 | DECIMAL(10,2) | NOT NULL | 5分毎インクリメンタル | 負値可 |
| net_amount | 実績金額 | DECIMAL(10,2) | NOT NULL | 5分毎インクリメンタル | gross-discount |
| payment_method | 決済種別 | STRING | NOT NULL | 5分毎インクリメンタル | 複数決済は分割行 |
| loyalty_id | 会員ID | STRING | NULLABLE | 5分毎インクリメンタル | 未登録客はNULL |
| updated_at | レコード更新日時 | TIMESTAMP | NOT NULL | 5分毎インクリメンタル | CDC基準 |

## 共通キーと差異
- **共通キー候補**: `transaction_id`, `store_id`, `business_date` は他POS・予約システムとの照合に使用。
- **差異**:
  - `loyalty_id` フィールドはSunflower POS固有で、会員連携を行わないシステムでは欠落。
  - 決済情報は `payment_method` の単一カラムで管理しており、明細レベルの決済分割は外部テーブル無しで表現。

## 備考
- タイムゾーンは全て店舗ローカルタイムで提供。分析基盤取り込み時にUTCへ変換が必要。
- 過去データ再取得は日次単位でリクエスト可能。
