import os
import json
import random
import logging
from telegram.ext import ApplicationBuilder

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = '@MyTrendChannel' 

def load_products():
    with open('products.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# دالة النشر التسويقي
async def auto_post(context):
    try:
        products = load_products()
        product = random.choice(products)
        
        # صياغة المنشور
        message = (
            f"⚡ **عرض اليوم | {product['title_ar']}**\n\n"
            f"💡 **المشكلة:** {product['problem']}\n"
            f"🏷️ **خصم خاص:** {product['discount_percentage']}\n\n"
            f"🔗 **اطلبها الآن من هنا:** {product['link']}\n\n"
            f"#CleverMarketing #Engineering #Deals"
        )
        
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
        logging.info("تم النشر بنجاح!")
    except Exception as e:
        logging.error(f"خطأ في النشر: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # إعداد الـ JobQueue
    job_queue = application.job_queue
    
    # 1. النشر فوراً عند بدء التشغيل
    job_queue.run_once(auto_post, when=1)
    
    # 2. النشر التلقائي كل 10 دقائق (600 ثانية)
    job_queue.run_repeating(auto_post, interval=600, first=600)
    
    print("البوت يعمل الآن وسينشر كل 10 دقائق...")
    application.run_polling()
    
