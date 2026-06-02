import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# القائمة الرئيسية - الشجرة
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 المرجع الهندسي", callback_data='mep_tools')],
        [InlineKeyboardButton("📏 حصر الكميات (BOQ)", callback_data='boq_tool')],
        [InlineKeyboardButton("🖥️ موارد الأوتوكاد", callback_data='autocad_res')],
        [InlineKeyboardButton("🤝 دليل الموردين", callback_data='suppliers')],
        [InlineKeyboardButton("🤖 اسأل المساعد الذكي", callback_data='tech_solutions')]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏗️ **أهلاً بك في المنصة الهندسية المتكاملة** ⚙️\nاختر الخدمة المطلوبة:", reply_markup=get_main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'back':
        await query.edit_message_text("🏗️ **أهلاً بك في المنصة الهندسية المتكاملة** ⚙️\nاختر الخدمة المطلوبة:", reply_markup=get_main_menu())
    
    elif query.data == 'mep_tools':
        await query.edit_message_text("⚙️ **المرجع الهندسي:**\n1. [أكواد NFPA](https://www.nfpa.org/codes-and-standards)\n2. [محولات الوحدات](https://www.unitconverters.net/)", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data='back')]]), parse_mode='Markdown')
    
    elif query.data == 'tech_solutions':
        await query.edit_message_text("🤖 **أنا هنا معك!** أرسل سؤالك الهندسي وسأجيبك فوراً.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data='back')]]))
    
    else:
        await query.edit_message_text(f"🚧 **قسم {query.data} قيد التطوير حالياً.**\nسنقوم بتفعيله قريباً!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة", callback_data='back')]]))

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()
    
