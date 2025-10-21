# Maple POS データ仕様テンプレート

## 概要
- **システム名**: Maple POS
- **対象範囲**: 精算ジャーナル・商品明細
- **主テーブル**: `maple_sales_journal`

## フィールド定義
| フィールド名 | 説明 | データ型 | NULL可否 | 更新頻度 | 備考 |
| --- | --- | --- | --- | --- | --- |
| receipt_no | レシート番号 | STRING | NOT NULL | 10分毎インクリメンタル | 数字＋枝番 |
| store_code | 店舗コード | STRING | NOT NULL | 10分毎インクリメンタル | 自社マスタキーと一致 |
| pos_lane | POSレーン番号 | INTEGER | NOT NULL | 10分毎インクリメンタル | |
| trade_date | 取引日 | DATE | NOT NULL | 10分毎インクリメンタル | |
| trade_timestamp | 取引日時 | TIMESTAMP | NOT NULL | 10分毎インクリメンタル | |
| sku | SKUコード | STRING | NOT NULL | 10分毎インクリメンタル | |
| sku_name | SKU名称 | STRING | NOT NULL | 10分毎インクリメンタル | |
| department | 部門コード | STRING | NOT NULL | 1日1回フル | 商品マスタ連携 |
| quantity | 数量 | DECIMAL(9,2) | NOT NULL | 10分毎インクリメンタル | 計量対応 |
| gross_sales | 税込売上 | DECIMAL(12,2) | NOT NULL | 10分毎インクリメンタル | |
| tax_amount | 税額 | DECIMAL(12,2) | NOT NULL | 10分毎インクリメンタル | |
| discount_code | 値引コード | STRING | NULLABLE | 10分毎インクリメンタル | 値引未適用時はNULL |
| discount_value | 値引額 | DECIMAL(12,2) | NULLABLE | 10分毎インクリメンタル | |
| tender_type | 受領決済種別 | STRING | NOT NULL | 10分毎インクリメンタル | |
| customer_reference | 顧客参照番号 | STRING | NULLABLE | 10分毎インクリメンタル | 外部CRM連携時のみ |
| last_synced_at | 連携更新日時 | TIMESTAMP | NOT NULL | 10分毎インクリメンタル | |

## 共通キーと差異
- **共通キー候補**: `store_code` は他システムの `store_id` と相互参照可能。`receipt_no` + `trade_date` で取引一意。
- **差異**:
  - 金額項目は税込・税額が分離しており、純売上算出には計算が必要。
  - `quantity` は小数対応のため、整数のみを扱うシステムとは型が異なる。
  - 割引関連は `discount_code`/`discount_value` の2カラム構成。

## 備考
- POS閉店処理完了時に当日分のフルスナップショットを翌日3時に提供可能。
- 返品トランザクションは負の数量・金額で表現。
