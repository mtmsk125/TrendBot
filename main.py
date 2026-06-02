import os
import json
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = '@MyTrendChannel' # استبدله بمعرف قناتك

# دالة تحميل البيانات (للترندات)
def load_products():
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return [{"title_ar": "أداة فحص ذكية", "problem": "صعوبة في التشخيص", "link": "https://amazon.com"}]

# دالة النشر التلقائي في القناة
async def auto_post(context: ContextTypes.DEFAULT_TYPE):
    try:
        products = load_products()
        product = random.choice(products)
        message = (f"⚡ **عرض اليوم | {product['title_ar']}**\n\n"
                   f"💡 **المشكلة:** {product['problem']}\n"
                   f"🔗 **اطلبها الآن:** {product['link']}")
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"خطأ في النشر: {e}")

# واجهة البوت الأساسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🏗️ **أهلاً بك في المنصة الهندسية المتكاملة** ⚙️\n\n"
        "أنا مساعدك الشخصي ومرجعك الهندسي. اختر الخدمة من القائمة:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📚 المكتبة الفنية والأكواد", callback_data='mep_tools')],
        [InlineKeyboardButton("🤖 اسأل المساعد الهندسي", callback_data='tech_solutions')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# التعامل مع الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'mep_tools':
        await query.edit_message_text(
            "⚙️ **المرجع الهندسي:**\n\n"
            "1. 📚 [المكتبة الفنية (أكواد NFPA)](https://www.nfpa.org/codes-and-standards)\n"
            "2. 📐 [محولات الوحدات الهندسية](https://www.unitconverters.net/)\n\n"
            "استخدم القائمة للعودة للخلف لاحقاً."
        )
    elif query.data == 'tech_solutions':
        await query.edit_message_text(
            "🤖 **أنا هنا معك!**\n"
            "أرسل سؤالك الهندسي في رسالة وسأقوم بالإجابة عليك فوراً كاستشارة تقنية."
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # جدولة النشر التلقائي (كل 24 ساعة)
    job_queue = application.job_queue
    job_queue.run_repeating(auto_post, interval=86400, first=10)
    
    application.run_polling()
        
