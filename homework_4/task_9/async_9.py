import asyncio
import aiohttp
import time
import requests
from bs4 import BeautifulSoup as BS


url_site = 'https://www.sew-world.ru'


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


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            cont = await response.read()
            filename = 'async_images/' + "".join(url.replace('https://', '').split("/")[4:5])
            with open(filename, "wb") as f:
                f.write(cont)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


async def main():
    tasks = []
    for url in urls[1:6]:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

