import sqlite3


class SQLighter:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)
            ).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)",
                (user_id, status),
            )

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?",
                (status, user_id),
            )

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


class SQLcity(SQLighter):
    def __init__(self, database):
        super().__init__(database)
        self.cities_cache = []
        self.request_cahe = ""

    def add_city(self, city, url, population):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `cities` (`name`,`url`,`population`, `u_name`) VALUES(?,?,?,?)",
                (
                    city,
                    url,
                    population,
                    city.upper(),
                ),
            )

    def mylog(self):
        print(self.request_cahe)

    def _get_city_info(self, string):
        self.request_cahe = string
        with self.connection:
            result = [
                [*item]
                for item in self.cursor.execute(
                    "SELECT name,url,population FROM cities WHERE u_name LIKE ?",
                    [
                        string.upper() + "%",
                    ],
                ).fetchall()
            ]
            self.cities_cache = []
            for item in result:
                self.cities_cache.append(item)

    def get_city_names(self, string):
        if self.request_cahe != string:
            self._get_city_info(string)
        return [item[0] for item in self.cities_cache]

    def get_city_names_str(self, string):
        if self.request_cahe != string:
            self._get_city_info(string)
        return "\n".join([item[0] for item in self.cities_cache])

    def get_city_url(self):
        if len(self.cities_cache) == 0:
            return "Не могу найти ulr, в базе нет города"
        elif len(self.cities_cache) > 1:
            return "\nНайдено много городов, введите название одного"
        return (
            '\n<a href="https://ru.wikipedia.org/'
            + self.cities_cache[0][1]
            + '">'
            + self.cities_cache[0][0]
            + "</a>"
        )

    def get_city_population(self):
        if len(self.cities_cache) == 1:
            return "\nНаселение: " + str(self.cities_cache[0][2])


if __name__ == "__main__":
    # код для отладки
    db = SQLcity("db.db")
    CITY = "вере"
    for item in db.get_city_names(CITY):
        print(item)
    print(db.get_city_url())
    print(db.get_city_population())
