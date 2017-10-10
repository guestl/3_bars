# Ближайшие бары

Скрипт, который рассчитает:

* самый большой бар;
* самый маленький бар;
* самый близкий бар (текущие gps-координаты пользователь вводит с клавиатуры).

На сайте data.mos.ru есть список московских баров. Его можно скачать в формате JSON. Для этого нужно:

зарегистрироваться на сайте и получить ключ API;
скачать файл по ссылке вида https://apidata.mos.ru/v1/features/1796?api_key={place_your_API_key_here}.

# Как запустить

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5

После запуска скрипт попросит ввести свои координаты, чтобы определить ближайший бар. Координаты вводятся в формате 1.2345, 6.7890

Запуск на Linux:

```#!bash

$ python bars.py json_filename
# possibly requires call of python3 executive instead of just python
```

Пример вывода:

```
python bars.py bars.json
Enter your longitude:37.62
Enter your latitude:55.77
Smallest bar is БАР. СОКИ located in Дубравная улица, дом 34/29 and with 0 seats
Biggest bar is Спорт бар «Красная машина» located in Автозаводская улица, дом 23, строение 1 and with 450 seats
Closest bar for user is Бар Виват located in посёлок Ерино, дом 1 and with 35 seats

Запуск на Windows происходит аналогично.
```
# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)


