# 📅 自動予約マクロシステム (autoBooking) JAPANESE(🇯🇵)

ウェブサイト上での予約を自動で実行する、Pythonベースの自動化スクリプトです。  
Seleniumを使ってブラウザを操作し、`.env`ファイルで個人情報を安全に管理します。  
cronやタスクスケジューラを使って定期的な実行も可能です。

---

## 📦 セットアップ手順

### ✅ クローン先のパスにご注意

> ❌ フォルダ名に日本語が含まれているパスや、`OneDrive`、`iCloud`、`ドキュメント`などのクラウドフォルダでは実行に失敗する可能性があります  
> ✅ `C:\Projects` や `~/Projects` のようなローカルの英字パスを推奨

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
```

---

### 環境変数ファイルの設定

```bash
cp info.env.example info.env        # macOS / Linux
copy info.env.example info.env      # Windows
```

`info.env`ファイルを開いて、以下の内容を入力してください：

```env
TARGET_URL=https://example.com/reservation
NAME=山田太郎
PHONE_NUMBER=09012345678
E_MAIL=test@example.com
```

---

## 🧪 実行前のテスト（ブラウザ確認）

> 自動予約を行う前に、ブラウザが正常に動作するかを確認しましょう。

### macOS / Linux / Git Bash

```bash
chmod +x test_run.sh
./test_run.sh
```

### Windows

```cmd
test_run.bat
```

---

## 🚀 自動予約の実行

### macOS / Linux / Git Bash

```bash
chmod +x run.sh
./run.sh
```

### Windows

```cmd
run.bat
```

---

## 🕑 定期実行の設定

### macOS（cronを使用）

```bash
crontab -e
```

以下の行を追加してください（毎週土曜日の午前7時に実行）：

```cron
0 7 * * 6 /Users/yourname/autoBooking/run.sh >> /Users/yourname/autoBooking/cron.log 2>&1
```

### Windows（タスクスケジューラを使用）

1. タスクスケジューラを起動  
2. 新しいタスクを作成  
3. トリガー：毎週土曜日 午前7時  
4. 実行内容：`run.bat` を指定

---

## 📁 ディレクトリ構成

```
autoBooking/
├── main.py                  # 自動予約のメインスクリプト
├── run.sh                   # macOS/Linux 用の実行ファイル
├── run.bat                  # Windows 用の実行ファイル
├── test_run.sh              # テスト実行（.sh）
├── test_run.bat             # テスト実行（.bat）
│
├── step1_access.py          # STEP 1 - 予約ページにアクセス
├── step2_select_date.py     # STEP 2 - 日付選択と○予約クリック
├── step3_select_time.py     # STEP 3 - バドミントン2（9–11時）クリック
├── step4_input_form.py      # STEP 4 - 名前、電話番号、メールの入力
├── step5_confirm.py         # STEP 5 - 最終送信ボタンのクリック
├── utils.py                 # WebDriver設定など共通関数
│
├── info.env.example         # 環境変数テンプレート
├── requirements.txt         # パッケージリスト
├── .gitignore               # 除外対象ファイル
└── README_JP.md             # この日本語マニュアル
```

---

## 📌 バージョン履歴

| 日付       | バージョン | 変更内容                           |
|------------|------------|------------------------------------|
| 2025-04-09 | 1.0.0      | 初回リリース（モジュール化構成、変更なし） |

---

## ✅ ライセンスと作者

- Maintained by [kurooru]  
- License: kurooru