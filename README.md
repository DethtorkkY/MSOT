<div align="center">

# Код для запуска Майнкрафт сервера Bedrock Edition через бота в телеграмме
</div>
<div align="center">
  
## Комманды для управления (Писать в Темримале)
</div>

<div align="center">

### Обновление сервера до последней версии
</div>
python main.py update

<div align="center">

### Запуск сервера
</div>
python main.py start

<div align="center">

### Остановка сервера
</div>
python main.py stop

<div align="center">

### Отправка команды на сервер
</div>
python main.py command --cmd "Комманда пишется здесь"

<div align="center">

### Создание резервной копии сервера
</div>
python main.py backup

<div align="center">

### Экспорт данных сервера
</div>
python main.py export

<div align="center">

### Управление белым списком (добавление пользователя)
</div>
python main.py whitelist --username "Ник Игрока"

<div align="center">

### Назначение привилегированного пользователя
</div>
python main.py privilege --username "Ник Игрока"

<div align="center">

### Мониторинг состояния сервера
</div>
python main.py monitor

<div align="center">

### Отправка сообщения на сервер
</div>
python main.py notify --message "Сообщение которое хотите отправить"

<div align="center">

### Добавление модификации на сервер
</div>
python main.py addmod --file "Путь к аддону"

<div align="center">

### Установка ресурс пака
</div>
python main.py setpack --file "Путь к ресурс паку"