import time
import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Process


url_site = 'https://www.sew-world.ru'
# url = 'https://dzen.ru/?yredirect=true&clid=2270456&win=462'
# url = 'https://you-anime.ru'

headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 YaBrowser/23.7.0.2526 Yowser/2.5 Safari/537.36"
}


def write_html(url_site, headers):
    req = requests.get(url_site, headers)
    src = req.text
    with open("index.html", "w", encoding='utf-8') as f:
        f.write(src)
    soup = BS(src, "html.parser")
    return soup


def get_img_url_mass(url_site, headers):
    all_img = write_html(url_site, headers).find_all("img")
    img_url_mass = []
    for item in all_img:
        img_url_mass.append(url_site + item["src"])
    return img_url_mass


urls = get_img_url_mass(url_site, headers)
start_time = time.time()


# синхронная запись
def process_recording(url):
        response = requests.get(url)
        filename = 'process_images/' + "".join(url.replace('https://', '').split("/")[4:5])
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


processes = []

if __name__ == '__main__':
    for url in urls[1:6]:
        process = Process(target=process_recording, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

