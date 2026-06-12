# 使用教學

## 啟動 Bot

### 1. 準備環境

```powershell
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境（PowerShell）
. .\.venv\Scripts\Activate.ps1
```

### 2. 安裝依賴

```powershell
pip install -r requirements.txt
```

### 3. 設定 Token

複製 `.env.example` 為 `.env`：

```powershell
Copy-Item .env.example .env
```

編輯 `.env`，填入你的 Bot Token：

```env
DISCORD_TOKEN=your-bot-token-here
```

### 4. 啟動 Bot

```powershell
python bot.py
```

你應該會看到類似的輸出：

```
✓ Logged in as YourBot#1234
✓ Synced 1 slash command(s)
```

## 指令使用

### /greet 打招呼

基本用法：

```
/greet
```

或指定名字：

```
/greet name:Alice
```

**範例：**
- `/greet` → 回應：`👋 Hello User! Welcome to the bot!`
- `/greet name:Bob` → 回應：`👋 Hello Bob! Welcome to the bot!`

## 常見問題

**Q：找不到 Bot Token？**  
A：到 [Discord Developer Portal](https://discord.com/developers/applications) 建立應用，在「Bot」標籤複製 Token。

**Q：指令沒出現？**  
A：檢查終端是否顯示「Synced 1 slash command(s)」。若沒有，重啟 Bot 或刷新 Discord (Ctrl+R)。

**Q：Bot 無法連接？**  
A：確認 Token 是否正確，且 Bot 有加入你的伺服器。

## 下一步

現在你可以在 `cogs/slides.py` 中：
- 修改或刪除 `/greet` 指令
- 新增你自己的指令

詳見 [setup_and_architecture.md](setup_and_architecture.md) 的「擴充指令」章節。



