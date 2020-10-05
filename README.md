#Реєстр готових (pre-build) PHP імеджів
Всі доступні версії PHP контейнерів доступні за посиланням: [`https://web.docker.pp.ua/#!taglist/magento2-php`](https://web.docker.pp.ua/#!taglist/magento2-php)

#E-MAIL
Для листів встановлена локальна загрушка, яка не дозволить відправити лист в Internet, а лише збереже його локально для перегляду.

Переглянути всі отримані листи можна за посиланням: [`http://localhost:8025/`](http://localhost:8025/)

![](https://i.imgur.com/GaarM5O.png)

#Конфігурація та параметри
Для конфігурування мадженти використовуються наступні параметри:

![](https://i.imgur.com/QAUICmD.png)

- **`VIRTUAL_HOST`** - хостнейм, який буде використовуватись як адреса веб-сайту
- **`MAGE_MODE`** - режим роботи Magento (`default`, `developer`, `production`, `maintenance`)
- **`MAGE_RUN_TYPE`** - тип коду для ініціалізації (`store`, `website`)
- **`MAGE_RUN_CODE`** - код store або website (залежить від параметра `MAGE_RUN_TYPE`), який буде використовуватись для ініціалізації Magento.

Примітка:
- `MAGE_RUN_TYPE =`**`store`**:
    - `MAGE_RUN_CODE` дивитись БД у таблиці `store`
    - ![](https://i.imgur.com/BSjJBXc.png)

- `MAGE_RUN_TYPE =`**`website`**:
    - `MAGE_RUN_CODE` дивитись БД у таблиці `store_website`
    - ![](https://i.imgur.com/GlJaahP.png)

#Права доступу до директорій:
Для правильної роботи Magento необхідно надати право на запис у наступні директорії:
- `var`
- `app/etc`
- `pub/media`
- `pub/static`

Для цього необхідно виконати команду (знаходитись у директорії проекту):
- **`sudo chmod -R 777 shared code/app/etc code/pub/media code/pub/static`**

#Переглянути активні контейнери:

Команда **`docker ps`**

![](https://i.imgur.com/l5WV11H.png)

- `CONTAINER ID` - ID контейнера
- `IMAGE` - образ контейнера на якому він працює
- `COMMAND` - головна команда контейнера (задається при створенні в `Dockerfile`)
- `CREATED` - дата створення
- `STATUS` - час роботи від старту
- `PORTS` - показує як локальний (доступний на ПК) порт співвідноситься до порту в контейнері Docker
- `NAMES` - ім'я контейнера - використовується у командах по роботі з контейнером

#CLI в контейнері
Як заходити в PHP контейнер, щоб не зіпсувати права доступу:

**`docker exec -ti magento2_php su www-data -s /bin/bash`** - за допомогою цієї команди ви відкриєте CLI контейнера і там вже виконувати усі решту маніпуляції
- `magento2_php` - ім'я контейнера PHP (див. секцію `Переглянути активні контейнери`)

#Імпорт бази даних з backup-файлу:
**`cat backup.sql | docker exec -i CONTAINER_NAME /usr/bin/mysql -u ROOT --password=PASSWORD DATABASE`**:
- `backup.sql` - файл для імпорту
- `CONTAINER_NAME` - контейнер з MySQL (по замовчуванню `magento2_mysql`)
- `ROOT` - ім'я користувача MySQL (по замовчуванню `root`)
- `PASSWORD` - пароль користувача MySQL (по замовчуванню `magento2`)
- `DATABASE` - база данних MySQL (по замовчуванню `magento2`)

#Backup (dump) бази у файл:
**`docker exec CONTAINER_NAME /usr/bin/mysqldump -u ROOT --password=PASSWORD DATABASE > backup.sql`**:
- `CONTAINER_NAME` - контейнер з MySQL (по замовчуванню `magento2_mysql`)
- `ROOT` - ім'я користувача MySQL (по замовчуванню `root`)
- `PASSWORD` - пароль користувача MySQL (по замовчуванню `magento2`)
- `DATABASE` - база данних MySQL (по замовчуванню `magento2`)
- `backup.sql` - файл для імпорту

#Встановлення Magento
- за допомогою **`СOMPOSER`**
- за допомогою **`GIT`**