# 新潟バドミントン自動予約システム

新潟市スポーツ施設のバドミントンコートを自動で予約するPythonプログラムです。

## 主な機能

- 希望日（本日から5日後）・時間帯のバドミントンコートを自動予約
- 空きコートを自動検索し、複数コート同時予約（COURT_NO指定）
- FACILITY_NAME, FACILITY_IDはキーワード（例：HIGASHI, KITA等）で自動変換
- CSRFトークン自動処理・予約成功ログ出力
- 高速な予約処理（1～2秒以内）

## インストール方法

### 1. Pythonのインストール
Python 3.7以上が必要です。

### 2. 必要なライブラリのインストール (仮想環境推奨)
プロジェクトごとの依存分離のため、`venv` 仮想環境を作成してその中にライブラリをインストールすることを推奨します。

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

補足: システム全体の Python に直接インストールする代わりに仮想環境を使用してください。`start_booking.sh` と `start_booking.bat` はデフォルトで `./venv` 内の Python を使用し、必要であれば環境変数 `VENV_PYTHON` でパスを指定できます。

## 全体の環境構築

まずは環境を整えてください。

1) リポジトリのクローンと移動

```bash
git clone <repo-url> /path/to/autoBooking
cd /path/to/autoBooking
```

2) Python 仮想環境と依存関係のインストール

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3) 設定ファイルの作成（ブラウザ使用）

1) プロジェクトルートにある `USEME.html` をウェブブラウザで開きます（ファイルをダブルクリックするか、ブラウザの「ファイルを開く」から）。

2) フォームに必要事項を入力して「設定保存」ボタンを押すと、ブラウザのダウンロードフォルダ（例: `~/Downloads`）に `my_data.json` が生成されます。

3) 生成された `my_data.json` をプロジェクトフォルダに移動してください。例:

```bash
# macOS / Linux の例（環境に合わせてパスを修正してください）
mv ~/Downloads/my_data.json /path/to/autoBooking/my_data.json
# またはコピー
cp ~/Downloads/my_data.json /path/to/autoBooking/my_data.json
```

注: `USEME.html` を使えばサンプルからのコピー作業は不要です。

4) ログディレクトリの確認

```bash
mkdir -p logs
```

## start_booking の実行と予約方法

`start_booking.sh` は予約プロセスを起動するスクリプトです。通常 cron から実行します。内部で07:00まで待機するため、少し早めに起動する設定にするのが安全です。

1) 実行権限付与＆手動テスト

```bash
chmod +x start_booking.sh
sh start_booking.sh
```

2) crontab に登録（例：毎週土曜 06:59 実行）

```bash
crontab -e

# 毎週土曜 06:59 に実行
# 注意: `main.py` が `logs/reservation.log` を自動的に作成・出力します。
# そのため crontab での追加ログリダイレクトは基本的に不要です。
59 6 * * 6 cd /Users/<your-username>/Desktop/autoBooking && sh start_booking.sh
```

3) crontab 登録の確認

```bash
crontab -l
```

注意：
- cron では絶対パスと必要な環境変数（PATH、仮想環境のアクティベートなど）を明示してください。仮想環境を使う場合は `cd` 後に `source venv/bin/activate` を追加するか、スクリプト内でアクティベートすることを推奨します。
- スクリプトを7時00分前に実行すると `main.py`の内部待機ロジックが正確に7時00分に予約プロセスを始まります。

### `start_booking.sh` の変更点と cron 設定の推奨

- スクリプトは 2025-12-14 に cron で動作しやすいよう更新されました:
	- `HOME` をハードコードせず動的に設定します（`export HOME="${HOME:-/Users/$(id -un)}"`）。
	- `PATH` を設定して cron 環境でも `command -v` が動作するようにしています。
	- stdout/stderr を `logs/cron.log` にリダイレクトするようになり、cron 実行時の出力は `logs/cron.log` で確認できます。
	- `VENV_PYTHON` のデフォルトは `./venv/bin/python3` です。仮想環境を利用している場合は各自 `VENV_PYTHON` を指定することを推奨します。

- 問題のサインと対処
	- ログに `[WARN] Python executable not found at ''` が出る場合、`VENV_PYTHON` が空で仮想環境の Python を見つけられていません。スクリプト上部の設定例を編集してパスを指定してください。
	- スクリプトに実行権限があるか確認してください: `chmod +x start_booking.sh`

## nightly_update の実行と登録方法

自動更新用の `nightly_update.sh` は定期実行（例：毎日 01:00）を想定しています。

1) 実行権限付与＆手動テスト

```bash
chmod +x nightly_update.sh
sh nightly_update.sh
```

2) crontab 例（毎日 01:00 実行）

```bash
crontab -e

# 毎日 01:00 に実行: ディレクトリ移動後にスクリプトを実行
# `nightly_update.sh` の標準出力をファイルに残したい場合はリダイレクトできますが、
# 予約関連ログは `main.py` が担当しているため通常は不要です。
0 1 * * * cd /Users/<your-username>/Desktop/autoBooking && sh nightly_update.sh
```

3) 登録確認

```bash
crontab -l
```

---

### 実行結果の確認

