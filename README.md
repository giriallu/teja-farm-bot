# 🐐 Teja Farm Telegram Ledger Bot

A simple Telegram bot to manage farm finances (expenses, salaries, advances, goat/sheep buy & sell, stock, and reports).

✅ 100% Free  
✅ Mobile-friendly (Telegram-based)  
✅ No Excel needed  
✅ Works from farm directly  

---

# 🚀 Features

- Track daily expenses (feed, medicine, transport, etc.)
- Manage worker advances & salaries
- Record goat/sheep purchases and sales
- Auto stock tracking
- Daily & monthly reports
- Simple chat-based input

---

# 📱 Example Commands
expense feed 500
expense medicine 300
advance raju 2000
salary raju 8000
buy goat 5 20000
sell goat 2 15000
stock
today
month
worker raju

---

# 🛠️ Setup Guide

---

# 🟢 1. Create Telegram Bot

1. Open Telegram
2. Search **BotFather**
3. Run:
/start
/newbot

4. Provide:
   - Bot Name → TejaFarmLedger
   - Username → tejafarmledger_bot

5. Copy the **BOT TOKEN**

---

# 💻 2. Run Locally

## Step 1: Install Python

Install Python 3.11+

## Step 2: Install Dependencies
pip install python-telegram-bot==13.15 pandas

## Step 3: Set Environment Variable

### Linux / Mac
export BOT_TOKEN=your_token


### Windows

set BOT_TOKEN=your_token


## Step 4: Run Bot


python bot.py


## Output


Bot started successfully...


---

## ⚠️ Important

- Only one instance should run at a time  
- Do NOT run both local and cloud simultaneously  

---

# ☁️ 3. Deploy on Render (FREE 24/7)

## Step 1: Push Code to GitHub

Create repository and upload:


bot.py
requirements.txt
.python-version


---

## Step 2: Add `.python-version`


3.11.9


---

## Step 3: Create Render Service

1. Login to Render
2. Click **New → Web Service**
3. Connect GitHub repo

---

## Step 4: Configure


Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: python bot.py


---

## Step 5: Add Environment Variable


BOT_TOKEN=your_token


---

## Step 6: Deploy

Click **Create Web Service**

Wait 2–5 minutes

---

## Step 7: Verify Logs

You should see:


Running 'python bot.py'


---

# 📊 Available Commands

| Command | Description |
|--------|-------------|
| expense feed 500 | Add expense |
| advance raju 2000 | Worker advance |
| salary raju 8000 | Salary payment |
| buy goat 5 20000 | Purchase goats |
| sell goat 2 15000 | Sell goats |
| stock | Show animal stock |
| today | Today report |
| month | Monthly report |
| worker raju | Worker ledger |

---

# 🧪 Debugging

## View Logs (Render)

- Open service → Logs tab

## Add Debug Logs

Inside code:

```python
print("Bot started")
print(update.message.text)
```
⚠️ Known Issues
Python Version Error

If you see:

ModuleNotFoundError: No module named 'imghdr'
Fix:

Ensure .python-version contains:

3.11.9

Then:

Clear build cache
Redeploy
💾 Data Storage
Uses SQLite database (teja_farm.db)
Stored locally or in Render container

⚠️ Note: Render storage is temporary (data may reset)

🔮 Future Improvements
Auto daily report
Google Drive backup
Voice input support
Dashboard UI
Export to Excel
👨‍💻 Author

Teja Farm Ledger System
Built for simple farm financial tracking using Telegram.
