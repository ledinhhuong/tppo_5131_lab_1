# tppo_5131 ЛР №1
=============================
### TCP Сервер
В окне терминала:
- Запустить сервера, `python tppo_server_5131.py ip port`. Где ip: адрес, port: порт

Пример: `python tppo_server_5131.py 127.0.0.1 5000`
### TCP Клиенты
В других окнах терминала:
- Запустить клиенты, `python tppo_client_5131.py ip port`. Где ip: адрес, port: порт
- Установить проценты сдвига полотна пропуска светового потока, `set shaer X` и `set flux X`. Где X = 0 .. 100
- Получить значения процентов сдвига полотна, пропуска светового потока и текущей освещенности с внешней стороны, `get shaer`, `get flux` и `get illumination`

Пример: `python tppo_client_5131.py 127.0.0.1 5000`, `set shaer 52`, `get flux`

Установить данных вручную в файле устройства `blinds.txt`
