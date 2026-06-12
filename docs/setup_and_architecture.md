# 專案架構說明（基礎版）

## 目的

建立一個簡潔的 Discord Bot 基礎專案骨架，搭配 **Slash Command** 架構，幫助初學者理解 bot 開發的核心結構。

## 目錄結構

```
note-bot/
├── bot.py                      # Bot 啟動程式（主入口）
├── requirements.txt            # 依賴套件清單
├── .env                        # 環境變數（本地用，不上傳 Git）
├── .env.example                # 環境變數範例
├── cogs/
│   ├── __init__.py             # Cog 套件初始化
│   └── slides.py               # Cog 範例：包含打招呼指令
├── data/                       # 資料儲存目錄
└── docs/
    ├── setup_and_architecture.md   # 本檔案
    └── usage_guide.md              # 使用教學
```

## 核心概念

### 1. 什麼是 Cog？
**Cog** 是 discord.py 用來組織指令的方式。每個 Cog 是一個包含相關指令的模組：

```python
class Slides(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="greet")
    async def greet(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Hello {name}!")

async def setup(bot):
    await bot.add_cog(Slides(bot))
```

**為什麼用 Cog？**
- ✅ 將指令分離到不同檔案，避免 `bot.py` 變得太大
- ✅ 易於擴充：新增指令時只需新增 Cog 檔案
- ✅ 便於管理：每個功能集合有獨立的類別

### 2. Slash Command 是什麼？
Slash Command 是以 `/` 開頭的指令，由 Discord 自動顯示，提供更好的 UX：

```python
@app_commands.command(name="greet", description="打招呼")
async def greet(self, interaction: discord.Interaction, name: str = "User"):
    await interaction.response.send_message(f"Hello {name}!")
```

**優勢：**
- ✅ 自動補完與參數驗證
- ✅ Discord 在輸入框顯示指令提示
- ✅ 更現代、更易用的方式

### 3. Intents 是什麼？
Intents 定義 Bot 能接收哪些事件類型：

```python
intents = Intents.default()
bot = commands.Bot(intents=intents)
```

常見的 Intents：
- `message_content`：允許讀取訊息內容
- `guilds`：接收伺服器事件
- `members`：接收成員事件

## 檔案說明

### bot.py
啟動程式，負責：
1. 從 `.env` 讀取 Token
2. 初始化 Bot 與 intents
3. 載入 Cogs
4. 同步 slash commands
5. 啟動 Bot

**關鍵流程：**
```python
@bot.event
async def on_connect():
    """連接時載入 Cogs"""
    await load_cogs()

@bot.event
async def on_ready():
    """連接成功時同步指令"""
    synced = await bot.tree.sync()
```

### cogs/slides.py
Cog 範例檔案，包含一個簡單的打招呼指令。

```python
@app_commands.command(name="greet", description="打招呼")
async def greet(self, interaction: discord.Interaction, name: str = "User"):
    await interaction.response.send_message(f"👋 Hello {name}!")
```

### .env 與 .env.example
- `.env.example`：環境變數的模板（上傳到 Git）
- `.env`：實際的環境變數，包含敏感資訊（**不上傳到 Git**）

```env
DISCORD_TOKEN=your-bot-token-here
```

## 快速開始

### 1. 設定環境

```powershell
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
. .\.venv\Scripts\Activate.ps1
```

### 2. 安裝依賴

```powershell
pip install -r requirements.txt
```

### 3. 設定 Token

```powershell
# 複製範例檔案
Copy-Item .env.example .env

# 編輯 .env，填入你的 DISCORD_TOKEN
# DISCORD_TOKEN=你的-bot-token
```

### 4. 啟動 Bot

```powershell
python bot.py
```

## 下一步：擴充指令

若要新增新的指令：

### 方式 1：在 slides.py 中新增方法

```python
@app_commands.command(name="hello")
async def hello(self, interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")
```

### 方式 2：建立新的 Cog

1. 在 `cogs/` 新增 `my_commands.py`：

```python
from discord.ext import commands
from discord import app_commands
import discord

class MyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test command works!")

async def setup(bot):
    await bot.add_cog(MyCommands(bot))
```

2. 在 `bot.py` 的 `load_cogs()` 中載入它：

```python
async def load_cogs():
    await bot.load_extension("cogs.slides")
    await bot.load_extension("cogs.my_commands")
```

或使用自動載入（遍歷所有 .py 檔案）。

## 學習重點

- 📌 Cog 是組織指令的核心方式
- 📌 Slash Command 提供更好的使用體驗
- 📌 Intents 控制 Bot 能接收的事件
- 📌 Interaction 是 slash command 的回應物件
- 📌 環境變數保護敏感資訊（如 Token）

## 常見問題

**Q：為什麼指令沒出現？**  
A：確保 `bot.tree.sync()` 成功執行。檢查終端是否顯示「Synced N slash command(s)」。

**Q：如何修改指令名稱？**  
A：編輯 `@app_commands.command(name="...")` 的 `name` 參數。

**Q：如何新增指令參數？**  
A：在函數簽名中新增參數，Discord 會自動提示：
```python
async def greet(self, interaction, name: str, age: int = 18):
```