出力はコンソールおよび `logs/reservation.log` / `logs/nightly_update.log` を参照してください。問題が発生した場合はログの内容を確認して対処してください。

## プログラム構成

```
├── main.py                    # メイン実行ファイル
├── modules/
│   ├── get_date_id.py            # 日付ID取得モジュール
│   ├── get_reservation_ids.py    # 空きコート取得モジュール
│   └── niigata_macro.py          # 予約実行モジュール
├── USEME.html                    # ブラウザで my_data.json を生成するフォーム
├── start_booking.sh              # 予約実行スクリプト (cron 用)
├── nightly_update.sh             # 自動アップデートスクリプト (cron または 手動実行)
├── requirements.txt              # 必要ライブラリ一覧
├── README.md                     # 日本語説明書
└── reservation.log               # 実行ログ（自動生成）
```

## 動作概要

1. **日付ID取得**：予約希望日（本日+5日）のIDをWebサイトから取得
2. **コート検索**：該当日・時間帯の空きコートを検索
3. **CSRFトークン取得**：予約ページからセキュリティトークン取得
4. **予約確認・実行**：予約情報を送信し予約完了

## 予約可能時間帯

- 9-11時
- 11-13時
- 13-15時
- 15-17時
- 17-19時
- 19-21時

## 注意事項

⚠️ **重要な制限事項**

1. **Rate Limit**：Webサイトは1分あたり約5回までリクエスト可能。過度な実行は429エラーとなります。
2. **予約可能期間**：Webサイトの予約可能期間に従ってください。
3. **重複予約防止**：既に予約済みのコートは自動予約されません。
4. **コート選択**：複数空きがある場合、COURT_NO分だけ順に予約します。

## トラブルシューティング

### 空きコートがない場合
- その時間帯の全コートが既に予約済みです。
- 他の時間帯や日付をお試しください。

### 429エラーが出る場合
- リクエスト過多です。
- 30秒～1分待ってから再実行してください。

### CSRFトークンエラー
- Webサイトのセッションが切れた場合です。
- プログラムを再実行すれば自動で解決します。

### ValueError: too many values to unpack
- `get_reservation_ids.py`が古い場合に発生します。
- 最新版に差し替えてください。

## ログ確認

`reservation.log`ファイルで以下を確認できます：
- 日付ID取得結果
- 空きコート一覧
- 選択コート情報
- CSRFトークン取得状況
- 予約リクエスト応答コード
- 予約成功/失敗
- 総所要時間

**ログ例：**
```
2025-10-12 01:42:02,844 - INFO - 空きコート: ['バドミントン 1 (ID: 250514)', 'バドミントン 2 (ID: 250521)']
2025-10-12 01:42:02,844 - INFO - 選択コート: バドミントン 1 (ID: 250514)
2025-10-12 01:42:02,844 - INFO - 予約完了 - コート: バドミントン 1
2025-10-12 01:42:02,845 - INFO - === 予約が正常に完了しました! ===
2025-10-12 01:42:02,845 - INFO - 予約済みコート: バドミントン 1
2025-10-12 01:42:02,845 - INFO - 総所要時間: 1.56秒
```

## 成功例

```
[成功] 予約が正常に完了しました!
予約コート: バドミントン 1
所要時間: 1.56秒
```

## 📌 バージョン履歴

| 日付 | バージョン | 変更内容 |
|---|---:|---|
| 2025-04-09 | 1.0.0 | 初回リリース (Selenium ベース) |
| 2025-04-13 | 1.0.1 | Selenium ベースの速度改善 |
| 2025-04-14 | 2.0.0 | Playwright 版導入と速度改善 |
| 2025-04-19 | 2.0.1 | コート/時間指定機能追加、マジックナンバーを変数化 |
| 2025-04-23 | 2.1.1 | 体育館指定機能追加(カメダ)、予約失敗時の応答速度向上 |
| 2025-05-10 | 2.2.0 | 体育館オプション追加(トヤノ) |
| 2025-06-02 | 2.2.1 | エラー対応、安定性向上 |
| 2025-06-28 | 3.0.0 | 複数コート対応(最大3コート)、速度改善 |
| 2025-07-26 | 3.1.0 | 体育館オプション追加(西、北)、日付バグ修正 |
| 2025-07-27 | 3.2.0 | nightly update 機能追加 |
| 2025-10-12 | 4.0.0 | api ベースの速度改善 |
| 2025-10-12 | 4.1.0 | 自動化ツール提供(start_booking, nightly_update) |
| 2025-10-18 | 4.2.0 | 予約の安全性強化・月末時点での月初予約対応 |
| 2025-11-09 | 4.3.0 | jsonファイル生成のブラウザ提供 |
| 2025-12-07 | 4.4.0 | 3コート同時予約対応（テスト用） |
| 2025-12-14 | 4.5.0 | start_booking.sh アップデート - 動的なディレクトリとレイシング |

## ✅ ライセンスおよび製作者

- Maintained by [kurooru]
- License: kurooru

## 📔 開発日誌

[開発日誌 (Notion)](https://www.notion.so/NEMMY-DARRY-MENDY-208b163aeba780e09715c8992b99829a?source=copy_link)