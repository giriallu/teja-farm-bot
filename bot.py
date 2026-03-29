import sqlite3
import os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from datetime import datetime
import pandas as pd

# Telegram Bot Token
TOKEN = os.environ.get("BOT_TOKEN")  # set BOT_TOKEN in environment variable

# Connect to local database
conn = sqlite3.connect("teja_farm.db", check_same_thread=False)
cursor = conn.cursor()

# Create ledger table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ledger(
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT,
type TEXT,
amount REAL,
person TEXT,
item TEXT
)
""")

# Create stock table
cursor.execute("""
CREATE TABLE IF NOT EXISTS stock(
item TEXT PRIMARY KEY,
quantity INTEGER
)
""")
conn.commit()

# Save entry
def save_entry(update, context):
    text = update.message.text.lower().split()
    try:
        cmd = text[0]
        
        # Expense, salary, advance
        if cmd in ["expense","salary","advance"]:
            amount = float(text[1])
            person = text[2] if len(text)>2 else ""
            details = " ".join(text[3:]) if len(text)>3 else ""
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute(
                "INSERT INTO ledger(date,type,amount,person,item) VALUES(?,?,?,?,?)",
                (date,cmd,amount,person,details)
            )
            conn.commit()
            update.message.reply_text("✅ Entry Saved")
        
        # Buy goats/sheep
        elif cmd=="buy":
            item = text[1]
            quantity = int(text[2])
            amount = float(text[3])
            # Add to ledger
            cursor.execute(
                "INSERT INTO ledger(date,type,amount,person,item) VALUES(?,?,?,?,?)",
                (datetime.now().strftime("%Y-%m-%d %H:%M"), "buy", amount, "", f"{quantity} {item}")
            )
            # Update stock
            cursor.execute("SELECT quantity FROM stock WHERE item=?",(item,))
            row = cursor.fetchone()
            if row: cursor.execute("UPDATE stock SET quantity=? WHERE item=?",(row[0]+quantity,item))
            else: cursor.execute("INSERT INTO stock(item,quantity) VALUES(?,?)",(item,quantity))
            conn.commit()
            update.message.reply_text(f"✅ Purchased {quantity} {item}")
        
        # Sell goats/sheep
        elif cmd=="sell":
            item = text[1]
            quantity = int(text[2])
            amount = float(text[3])
            # Add to ledger
            cursor.execute(
                "INSERT INTO ledger(date,type,amount,person,item) VALUES(?,?,?,?,?)",
                (datetime.now().strftime("%Y-%m-%d %H:%M"), "sell", amount, "", f"{quantity} {item}")
            )
            # Update stock
            cursor.execute("SELECT quantity FROM stock WHERE item=?",(item,))
            row = cursor.fetchone()
            if row: cursor.execute("UPDATE stock SET quantity=? WHERE item=?",(row[0]-quantity,item))
            else: cursor.execute("INSERT INTO stock(item,quantity) VALUES(?,?)",(item,-quantity))
            conn.commit()
            update.message.reply_text(f"✅ Sold {quantity} {item}")
        
        else:
            update.message.reply_text(
                "Commands:\n"
                "expense 500 feed\nadvance 2000 raju\nsalary 8000 raju\n"
                "buy goat 5 20000\nsell goat 3 18000\n"
                "stock\ntoday\nmonth\nworker raju"
            )
    except Exception as e:
        update.message.reply_text(f"⚠ Format Error\n{e}")

# Stock check
def show_stock(update, context):
    rows = cursor.execute("SELECT * FROM stock").fetchall()
    msg = "🐐 Farm Stock\n\n"
    for r in rows: msg += f"{r[0]} : {r[1]}\n"
    update.message.reply_text(msg)

# Today report
def today_report(update, context):
    today = datetime.now().strftime("%Y-%m-%d")
    rows = cursor.execute(
        "SELECT type,SUM(amount) FROM ledger WHERE date LIKE ? GROUP BY type",(today+'%',)
    ).fetchall()
    msg = "📊 Today Report\n\n"
    total_income = 0
    total_expense = 0
    for r in rows:
        msg += f"{r[0]} : {r[1]}\n"
        if r[0] in ["sell"]: total_income += r[1]
        elif r[0] in ["expense","salary","advance","buy"]: total_expense += r[1]
    profit = total_income - total_expense
    msg += f"\nProfit : {profit}"
    update.message.reply_text(msg)

# Worker ledger
def worker_ledger(update, context):
    text = update.message.text.split()
    if len(text)<2:
        update.message.reply_text("Usage: worker raju")
        return
    person = text[1]
    rows = cursor.execute(
        "SELECT type,amount FROM ledger WHERE person=?",(person,)
    ).fetchall()
    msg = f"👷 Worker Ledger: {person}\n\n"
    total_advance = sum(r[1] for r in rows if r[0]=="advance")
    total_salary = sum(r[1] for r in rows if r[0]=="salary")
    balance = total_advance - total_salary
    msg += f"Advance : {total_advance}\nSalary Paid : {total_salary}\nBalance : {balance}"
    update.message.reply_text(msg)

# Monthly report
def month_report(update, context):
    month = datetime.now().strftime("%Y-%m")
    rows = cursor.execute(
        "SELECT type,SUM(amount) FROM ledger WHERE date LIKE ? GROUP BY type",(month+'%',)
    ).fetchall()
    msg = f"📊 {month} Report\n\n"
    total_income = 0
    total_expense = 0
    for r in rows:
        msg += f"{r[0]} : {r[1]}\n"
        if r[0] in ["sell"]: total_income += r[1]
        elif r[0] in ["expense","salary","advance","buy"]: total_expense += r[1]
    profit = total_income - total_expense
    msg += f"\nProfit : {profit}"
    update.message.reply_text(msg)

# Main
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("stock", show_stock))
    dp.add_handler(CommandHandler("today", today_report))
    dp.add_handler(CommandHandler("month", month_report))
    dp.add_handler(MessageHandler(Filters.regex("^worker"), worker_ledger))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, save_entry))

    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()
