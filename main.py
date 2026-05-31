import os
import json
import random
import logging
from telegram.ext import ApplicationBuilder, CommandHandler

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# دالة قراءة ملف المنتجات
def load_products():
    with open('products.json', 'r', encoding='utf-8') as f:
        return json.load(f)

async def start(update, context):
    await update.message.reply_text("مرحباً! البوت يعمل. استخدم /trend لجلب منتج للنشر.")

async def trend(update, context):
    try:
        products = load_products()
        product = random.choice(products)
        
        # صياغة المنشور
        message = (
            f"{product['title_en']} | {product['title_ar']} 🛠️\n\n"
            f"{product['description_en']}\n"
            f"{product['description_ar']}\n\n"
            f"🔗 احصل عليه الآن: {product['link']}\n\n"
            f"#CleverMarketing #Engineering"
        )
        
        # النشر في القناة (استبدل @YourChannelUsername بمعرف قناتك)
        await context.bot.send_message(chat_id='@MyTrendChannel', text=message)
        await update.message.reply_text("✅ تم نشر المنتج في القناة بنجاح!")
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('trend', trend))
    application.run_polling()
    
