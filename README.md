Magento 2 Docker
================

Що нового?
----------
- **Fast Reverse Proxy** - аналог **Ngrok** - утиліта яка дозволяє налаштувати доступ до вашого локального проекту з мережі Інтернет, корисно коли потрібно взаємодіяти з сервісами, котрі просять публічний URL вашого сайту.
- **PHP Profiler** та **Magento Profiler** - тепер вмикаються однією кнопкою, що дозволяє максимально швидко знайти слабкі місця в коді, без використання стороннього ПО (Blackfire, New Relic, ..)
- **Varnish** - встановлено Varnish, керування через плагін Xdebug, що дозволяє вмикати його у разі потреби, без перезавантажень контейнера

Magento2 Helper
---------------
Хочу запропонувати вам також використовувати додатковий інструмент для пришвидшення взаємодії з контейнерами та `bin/magento` - [magento2-helper](https://github.pp.ua/anbis/magento2-helper)

Зміст
-----
- [Troubleshooting](#troubleshooting)
- [Varnish](#varnish)
- [Profiler](#profiler)
- [Fast Reverse Proxy](#fast-reverse-proxy)
- [Plugin Xdebug](#plugin-xdebug)
- [Підготовка та встановлення необхідних інструментів](#підготовка-та-встановлення-необхідних-інструментів)
- [Реєстр (pre-build) PHP імеджів](#реєстр-pre-build-php-імеджів)
- [E-MAIL](#e-mail)
- [Домени та SSL](#домени-та-ssl)
- [SSL сертифікати](#ssl-сертифікати)
- [Переглянути активні контейнери](#переглянути-активні-контейнери)
- [CLI в контейнері](#cli-в-контейнері)
- [Використання Docker-compose](#використання-docker-compose)
- [Завантаження Magento](#завантаження-magento)
- [Права доступу до директорій](#права-доступу-до-директорій)
- [Встановлення Magento](#встановлення-magento)
- [Використання контейнера для існуючого проекту Magento](#використання-контейнера-для-існуючого-проекту-magento)
- [Імпорт бази даних з backup-файлу](#імпорт-бази-даних-з-backup-файлу)
- [Backup (dump) бази у файл](#backup-dump-бази-у-файл)
- [Видалити DEFINER з dump файлу](#видалити-definer-з-dump-файлу)
- [Налаштування Xdebug для CLI](#налаштування-xdebug-для-cli)
- [Встановлення додаткових бібліотек та розширень в Dockerfile](#встановлення-додаткових-бібліотек-та-розширень-в-dockerfile)

Varnish
-------
Для початку роботи з Varnish, необхідно лише перемкнути режим плагіна у наступне положення:
- ![](https://i.imgur.com/lKfSVAi.png)

Трохи не логічно і не для того ця кнопка існує, але поки це найзручніший спосіб.

Виконати у терміналі в контейнері з PHP:
- `bin/magento config:set --scope=default --scope-code=0 system/full_page_cache/caching_application 2`

Додаткові налаштування в Admin Dashboard (Stores > Settings > Configuration > Advanced > System > Full Page Cache)

Profiler
--------

Для роботи з профайлером необхідно:
- Включити відповідний режим на плагіні
- ![](https://i.imgur.com/1rMBfBk.png)
- перезавантажити сторінку
- з самого низу сторінки, під футером, буде таблиця репорту роботи профайлера від Magento 2
- ![](https://i.imgur.com/XvsnUMO.png)
- репорт з роботою профайлера від PHP знаходиться у директорії `logs/profiler/cachegrind....`
- ![](https://i.imgur.com/KysSgzg.png)
- відкрити цей файл потрібно за добомогою інструменту PhpStorm
- ![](https://i.imgur.com/vzGuYcA.png)
- ![](https://i.imgur.com/aGesytL.png)

Fast Reverse Proxy
------------------
**_УВАГА_: Ще не реалізована підтримка SSL**, тобто `base_url` повинен починатись з `http://`, а НЕ з `httpS://`

Для проксювання вашого локального середовища у Інтернет необхідно лише вибрати домен, який будете використовувати і вказати його у налаштуваннях:
- ![](https://i.imgur.com/QpX227V.png)
- тут для прикладу вибрано `magento2.ukranian.pp.ua`, але рекомендую вибрати щось своє для власного використання, єдина умова - закінчуватись хост повинен на `.ukranian.pp.ua`
- тобто любі комбінації виду `XXX.ukranian.pp.ua`:
  - `super.ukranian.pp.ua` 
  - `my.favoryte.site.ukranian.pp.ua`
  - `varuk.ukranian.pp.ua`
- після зміни значення потрібно перепідняти контейнери командою `docker-compose stop` та `docker-compose up`
- потрібно вимкнути модуль `Magento_Csp`
- виконати команду `bin/magento config:set --scope=default --scope-code=0 web/url/redirect_to_base 0`
- перевірити роботу
  - ![](https://i.imgur.com/0MPxaX6.png)

Troubleshooting
---------------

- **Xdebug не працює на MacOS** - перевірте значення змінної `xdebug.remote_connect_back` у файлі `config/php/php.ini`, воно має бути рівним `0` або `Off`

- **docker-compose не оновлюється** - при встановленні через `pip install docker-compose` встановлення відбувається в директорію `~/.local/bin/docker-compose`, тоді як правильне місце буде `/usr/local/bin/docker-compose`. 
Необхідно деінсталювати `pip uninstall docker-compose`
- **invalid port in upstream "${PHP_HOST_XDEBUG}** - оновити локальні імеджі контейнерів, виконайте команду `docker-compose pull`
- **Configuration for volume code specifies "mountpoint" driver_opt...** - оновити `docker-compose`, `sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

Plugin Xdebug
-------------
*__Примітка__: Для виконання команд `composer` або роботи з `bin/magento` використовуйте контейнер `magento2_php`, а не `magento2_php_xdebug`, це пришвидшить роботу.*

Для **Xdebug** потрібно встановити плагін **Xdebug helper**, який допомагає швидко вмикати та вимикати дебагер.
- **Chrome** -  [Xdebug Helper](https://chrome.google.com/webstore/detail/xdebug-helper/eadndfjplgieldjbigjakmdgkmoaaaoc?hl=en-US)
- **Firefox** - [Xdebug Helper](https://addons.mozilla.org/en-US/firefox/addon/xdebug-helper-for-firefox/)

Підготовка та встановлення необхідних інструментів
--------------------------------------------------
### Linux
*__Примітка__: Перевірено на __Ubuntu__ та __Manjaro__ дистрибутивах, також буде працювати на усіх похідних від __Debian__ та __Arch__.*

Для роботи необхідно встановити офіційний плагін для Docker - [local-persist](https://github.com/MatchbookLab/local-persist) за допомогою команди:
`curl -fsSL https://raw.githubusercontent.com/MatchbookLab/local-persist/master/scripts/install.sh | sudo bash`

Необхідно оновити програму `docker-compose` на найновішу версію, на момент написання інструкції це **1.29.2**, для цього виконайте команди:
- `sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
- `sudo chmod +x /usr/local/bin/docker-compose`

Перевірити свою версію програми `docker-compose` можна за допомогою команди `docker-compose --version`

**Важливо оновити локальні імеджі** контейнерів, так як вони кешуються, і можуть виникати помилки при старті проекту. 
Для повторного завантаження імеджів з хмари виконайте команду `docker-compose pull` у директорії з проектом.

### MacOS
*__Примітка__: Гілка зі __збіркою для MacOS__ знаходиться у відповідній гілці репозиторію*

Для роботи потрібно встановити **Homebrew** та **Mutagen (beta)**:
- **Homebrew** - `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`
- **Mutagen** - `brew install mutagen-io/mutagen/mutagen-beta`
- Запустити **службу Mutagen** - `mutagen daemon start`

Для роботи з Mutagen необхідно усі команди для роботи з контейнерами змінити з `docker-compose ...` на `mutagen compose ... (up, down, start, down, rm ...)`

**Mutagen** - це програма, яка дозволяє робити синхронізацію файлів між локальною файловою системою (ФС) і ФС контейнера без втрати продуктивності.

Для того, щоб перевірити статус виконання синхронізації можна ввести команду `mutagen sync monitor`

**Важливо оновити локальні імеджі** контейнері, так як вони кешуються, і можуть виникати помилки при старті проекту.
Для повторного завантаження імеджів з хмари виконайте команду `docker compose pull` у директорії з проектом.

**При виникненні помилок з не існуючим класом, або ж не можливістю створення файлу - потрібно виконати команду у контейнері PHP `chmod -R 777 app/etc/ pub/static pub/media/ var/ generated/`** 

У випадку якщо **Xdebug** не працює, перевірте значення змінної `xdebug.remote_connect_back` у файлі `config/php/php.ini`, воно має бути рівним `0` або `Off`

Реєстр (pre-build) PHP імеджів
--------------------------------------
Всі доступні версії PHP контейнерів доступні за посиланням: [`https://web.docker.pp.ua/#!taglist/magento2-php`](https://web.docker.pp.ua/#!taglist/magento2-php)

*__Примітка__: також можете переглянути репозиторій за посиланням [https://web.docker.pp.ua/](https://web.docker.pp.ua/)*

E-MAIL
------
Для листів встановлена локальна заглушка, яка не дозволить відправити лист на реальну поштову скриньку, а лише збереже його локально для перегляду.

Переглянути всі отримані листи можна за посиланням: [`http://localhost:8025/`](http://localhost:8025/)

![](https://i.imgur.com/GaarM5O.png)

Домени та SSL
--------------------------
*__Примітка__: виконуємо у локальному терміналі*

При запуску **`docker-compose up`** будуть створені усі необхідні сертифікати, відповідно до параметра `DOMAINS`, який знаходиться у файлі `env/nginx.env`:
- ![](https://i.imgur.com/u63mm2k.png)
- ![](https://i.imgur.com/OyIW6X8.png)
- додати домени до файлу `/etc/hosts`, наприклад `0.0.0.0 magento2.local magento2.test magento2.dev`

### Додаткові домени
Наприклад потрібно мати окремий домен для кожної мови, яка використовується на сайті.

Для цього необхідно налаштувати `base_url` стору (вебсайту) на окремий домен. Це можуть бути як зовсім різні URL, так і зі спільним доменом другого рівня.

**_Наприклад_**: 
- `store1` - `superdeal.com`
- `store2` - `special.org.eu`

У такому випадку параметр `DOMAINS` буде мати вигляд `DOMAINS=superdeal.com=store1 special.org.eu=store2`

Або для різних мов:
- `en_store` - `global.superdeal.com`
- `uk_store` - `uk.superdeal.com`
- `fr_store` - `fr.superdeal.com`

`DOMAINS` буде мати вигляд `DOMAINS=global.superdeal.com=en_store uk.superdeal.com=uk_store fr.superdeal.com=fr_store`

Тобто для додавання нових доменів потрібно всього лиш додати нову пару значень `{url}={code}`, де:
- `{url}` - це хост для браузера
- `{code}` - це код стора або вебсайту, залежить від значення параметру `MAGE_RUN_TYPE` (`env/nginx.env`)

**_Не забудьте додати нові домени до `/etc/hosts` файлу на налаштувати `base_url` відповідним чином!_**

SSL сертифікати
-----------------------------------------

Для коректної роботи SSL необхідно імпортувати кореневий (CA) сертифікат в браузер, для того щоб браузер міг довіряти самопідписаним сертифікатам:
- Chrome - Settings - [Privacy and security] Security - [Advanced] Manage certificates - Authorities
- натиснути кнопку Import
- ![](https://i.imgur.com/BjtlZ9X.png)
- перейти у директорію з проектом `docker-magento2/ssl/ssl_generator`
- змінити фільтр на `All Files`
- ![](https://i.imgur.com/jsJOSJR.png)
- вибрати файл `rootCA.crt`
- відмітити 3 чекбокси і натиснути ОК
- ![](https://i.imgur.com/hjMKC8T.png)
- додати `0.0.0.0 sample.test` до `/etc/hosts` файлу
- готово
  - ![](https://i.imgur.com/mBxnMks.png)

Переглянути активні контейнери
------------------------------
*__Примітка__: виконуємо у локальному терміналі*

Команда **`docker ps`**

![](https://i.imgur.com/l5WV11H.png)

- `CONTAINER ID` - ID контейнера
- `IMAGE` - образ контейнера на якому він працює
- `COMMAND` - головна команда контейнера (задається при створенні в `Dockerfile`)
- `CREATED` - дата створення
- `STATUS` - час роботи від старту
- `PORTS` - показує як локальний (доступний на ПК) порт співвідноситься до порту в контейнері Docker
- `NAMES` - ім'я контейнера - використовується у командах по роботі з контейнером

CLI в контейнері
----------------
Як заходити в PHP контейнер, щоб не зіпсувати права доступу:

**`docker exec -ti magento2_php su www-data -s /bin/bash`** - за допомогою цієї команди ви відкриєте CLI контейнера і там вже виконувати усі решту маніпуляції
- `magento2_php` - ім'я контейнера PHP (див. секцію [`Переглянути активні контейнери`](#переглянути-активні-контейнери))

Використання Docker-compose
---------------------------
*__Примітка__: виконуємо у локальному терміналі*

- Клонуємо GIT-репозиторій на локальний комп'ютер: **`git clone https://github.pp.ua/anbis/docker-magento2.git`**
- Переходимо у директорію, яка була створена у попередньому пункті **`cd docker-magento2`**
- Запускаємо контейнери **`docker-compose up`**
- Перевіряємо статус контейнерів **`docker ps`** (у новому вікні терміналу): 
    - має бути активно декілька контейнерів (`nginx`, `php`, `mysql`, `mailhog`, `redis`, `elasticsearch`...)
    - ![](https://i.imgur.com/sJxjcgs.png)
- переходимо в контейнер PHP **`docker exec -ti magento2_php bash`**

Завантаження Magento
--------------------
*__Примітка__: виконуємо у контейнері PHP*

- за допомогою **`СOMPOSER`**
    - **`composer create-project --repository-url=https://repo.magento.com/ magento/project-community-edition`** - завантажуємо файли за допомогою Composer
    - **`mv project-community-edition/{*,.*} .`** - переміщуємо файли на рівень нижче (можуть бути повідомлення про помилку - ігноруємо)
    - **`rm -rf project-community-edition`** - видаляємо директорію, вона нам більше не потрібна
    - **`chown -R www-data:www-data .`** - змінюємо права доступу після завантаження на коректні
    - **`exit`** - виходимо з терміналу контейнера
    
- за допомогою **`GIT`**
    - to be continued...
    
Права доступу до директорій
---------------------------
*__Примітка__: виконуємо у локальному терміналі*

Для правильної роботи Magento необхідно надати право на запис у наступні директорії:
- `var`
- `app/etc`
- `pub/media`
- `pub/static`

Для цього необхідно виконати команду (знаходитись у директорії проекту):
- **`chmod -R 777 app/etc/ pub/static pub/media/ var/ generated/` в контейнері PHP**
- **`sudo chown -R $USER:$USER code` в локальному терміналі**

Встановлення Magento
--------------------
*__Примітка__: виконуємо у контейнері PHP*

- **`bin/magento`** - перевіряємо чи працює консоль Magento
- ![](https://i.imgur.com/jVwRPRS.png)
- **`bin/magento setup:install --db-host=magento2_mysql --db-name=magento2 --db-user=magento2 --db-password=magento2 --search-engine=elasticsearch6 --elasticsearch-host=http://magento2_elasticsearch:9200 --elasticsearch-port=9200 --elasticsearch-enable-auth=0 --session-save=redis --session-save-redis-host=magento2_redis --session-save-redis-port=6379 --session-save-redis-db=1 --cache-backend=redis --cache-backend-redis-server=magento2_redis --cache-backend-redis-port=6379 --cache-backend-redis-db=2 --admin-user=anbis --admin-password=magent0 --admin-email=test@example.com --admin-firstname=name --admin-lastname=surname --base-url=https://magento2.dev/ --backend-frontname=admin --language=en_US --currency=USD --timezone=America/Chicago --cleanup-database --use-rewrites=1`**
    - `db-host=magento2_mysql` - хост бази даних (БД)
    - `db-user=magento2` - користувач БД
    - `db-password=magento2` - пароль користувача БД
    - `db-name=magento2` - назва БД
    - `search-engine=elasticsearch6` - використовувати пошуковий сервер ElasticSearch6
    - `elasticsearch-host=http://magento2_elasticsearch:9200` - хост ElasticSearch
    - `elasticsearch-port=9200` - порт ElasticSearch
    - `elasticsearch-enable-auth=0` - не використовувати аутентифікацію ElasticSearch
    - `session-save=redis` - використовувати Redis для зберігання сесій
    - `session-save-redis-host=magento2_redis` - хост Redis
    - `session-save-redis-port=6379` - порт Redis
    - `session-save-redis-db=1` - БД Redis
    - `cache-backend=redis` - використовувати Redis для зберігання кешу
    - `cache-backend-redis-server=magento2_redis` - хост Redis
    - `cache-backend-redis-port=6379` - порт Redis
    - `cache-backend-redis-db=2` - БД Redis
    - `admin-user=anbis` - користувач для адмін-панелі
    - `admin-password=magent0` - пароль користувача адмін-панелі
    - `admin-email=test@example.com` - email користувача адмін-панелі
    - `admin-firstname=name` - ім'я користувача адмін-панелі
    - `admin-lastname=surname` - прізвище користувача адмін-панелі
    - `base-url=https://magento2.dev/` - URL для доступу Magento з браузера (`magento2.dev`, `magento2.local`, `magento2.test`)
    - `backend-frontname=admin` - URL-постфікс для доступу в адмін-панель
    - `language=en_US` - локаль магазину
    - `currency=USD` - валюта магазину
    - `timezone=America/Chicago` - часова зона магазину
    - `cleanup-database` - очистити базу перед встановленням Magento
    - `use-rewrites=1` - використовувати SEO-friendly URL для категорій і продуктів
- ![](https://i.imgur.com/JrApk26.png)
    
- перейти по URL, який був вказаний в параметрі `base-url` ([`https://magento2.dev/`](https://magento2.dev/))
- ![](https://i.imgur.com/RFHAAvK.png)

Використання контейнера для існуючого проекту Magento
-----------------------------------------------------
*__Примітка__: виконуємо у контейнері PHP*

- створити директорію `code` у директорії з проектом
- копіювати або перенести усі файли Magento у директорію `code`
- імортувати БД з файлу
- перевірити коректні налаштування файлу `app/etc/env.php` (файл-примірник `env.php.example`)
- якщо директорія `vendor` порожня - виконати в команду **`composer install`**
- за необхідності встановити коректні права доступу до директорій
- виконати **`bin/magento setup:upgrade`**
- **`bin/magento setup:store-config:set --base-url="http://magento2.dev/"`**
- **`bin/magento setup:store-config:set --base-url-secure="https://magento2.dev/"`**
- **`bin/magento cache:flush`**
- додати `0.0.0.0 magento2.dev` до `/etc/hosts` файлу
    
Імпорт бази даних з backup-файлу
--------------------------------
*__Примітка__: виконуємо у локальному терміналі*

**`cat backup.sql | docker exec -i CONTAINER_NAME /usr/bin/mysql -u ROOT --password=PASSWORD DATABASE`**:
- `backup.sql` - файл для імпорту
- `CONTAINER_NAME` - контейнер з MySQL (по замовчуванню `magento2_mysql`)
- `ROOT` - ім'я користувача MySQL (по замовчуванню `root`)
- `PASSWORD` - пароль користувача MySQL (по замовчуванню `magento2`)
- `DATABASE` - база данних MySQL (по замовчуванню `magento2`)

Backup (dump) бази у файл
-------------------------
*__Примітка__: виконуємо у локальному терміналі*

**`docker exec CONTAINER_NAME /usr/bin/mysqldump -u ROOT --password=PASSWORD DATABASE > backup.sql`**:
- `CONTAINER_NAME` - контейнер з MySQL (по замовчуванню `magento2_mysql`)
- `ROOT` - ім'я користувача MySQL (по замовчуванню `root`)
- `PASSWORD` - пароль користувача MySQL (по замовчуванню `magento2`)
- `DATABASE` - база данних MySQL (по замовчуванню `magento2`)
- `backup.sql` - файл для імпорту

Видалити DEFINER з dump файлу
-----------------------------
*__Примітка__: виконуємо у локальному терміналі*

**`cat backup_WITH_definers.sql | sed -e 's/DEFINER[ ]*=[ ]*[^*]*\*/\*/' > backup_WITHOUT_definers.sql`**
- `backup_WITH_definers` - файл з дефайнерами
- `backup_WITHOUT_definers` - файл для імпорту, який вже не містить дефайнерів

Встановлення додаткових бібліотек та розширень в Dockerfile
-------------------------------------------------------
*__Примітка__: виконуємо у локальному терміналі*

- закоментувати стрічку з `image: docker.pp.ua/magento2-....`
- розкоментувати стрічку з `build: ./builds-custom/....`
- ![](https://i.imgur.com/psoVNUF.png)
- відкрити та редагувати `Dockerfile` файл у директорії `builds-custom` і відповідний імедж (наприклад `php` - `builds-custom/php/Dockerfile`)
- ![](https://i.imgur.com/pvD4EK3.png)
- **`docker-compose stop`**
- **`docker-compose up --force-recreate --build`**
