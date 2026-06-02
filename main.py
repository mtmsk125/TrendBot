import os
import json
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = '@MyTrendChannel' 

# دالة تحميل البيانات
def load_products():
    with open('products.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# دالة النشر التلقائي (التي كانت لديك)
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

# واجهة القائمة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏗️ الخدمات الهندسية", callback_data='mep_tools')],
        [InlineKeyboardButton("💻 الحلول والذكاء الاصطناعي", callback_data='tech_solutions')],
        [InlineKeyboardButton("⚙️ إدارة الحساب", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بك في المنصة الهندسية المتكاملة. اختر الخدمة:", reply_markup=reply_markup)

# التعامل مع الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'mep_tools':
        await query.edit_message_text("🏗️ **قسم الخدمات الهندسية (MEP):**\n- 📐 استخراج الكميات (قريباً...)\n- 💡 حاسبة الأحمال (قريباً...)")
    elif query.data == 'tech_solutions':
        await query.edit_message_text("💻 **قسم الحلول التقنية:**\n- 📈 الترندات والبحث (مفعل)\n- 🤝 دليل الموردين (قريباً...)")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # جدولة النشر التلقائي (كل 24 ساعة مثلاً)
    job_queue = application.job_queue
    job_queue.run_repeating(auto_post, interval=86400, first=10)
    
    application.run_polling()
        
