"""
Написать программу, которая скачивает изображения с заданных URL-адресов и
сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
файле, название которого соответствует названию изображения в URL-адресе.
� Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
image1.jpg
� Программа должна использовать многопоточный, многопроцессорный и
асинхронный подходы.
� Программа должна иметь возможность задавать список URL-адресов через
аргументы командной строки.
� Программа должна выводить в консоль информацию о времени скачивания
каждого изображения и общем времени выполнения программы.
"""
import requests
from bs4 import BeautifulSoup as BS
import time

url = 'https://www.sew-world.ru'
# url = 'https://dzen.ru/?yredirect=true&clid=2270456&win=462'
# url = 'https://you-anime.ru'

headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 YaBrowser/23.7.0.2526 Yowser/2.5 Safari/537.36"
}


def write_html(url, headers):
    req = requests.get(url, headers)
    src = req.text
    with open("index.html", "w", encoding='utf-8') as f:
        f.write(src)
    soup = BS(src, "html.parser")
    return soup


def get_img_url_mass(url, headers):
    all_img = write_html(url, headers).find_all("img")
    img_url_mass = []
    for item in all_img:
        img_url_mass.append(url + item["src"])
    return img_url_mass


urls = get_img_url_mass(url, headers)
start_time = time.time()


# синхронная запись
def synchronous_recording(urls):
    for url in urls[1:6]:
        response = requests.get(url)
        filename = 'sync_images/' + "".join(url.replace('https://', '').split("/")[4:5])
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


if __name__ == '__main__':
    synchronous_recording(urls)
