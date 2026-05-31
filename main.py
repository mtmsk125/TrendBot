import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# قراءة التوكن من النظام مباشرة
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("البوت يعمل الآن ومستعد لجلب الترندات!")

if __name__ == '__main__':
    # التأكد من وجود التوكن قبل البدء
    if not BOT_TOKEN:
        print("خطأ: يرجى إعداد متغير BOT_TOKEN في منصة Render")
    else:
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        print("البوت بدأ العمل...")
        application.run_polling()
        
