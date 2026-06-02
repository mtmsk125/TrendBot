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

    
