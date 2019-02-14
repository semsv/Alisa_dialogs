# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import requests

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
application = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Флаг что выбран язык с которого мы делаем перевод
select_lang = '0'

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@application.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']    
	
    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Английский",
                "Французкий",
                "Немецкий",
                "другой",
            ]
        }

        res['response']['text'] = 'Выберите язык с которого необходимо перевести?'
        res['response']['buttons'] = get_suggests(user_id)
        return
    
	# Если пользователь уже выбрал язык с которого необходимо сделать перевод
	if select_lang in ['1']:
	    res['response']['text'] = requests.get('https://translate.yandex.ru/?utm_source=wizard&lang=en-ru&text="%s"' % (
		    req['request']['original_utterance'].lower()
		)).text
	    return
		
    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'английский',
        'французкий',
        'немецкий',
        'другой',
    ]:
        # Пользователь сделал выбор.
        res['response']['text'] = 'Cкажите фразу или слово!'
        select_lang = '1'
        return  	

    # Если нет, то сообщаем ему об этом!
    res['response']['text'] = 'Другие языки "%s", пока не поддерживаются!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выводим все подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:4]
    ]
    
    return suggests
