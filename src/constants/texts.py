
# middlewares/utils
REGISTER_OK_BTN = 'Да, все окей ✅!'
REGISTER_FAIL_BTN = 'Нет, пройду сначала ❌'

# routers/start
HELLO_TEXT = "Здравствуйте! 👋 Давайте пройдем регистрацию. Введите фамилию, имя и отчество (при наличии) через пробел"
FIO_ERROR_TEXT = "👤❕ Пожалуйста, введите корректные фамилию, имя и отчество (при наличии)"
COURSE_CHANGE_TEXT = f"📕 А теперь выберите Ваш курс:"
PROGRAM_CHANGE_TEXT = f"🍋 Теперь направление:"
EMAIL_CHANGE_TEXT = f"📧 Теперь введите Вашу почту:"
EMAIL_ERROR_TEXT = "📧❕ Пожалуйста, введите корректный email адрес"
RESULT_TEXT = ("👤 Ваше ФИО: {fio}\n"
               "📕 Ваш курс: {course}\n"
               "🍋 Ваше направление: {program}\n"
               "📧 Ваш email: {email}\n"
               "Все верно?")
QR_CODE_TEXT = "Вот Ваш QR-код"
COMMAND_TEXT = ("/start - изменить информацию о себе ✏️\n"
                "/help - показать это сообщение снова 💭\n"
                "/menu - вызвать меню с кнопками 📌\n"
                "/qr - получить свой qr-код 🔳")
USER_ALREADY_EXISTS_TEXT = "Кажется, Вы уже зарегистрированы"

# routers/menu
SCHEDULE_BTN = "🗓 Расписание активностей 🗓"
ACTIVITY_MAP_BTN = "🗺 Карта локаций 🗺"
NU_KAK_TAM_S_DENGAMI_BTN = "🎁 Как получить материалы и приз 🎁"
SEND_QR = "🔳 Получить свой QR-код 🔳"
ATTENDED_ACTIVITY = "❣️ Посещенные активности ❣️"

EXCEPTION_MESSAGE = ("Что-то пошло не так 🤷\n"
                     "Попробуй еще раз или чуть позже.\n\n"
                     "Если проблема не исчезнет - обратись в поддержку и перешли это сообщение: @poka\\_nekuda\n\n"
                     "Код ошибки: `#{}`")

UNREGISTERED_USER_EXCEPTION = ("Кажется, ты не зарегистрирован 😔\n\n"
                               "Пройди регистрацию (/start) и возвращайся 😊")

COMPANY_VISIT = "Ты посетил стенд компании {company}!\n"
BAD_COMPANY_VISIT = "Ты уже посетил стенд этой компании 😎👍"
TO_SITE = "На сайт компании ↗️"

