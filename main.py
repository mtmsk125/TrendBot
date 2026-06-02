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

# دالة النشر التلقائي
async def auto_post(context: ContextTypes.DEFAULT_TYPE):
    try:
        # يمكنك إضافة ملف products.json لاحقاً
        message = "⚡ **عرض اليوم**\n\nاكتشف أحدث الأدوات الهندسية عبر منصتنا!"
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"خطأ: {e}")

# واجهة البوت الرئيسية بالأزرار
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "🏗️ **أهلاً بك في المنصة الهندسية المتكاملة** ⚙️\nاختر الخدمة من القائمة:"
    
    keyboard = [
        [InlineKeyboardButton("📚 المرجع الهندسي", callback_data='mep_tools')],
        [InlineKeyboardButton("🤖 اسأل المساعد الذكي", callback_data='tech_solutions')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# التعامل مع الأزرار (هنا السر!)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'mep_tools':
        keyboard = [[InlineKeyboardButton("🔙 العودة للرئيسية", callback_data='back')]]
        await query.edit_message_text(
            "⚙️ **المرجع الهندسي:**\n\n"
            "1. 📚 [المكتبة الفنية (أكواد NFPA)](https://www.nfpa.org/codes-and-standards)\n"
            "2. 📐 [محولات الوحدات الهندسية](https://www.unitconverters.net/)",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown'
        )
    elif query.data == 'tech_solutions':
        keyboard = [[InlineKeyboardButton("🔙 العودة للرئيسية", callback_data='back')]]
        await query.edit_message_text(
            "🤖 **أنا هنا معك!**\nأرسل سؤالك الهندسي في المحادثة وسأجيبك فوراً.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == 'back':
        # إعادة إظهار القائمة الرئيسية
        keyboard = [
            [InlineKeyboardButton("📚 المرجع الهندسي", callback_data='mep_tools')],
            [InlineKeyboardButton("🤖 اسأل المساعد الذكي", callback_data='tech_solutions')]
        ]
        await query.edit_message_text("🏗️ **أهلاً بك في المنصة الهندسية المتكاملة** ⚙️\nاختر الخدمة:", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    job_queue = application.job_queue
    job_queue.run_repeating(auto_post, interval=86400, first=10)
    application.run_polling()
    
