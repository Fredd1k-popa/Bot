import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8600321504:AAGg_uHZWtSMyf-QrTFRhiw-FYR916Xde_k'
CHANNEL_USERNAME = '@nexum_znoser'

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_keyboard():
    # Создаем клавиатуру с двумя кнопками друг под другом
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перейти в канал", 
                    url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Проверить подписку", 
                    callback_data="check_subscription"
                )
            ]
        ]
    )


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Чтобы получить голду подпишысь на канал", 
        reply_markup=get_keyboard()
    )


@dp.callback_query(lambda c: c.data == "check_subscription")
async def check_sub_handler(callback: types.CallbackQuery):
    try:
        # Запрашиваем статус пользователя в канале
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=callback.from_user.id)
        
        # Проверяем, подписан ли пользователь (статусы: creator, administrator, member)
        if member.status in ["creator", "administrator", "member"]:
            await callback.answer("✅ Подписка подтверждена! Вот твоя голда.", show_alert=True)
            # Здесь можно отправлять сообщение с промокодом или ссылкой
        else:
            await callback.answer("❌ Вы еще не подписались на канал!", show_alert=True)
            
    except Exception as e:
        # Ошибка возникает, если бот не добавлен в админы канала или юзернейм указан неверно
        await callback.answer("⚠️ Ошибка проверки. Убедитесь, что бот назначен администратором канала!", show_alert=True)


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())