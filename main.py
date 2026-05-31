import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler

# إعدادات التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# دالة محاكاة لجلب منتج ترند (حتى يتوفر الـ API)
async def get_trend_product():
    # هنا لاحقاً سنضع كود الـ Scraping أو الـ API
    return {
        "title_en": "Professional Laser Distance Measurer",
        "title_ar": "جهاز قياس المسافات بالليزر احترافي",
        "description_en": "High-precision tool for MEP engineers.",
        "description_ar": "أداة عالية الدقة لمهندسي الميكانيك والكهرباء.",
        "link": "https://amazon.com/your-affiliate-link"
    }

async def start(update, context):
    await update.message.reply_text("البوت يعمل! استخدم /trend لجلب أحدث المنتجات.")

async def trend(update, context):
    # جلب المنتج
    product = await get_trend_product()
    
    # تنسيق الرسالة
    message = (
        f"{product['title_en']} | {product['title_ar']} 🛠️\n\n"
        f"{product['description_en']}\n"
        f"{product['description_ar']}\n\n"
        f"🔗 الرابط: {product['link']}\n\n"
        f"#CleverMarketing #Engineering"
    )
    
    # إرسال الرسالة لك (أنت فقط) لتنسخها وتنشرها
    await update.message.reply_text(message)

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("خطأ: يرجى إعداد متغير BOT_TOKEN")
    else:
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('trend', trend)) # إضافة أمر التند
        print("البوت بدأ العمل...")
        application.run_polling()
    
