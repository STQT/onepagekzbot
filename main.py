"""
This is a echo bot.
It echoes any incoming text messages.
"""
import json
import logging

from aiogram import Bot, Dispatcher, executor, types

from btns import main_page_button
from configs import BOT_TOKEN
from utils import get_or_create_user, upload_updates_to_server

API_TOKEN = BOT_TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await get_or_create_user(tg_id=message.from_user.id,
                             username=message.from_user.username,
                             first_name=message.from_user.first_name,
                             last_name=message.from_user.last_name)
    text = ("ONEPAGE.kz\n"
            "*Что мы сделаем для Вашего бизнеса*\n"
            " 1 Проведем аудит вашей ниши.\n"
            " 2 Определим конкурентов.\n"
            " 3 Определим целевую аудиторию.\n"
            " 4 Предложим маркетинг план для продвижение бизнеса.\n"
            " 5 Разработаем сайт.\n"
            " 6 Автоматизируем отдел продажи внедрим CRM систему.\n"
            " 7 Обучим менеджеров отдела продажи пользоваться CRM системой.\n"
            " 8 Настроим рекламу в Интернет.\n"
            " 9 Обеспечим поток клиентов. Увеличим продажи.")

    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    text_and_data = (
        ('Разработка сайта', 'sites'),
        ('SEO оптимизация', 'seos'),
        ('Контекстная реклама', 'contexts'),
        ('Оставить заявку', 'application'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    # keyboard_markup.row(*row_btns)
    for row in row_btns:
        keyboard_markup.row(row)
    keyboard_markup.add(
        # url buttons have no callback data
        types.InlineKeyboardButton('Перейти на сайт', url='https://onepage.kz'),
    )
    await message.answer_photo(photo=types.InputFile("media/logo3.png"), caption=text, parse_mode="Markdown",
                               reply_markup=keyboard_markup)


@dp.message_handler()
async def echo(message: types.Message):
    result = json.loads(message.as_json())
    await upload_updates_to_server(tg_id=message.from_user.id, json=result)
    await message.answer(message.text)


@dp.callback_query_handler(text='main_page')
async def main_page_query_handler(query: types.CallbackQuery):
    await query.answer("Сайты")
    await send_welcome(query.message)


@dp.callback_query_handler(text='sites')
async def site_query_handler(query: types.CallbackQuery):
    await query.answer("Сайты")
    text = ("Решили начать свой бизнес или вдохнуть новую жизнь в уже существующую компанию "
            "и не знаете с чего начать? Решение есть. Доверьте свое дело интернету. "
            "Сарафанное радио и хорошую репутацию, конечно, никто не отменял, "
            "но новые клиенты в основном приходят из интернета. ")
    text2 = ("*Мы разработаем для вас*\n"
             "🪪 Сайт визитка\n"
             "🛍 Интернет магазин\n"
             "🧾 Сайт каталог\n"
             "🛬 Landing Page")
    await query.message.answer_photo(photo=types.InputFile('media/sites.jpg'), caption=text)
    await query.message.answer(text2, reply_markup=main_page_button(), parse_mode="Markdown")


@dp.callback_query_handler(text='seos')
async def seos_query_handler(query: types.CallbackQuery):
    await query.answer("SEO")
    text = ("Что такое SEO продвижение и что нужно знать, чтобы не навредить "
            "Большинство клиентов в современном мире узнают о товаре или услуге из интернета. "
            "Для того, чтобы привлечь как можно больше клиентов, существует такой инструмент "
            "как SEO оптимизация. ")
    text2 = ("SEO оптимизация\n"
             "Этапы работы надо SEO оптимизацией сайта\n"
             "1 - внутренняя оптимизация сайта\n"
             "2 - написание текстов под SEO\n"
             "3 - внешняя оптимизация сайта \n\n"
             "   Преимущества SEO\n"
             "➕ Бесплатная реклама\n"
             "➕ Нет денег, есть трафик\n"
             "➕ Доверие клиентов\n"
             "➕ В ТОПе на долго\n"
             "   Недостатки SEO\n"
             "➖ Время 4-6 месяцев")
    await query.message.answer_photo(photo=types.InputFile('media/seo_search.jpg'), caption=text)
    await query.message.answer_photo(photo=types.InputFile('media/seo_1.png'), caption=text2,
                                     reply_markup=main_page_button())


@dp.callback_query_handler(text='application')
async def seos_query_handler(query: types.CallbackQuery):
    await query.answer("Отправьте свой номер")
    share_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    share_button = types.KeyboardButton(text="📲 Отправить номер", request_contact=True)
    share_keyboard.add(share_button)
    await query.message.answer("Отправьте свой номер нажимая кнопку снизу👇", reply_markup=share_keyboard)


@dp.callback_query_handler(text='contexts')
async def contexts_query_handler(query: types.CallbackQuery):
    await query.answer("Контекстная реклама")
    text = ("Реклама в интернете\n"
            "Такая реклама привлекает большое количество потенциальных клиентов. Конверсия "
            "(количество реальных заказов) достаточно высока, потому как это целевая реклама. "
            "Ее видят только те, кто ищет подобные вашим услуги. Наверняка вы уже сталкивались "
            "с таким понятием как контекстная реклама.\n")
    text2 = ("Такое продвижение имеет огромное преимущество по сравнению с другими "
             "рекламными компаниями – это оптимальная цена. Никаких лишних затрат – плата только за клики. "
             "Чем грамотнее будет настроен данный вид рекламы, тем большее количество покупателей она вам принесет. "
             "Настройка контекстной рекламы – дело специалиста. Если вы хотите получить наибольшую отдачу, то лучше "
             "доверить столь ответственный шаг профессионалу. Мы предлагаем нашим клиентам качественные услуги "
             "по разумной цене. Добиться большего эффекта можно, если разместить такую рекламу "
             "на нескольких площадках.\n"
             "Реклама в гугле пользуется большим спросом. На сегодняшний момент "
             "Google – самый распространенный браузер среди пользователей интернета. "
             "На каждой странице любого сайта пестрит реклама гугл. Не увидеть ее невозможно.\n"
             "Стоимость рекламы на данной площадке несколько выше, чем реклама в яндексе, но оно того стоит. "
             "Для привлечения дополнительных клиентов яндекс-реклама – тоже хороший инструмент. "
             "Вы известите о себе огромное количество пользователей браузера яндекс, "
             "а также пользователей почты yandex и mail.\n"
             "Наиболее яркая и запоминающаяся реклама на просторах интернета – баннерная реклама. "
             "Всегда хочется посмотреть, что же там внутри, увидев красивую картинку. "
             "Хотите привлечь большое количество клиентов в свой бизнес – обращайтесь к нам, "
             "и мы увеличим ваши доходы, минимизировав при этом расходы. Желание клиента – наша забота.")
    await query.message.answer_photo(photo=types.InputFile('media/kontext.jpg'), caption=text)
    await query.message.answer(text2, reply_markup=main_page_button())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
