# Discord Bot 基礎專案

簡潔的 Discord bot 骨架，使用 **Slash Command** 架構，適合初學者學習 bot 開發基礎。

## 特色

🎯 **簡化架構**：最小化的程式碼，專注於核心概念  
⚡ **Slash Command**：使用現代的 `/` 指令格式  
🧩 **Cog 系統**：模組化的指令組織方式  

## 快速開始

### 1. 環境設定

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. 設定 Token

```powershell
Copy-Item .env.example .env
# 編輯 .env，填入 DISCORD_TOKEN
```

### 3. 啟動

```powershell
python bot.py
```

## 指令

- `/greet [name]` - 打招呼

## 檔案結構

```
├── bot.py              # 主程式
├── cogs/
│   └── slides.py       # 指令 Cog
├── data/               # 資料存儲
├── docs/               # 文檔
├── requirements.txt    # 依賴
└── .env               # 環境變數
```

## 文檔

- 📖 [架構說明](docs/setup_and_architecture.md) - 詳解整個結構
- 📚 [使用教學](docs/usage_guide.md) - 啟動與使用指令

## 下一步

編輯 `cogs/slides.py` 新增或修改指令。詳見文檔。
