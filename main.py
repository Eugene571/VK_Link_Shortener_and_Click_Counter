import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    url_method = "https://api.vk.com/method/utils.getShortLink"
    params = {"access_token": token, "v": "5.199", "url": url}
    response = requests.get(url_method, params=params)
    response.raise_for_status()
    json_response = response.json()
    short_link = json_response['response']['short_url']
    return short_link


def is_shorten_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "vk.cc"


def count_clicks(token, url):
    url_method = "https://api.vk.com/method/utils.getLinkStats"
    parsed_url = urlparse(url)
    key = parsed_url.path.replace("/", "")
    params = {
        "access_token": token,
        "v": "5.199",
        "key": key,
        "interval": "forever"
    }
    response = requests.get(url_method, params=params)
    response.raise_for_status()
    json_response = response.json()
    count_click = json_response['response']['stats'][0]['views']
    return count_click


def main():
    load_dotenv()
    token = os.environ["VK_TOKEN"]
    parser = argparse.ArgumentParser(description='Сокращение ссылок и просмотр статистики кликов по коротким ссылкам.')
    parser.add_argument('url', type=str, nargs='?', help='URL для сокращения или проверки статистики')
    args = parser.parse_args()
    url = args.url
    if url is None:
        url = input('Введите URL: ')

    try:
        if is_shorten_link(url):
            print("Кол-во кликов:", count_clicks(token, url))
        else:
            print("Сокращенная ссылка:", shorten_link(token, url))
    except requests.exceptions.HTTPError as e:
        print("Ошибка HTTP:", e)
    except KeyError as e:
        print("Ошибка ключа:", e)
    except IndexError as e:
        print(f"Ошибка индекса: {e} \nВозможно ссылка не была использована или отсутствуют данные по кликам")


if __name__ == "__main__":
    main()
