# 📅 自動予約マクロシステム (autoBooking) JAPANESE(🇯🇵)

ウェブサイト上での予約を自動で実行する、Pythonベースの自動化スクリプトです。  
Playwrightを使用してブラウザを操作し、`.env`ファイルで個人情報を管理します。  
cronやタスクスケジューラでの定期実行にも対応しています。

---

## 📦 セットアップ手順

### ✅ クローン先のパスにご注意

> ❌ 日本語やクラウドフォルダ（例：`OneDrive`, `iCloud`, `ドキュメント`）では失敗する可能性があります  
> ✅ 英語名のローカルパスを推奨（例：`C:\Projects`, `~/Projects`）

```bash
git clone https://github.com/Yang-Min-Seok/autoBooking
cd autoBooking
```

---

### 仮想環境の作成と起動

#### macOS / Linux / Git Bash

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

---

### パッケージのインストール

```bash
pip install -r requirements.txt
playwright install
```

---

### 環境変数ファイルの設定

```bash
cp info.env.example info.env        # macOS / Linux
copy info.env.example info.env      # Windows
```

`info.env`ファイルを開いて、以下の情報を入力してください：

```env
TARGET_URL=https://example.com/reservation
NAME=山田太郎
PHONE_NUMBER=09012345678
E_MAIL=test@example.com
```

---

## 🧪 実行前のテスト

> Playwrightが正常に動作するか確認します。

```bash
python3 auto_booking.py
```

---

## 🚀 自動予約の実行

### macOS / Linux / Git Bash

```bash
chmod +x start_booking.sh
./start_playwright.sh
```

### Windows

```cmd
start_playwright.bat
```

---

## 🕑 定期実行の設定

### macOS（cronを使用）

```bash
crontab -e
```

```cron
0 7 * * 6 /Users/yourname/autoBooking/run_playwright.sh >> /Users/yourname/autoBooking/cron.log 2>&1
```

### Windows（タスクスケジューラを使用）

1. **タスクスケジューラ** を開く  
2. **基本タスクの作成** をクリック  
3. **トリガー**：毎週土曜日 午前7時 に設定  
4. **操作**：`run_playwright.bat` のパスを指定（例：`C:\\Users\\ユーザー名\\autoBooking\\run_playwright.bat`）  
5. 完了後、スクリプトが毎週自動的に実行されます  

以下の行を追加（毎週土曜 午前7時実行）：

1. **タスクスケジューラ** を開く  
2. **基本タスクの作成** をクリック  
3. **トリガー**：毎週土曜日 午前7時 に設定  
4. **操作**：`run_playwright.bat` のパスを指定（例：`C:\\Users\\ユーザー名\\autoBooking\\run_playwright.bat`）  
5. 完了後、スクリプトが毎週自動的に実行されます  

---

## 📁 ディレクトリ構成

```
autoBooking/
├── auto_booking_playwright.py     # 自動予約のメインスクリプト
├── run_playwright.sh              # macOS/Linux用スクリプト
├── run_playwright.bat             # Windows用スクリプト
│
├── steps/                         # 各STEPをモジュール化
│   ├── access_page.py             # STEP 1 - ページアクセス
│   ├── select_date.py             # STEP 2 - 日付選択と○予約クリック
│   ├── select_time.py             # STEP 3 - 時間スロット選択（9–11時）
│   ├── fill_form.py               # STEP 4 - 名前・電話番号・メール入力
│   └── confirm_final.py           # STEP 5 - 最終確認ボタンクリック
│
├── info.env.example               # 環境変数テンプレート
├── requirements.txt               # パッケージリスト
├── .gitignore                     # 除外設定
└── README_JP.md                   # 日本語のマニュアル
```

---

## 📌 バージョン履歴

| 日付        | バージョン | 変更内容                                  |
|-------------|------------|-------------------------------------------|
| 2025-04-09  | 1.0.0      | 初回リリース（Seleniumベース）              |
| 2025-04-13  | 1.0.1      | Seleniumに基づいた速度改善               |
| 2025-04-14  | 2.0.0      | Playwright導入及び、速度改善 |

---

## ✅ ライセンスと作者

- Maintained by [kurooru]  
- License: MIT または希望するライセンスに変更可能