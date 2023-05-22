import openai                                       # Импортируем модуль openai для взаимодействия с OpenAI API
from aiogram import Bot, types                      # Импортируем классы Bot и types из модуля aiogram
from aiogram.dispatcher import Dispatcher           # Импортируем класс Dispatcher из модуля aiogram.dispatcher
from aiogram.utils import executor                  # Импортируем функцию executor из модуля aiogram.utils

TOKEN = 'YOUR_BOT_TOKEN'                            # Задаем токен нашего бота
openai.api_key = 'YOUR_OPENAI_API_KEY'              # Задаем ключ API для взаимодействия с OpenAI API

bot = Bot(TOKEN)                                    # Создаем экземпляр класса Bot, передавая токен вашего бота
dp = Dispatcher(bot)                                # Создаем экземпляр класса Dispatcher, связанный с ботом

@dp.message_handler()                               # Создаем обработчик, который будет мониторить то, что пишет пользователь
async def send(message: types.Message):             # Может использовать асинхронные операции, такие как отправка сообщений и взаимодействие с OpenAI API
    try:
        # Берем готовые параментры ответа с сайта AI (https://platform.openai.com/examples/default-chat), немного отредактировав
        response = openai.Completion.create(
            model="text-davinci-003",               # Выбираем модель "text-davinci-003" для генерации текста
            prompt=message.text,                    # Используем текст сообщения пользователя в качестве начала (промпт) для генерации ответа
            temperature=0.9,                        # Устанавливаем параметр температуры генерации в 0.9 для управления разнообразием ответов
            max_tokens=1000,                        # Ограничиваем максимальное количество токенов (включая пробелы) в ответе до 1000(можно сократить или увеличить)
            top_p=1,
            frequency_penalty=0.0,                  # Устанавливаем штраф за частоту токенов в ответе равным 0.0
            presence_penalty=0.6,                   # Устанавливаем штраф за присутствие токенов, равный 0.6
            stop=[" Human:", " AI:"]                # Задаем список стоп-токенов, указывающих модели, когда остановить генерацию текста
        )
        await message.answer(response['choices'][0]['text'])                # Отправляем пользователю отфильтрованный текст ответа
    except openai.OpenAIError as e:                                         # Обрабатываем ошибку, возникшую при запросе к OpenAI API
        await message.answer(f"Произошла ошибка при запросе к OpenAI API: {str(e)}")
    except Exception as e:                                                  # Обрабатываем другие непредвиденные ошибки
        await message.answer(f"Произошла непредвиденная ошибка: {str(e)}")

executor.start_polling(dp, skip_updates=True)                               # Запускаем бота для обработки вход




