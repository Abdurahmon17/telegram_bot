from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio

TOKEN = "BotToken"
CHANNEL_ID = "Kana username yoki kanal_id"

bot = Bot(TOKEN)
dp = Dispatcher()

# Xotirada saqlash
kodlar = {}  # kod: file_id

# /start
@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("🎬 Kino kodini yuboring. Videolar kanal orqali olinadi.")

# Kanalga yangi video post kelganda
@dp.channel_post(F.video)
async def new_video(post: types.Message):
    if post.caption and "kod:" in post.caption.lower():
        try:
            kod = int(post.caption.lower().split("kod:")[1])
            kodlar[kod] = post.video.file_id
            print(f"Kod {kod} saqlandi!")
        except:
            print("Caption formatida xato bor:", post.caption)

# Foydalanuvchi kod yuborganida
@dp.message(F.text.regexp(r"^\d+$"))
async def user_kod(m: types.Message):
    kod = int(m.text)
    file_id = kodlar.get(kod)
    if file_id:
        await bot.send_video(m.chat.id, file_id)
    else:
        await m.answer("❌ Kod topilmadi")

# Run bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
