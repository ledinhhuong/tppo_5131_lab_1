# tppo_5131 ЛР №1
=============================
### TCP Сервер
В окне терминала:
- Запустить сервера, `python tppo_server_5131.py ip port`

Пример: `python tppo_server_5131.py 127.0.0.1 5000`
### TCP Клиенты
В других окнах терминала:
- Запустить клиенты, `python tppo_client_5131.py IP PORT`
- Установить проценты сдвига полотна пропуска светового потока, `set shaer X` и `set flux X`. Где X = 0 .. 100
- Получить значения процентов сдвига полотна, пропуска светового потока и текущей освещенности с внешней стороны, `get shaer`, `get flux` и `get illumination`

Установить данных вручную в файле устройства `blinds.txt`
