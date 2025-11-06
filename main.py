from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
from keep_alive import keep_alive

TOKEN = "8568305074:AAGldekwMYk_Y_-04bZC0hlO5bR9Nn5fRAc"
CHANNEL_ID = "https://t.me/+LuA1Cm2Jjh83Yjc6"


bot = Bot(TOKEN)
dp = Dispatcher()
kodlar = {}  # kod: file_id

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("🎬 Kino kodini yuboring. Videolar kanal orqali olinadi.")

@dp.channel_post(F.video)
async def new_video(post: types.Message):
    if post.caption and "kod:" in post.caption.lower():
        try:
            kod = int(post.caption.lower().split("kod:")[1])
            kodlar[kod] = post.video.file_id
            print(f"Kod {kod} saqlandi!")
        except:
            print("Caption formatida xato:", post.caption)

@dp.message(F.text.regexp(r"^\d+$"))
async def user_kod(m: types.Message):
    kod = int(m.text)
    file_id = kodlar.get(kod)
    if file_id:
        await bot.send_video(m.chat.id, file_id)
    else:
        await m.answer("❌ Kod topilmadi")

async def main():
    keep_alive()  # bu serverni 24/7 ish holatda ushlab turadi
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
