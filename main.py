import requests
import os
import argparse
from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser(description='''
Создание короткой ссылки bitly для Вашего адреса, либо вывод количества переходов,
если в качестве параметра указана bitly-ссылка 
    	''')
    parser.add_argument ('link', help='Введите Вашу ссылку или bitly-ссылку')
 
    return parser


def get_bitly_link(token, long_url):
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
    'Authorization': 'Bearer '+token,
    }
    params = {
    'long_url': long_url,
    }
    response = requests.post(api_url, headers=headers, json=params)
    if response.ok:
        return response.json()['link']


def get_bitly_summary(token, link):
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks'+link[6:]+'/clicks/summary'
    headers = {
    'Authorization': 'Bearer '+token,
    }
    params = {
    'unit': 'day',
    'units': -1,
    }
    response = requests.get(api_url, headers=headers, json=params)
    if response.ok:
        return response.json()['total_clicks']


def check_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        long_url = url
    else:
        long_url = 'http://'+ url
    try:
        response = requests.get(long_url)
        if response.ok:
            return long_url
    except:
        pass


def get_bitly(token, link):
    result = get_bitly_summary(token, link)

    if result is None:
        print('Короткая ссылка для Вашего url: ', get_bitly_link(token, link))
    else:
        print('Количество переходов по ссылке bitly: ', result)


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN')

    parser = create_parser()
    namespace = parser.parse_args()

    link = check_url(namespace.link)
    if link is None:
    	print('Ошибка ввода ссылки')
    else:
    	get_bitly(token, link)