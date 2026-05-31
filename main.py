import logging
from telegram.ext import ApplicationBuilder, CommandHandler
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update, context):
    await update.message.reply_text("البوت يعمل الآن ومستعد لجلب الترندات!")

if __name__ == '__main__':
    # استخدام التوكن من ملف config.py
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    
    print("البوت بدأ العمل...")
    application.run_polling()
  
