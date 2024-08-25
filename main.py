import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='?', help='Введите url')
    args = parser.parse_args()
    if args.url:
        return args.url
    else:
        return input("Введите URL: ")


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
    token = os.getenv("token")
    if not token:
        print("VK Token is not set. Please check your .env file.")
        return
    url = create_parser()
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
        print("Ошибка индекса:", e)


if __name__ == "__main__":
    main()