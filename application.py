# coding: utf-8
# ����������� ��������� UTF-8.
from __future__ import unicode_literals

# ����������� ������ ��� ������ � JSON � ������.
import json
import logging
import requests

# ����������� ��������� Flask ��� ������� ���-�������.
from flask import Flask, request
application = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# ���� ��� ������ ���� � �������� �� ������ �������
select_lang = '0'

# ��������� ������ � �������.
sessionStorage = {}

# ������ ��������� ���������� Flask.
@application.route("/", methods=['POST'])

def main():
# ������� �������� ���� ������� � ���������� �����.
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

# ������� ��� ���������������� ��������� �������.
def handle_dialog(req, res):
    user_id = req['session']['user_id']    
	
    if req['session']['new']:
        # ��� ����� ������������.
        # �������������� ������ � �������������� ���.

        sessionStorage[user_id] = {
            'suggests': [
                "����������",
                "����������",
                "��������",
				"������",
            ]
        }

        res['response']['text'] = '�������� ���� � �������� ���������� ���������?'
        res['response']['buttons'] = get_suggests(user_id)
        return
    
	# ���� ������������ ��� ������ ���� � �������� ���������� ������� �������
	if select_lang in ['1']:
	    res['response']['text'] = requests.get('https://translate.yandex.ru/?utm_source=wizard&lang=en-ru&text="%s"' % (
		    req['request']['original_utterance'].lower()
		)).text
	    return
		
    # ������������ ����� ������������.
    if req['request']['original_utterance'].lower() in [
        '����������',
        '����������',
        '��������',
        '������',
    ]:
        # ������������ ������ �����.
        res['response']['text'] = 'C������ ����� ��� �����!'
        select_lang = '1'
        return  	

    # ���� ���, �� �������� ��� �� ����!
    res['response']['text'] = '������ ����� "%s", ���� �� ��������������!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

# ������� ���������� ��� ��������� ��� ������.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # ������� ��� ��������� �� �������.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:4]
    ]
    
    return suggests
