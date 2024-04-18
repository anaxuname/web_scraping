Для того чтобы начать работать с приложением, необходимо скачать и установить его с помощью команды: git clone https://github.com/anaxuname/web_scraping
Далее запустить виртуальное окружение командой: `python -m venv .venv`
Далее необходимо в командной строке перейти в терминал и выполнить команду: `pip install -r requirements.txt`
После установки зависимостей, необходимо в командной строке выполнить команду: `python main.py`
Время обработки данных зависит от количества товаров на странице. На обработку одного продукта вуходит 4 секунды, на обработку одной страницы из 24 продуктов - 120 секунд.