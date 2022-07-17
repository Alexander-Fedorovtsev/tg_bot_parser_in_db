### Телеграм бот, который умеет:
1. По команде запускает парсинг страницы https://ru.wikipedia.org/wiki/Городские_населённые_пункты_Московской_области, и сохраненяет\обновляет данные в бд.
Для этого выполните команду /start в боте, появится кнопка меню "Выполнить парсинг"
2. При обращении к боту в чате, при написании названия города или его части - отображает список подходящих городов.
3. При выборе конкретного города — выводит его численность и ссылку на вики.

### База данных 
В данном проекте используется БД SQLite 

### Настройка бота
Для корректной работы бота необходимо в файле config.py прописать API_TOKEN="" вашего бота.
Так же необходимо через botfather добавить одну команду /start для бота, или же при первом запуске ввести ее вручную.

### Установка бота
1. Клонируйте репозиторий
2. Добавьте в config.py токен вашего бота (необходимо его предварительно создать через (Botfather)[https://botcreators.ru/blog/kak-sozdat-svoego-bota-v-botfather/])
3. Установите Venv и зависимости из файла requirements.txt
4. Запускайте bot.py, бот начнет работу на локальной машине и будет доступен через Телеграм
