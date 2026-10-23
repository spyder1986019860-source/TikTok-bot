import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(
        f"হ্যালো {user_first_name}! 👋\n\n"
        f"আমি @NiraMediaBot। আমাকে যেকোনো TikTok ভিডিওর লিংক পাঠান, আমি সেটি ওয়াটারমার্ক ছাড়া ডাউনলোড করে দেব।"
    )

# ভিডিও ডাউনলোড এবং পাঠানোর ফাংশন
async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    # লিংক ভ্যালিডেশন (TikTok লিংক চেক)
    if "tiktok.com" not in url and "vm.tiktok.com" not in url and "vt.tiktok.com" not in url:
        await update.message.reply_text("❌ এটি সঠিক TikTok ভিডিও লিংক নয়! অনুগ্রহ করে একটি বৈধ TikTok লিংক পাঠান।")
        return

    status_message = await update.message.reply_text("⏳ ভিডিও ডাউনলোড করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")

    output_filename = f"tiktok_{update.message.message_id}.mp4"

    # yt-dlp সেটআপ
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_filename,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        # ভিডিও প্রসেস ও ডাউনলোড
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # টেলিগ্রামে ভিডিও সেন্ড করা
        await update.message.reply_video(
            video=open(output_filename, 'rb'),
            caption="✨ **NiraMediaBot** এর মাধ্যমে আপনার ভিডিও ডাউনলোড সফল হয়েছে!"
        )

        # ওয়েটিং মেসেজ ডিলিট
        await status_message.delete()

    except Exception as e:
        await status_message.edit_text("❌ ভিডিওটি ডাউনলোড করতে সমস্যা হয়েছে। লিংকটি কাজ করছে কিনা দেখুন বা কিছুক্ষণ পর চেষ্টা করুন।")
        print(f"Error: {e}")

    finally:
        # ডাউনলোড ফাইল মুছে ফেলা
        if os.path.exists(output_filename):
            os.remove(output_filename)

if __name__ == '__main__':
    # ⚠️ নিচে চিহ্নিত জায়গায় BotFather থেকে পাওয়া আপনার বটের API Token-টি বসান
    TOKEN = '8601214516:AAEPDyEa-WAo-bjEUPlcgOZ9ZSM-u49_2hs'

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))

    print("🤖 NiraMediaBot সফলভাবে চালু হয়েছে...")
    app.run_polling()
  
