import requests
import tqdm
from bs4 import BeautifulSoup as BS
from PIL import Image
import os
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
print(r"""
██████╗ ██████╗ ██╗   ██╗███████╗██╗      ██████╗      ██████╗ ██████╗    
██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝██║     ██╔═══██╗    ██╔════╝██╔═══██╗   
██║  ██║██████╔╝ ╚████╔╝ ███████╗██║     ██║   ██║    ██║     ██║   ██║   
██║  ██║██╔══██╗  ╚██╔╝  ╚════██║██║     ██║   ██║    ██║     ██║   ██║   
██████╔╝██║  ██║   ██║   ███████║███████╗╚██████╔╝    ╚██████╗╚██████╔╝██╗
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝ ╚═════╝      ╚═════╝ ╚═════╝ ╚═╝            
                                                    """)
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
def convert_to_jpg(file_path):
    file_name, _ = os.path.splitext(file_path)
    new_file_path = f"{file_name}.jpg"
    with Image.open(file_path) as img:
        img.convert("RGB").save(new_file_path, "JPEG")
    os.remove(file_path)
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }
)
def get(url: str) -> list:
    r = session.get("https://ayaznal.ru" + f"{url}-1-0-0-2-0-0-1", headers=headers)
    res = r.json()
    flag = res[0][0]
    i = 2
    while True:
        r = session.get("https://ayaznal.ru" + f"{url}-{i}-0-0-2-0-0-1", headers=headers)
        res1 = r.json()
        flag1 = res1[0][0]
        if flag1 == flag:
            break
        res.extend(res1)
        i += 1
    res = [x[1] for x in res]
    return res


def get_urls(url: str) -> list:
    try:
        res = []
        r = session.get(url, headers=headers)
        soup = BS(r.content, "html.parser")
        ul = soup.find("ul", attrs={"id": "uEntriesList"})
        for li in ul.find_all("li"):
            link = li.find("a").get("href")
            if "/photo/" in link:
                res.append(link)
        return res
    except:
        print("ERROR get_urls")
        time.sleep(1)
        return get_urls(url)


def dl(url: str):
    filename = url.split("/")[-1]
    try:
        with session.get("https://ayaznal.ru" + url, stream=True,headers=headers) as response:
            response.raise_for_status()
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        convert_to_jpg(filename)
    except requests.exceptions.RequestException as e:
        print("Error downloading the image:", e)

cats = ["https://ayaznal.ru/photo/tiktokershi/66","https://ayaznal.ru/photo/onlifans_sliv/35","https://ayaznal.ru/photo/strimershi/41","https://ayaznal.ru/photo/insta_modeli/77"]
os.mkdir("result")
os.chdir("result")
for cat in cats:
    cat_name = cat.split("/")[-2]
    print(cat_name,end =" ")
    os.mkdir(cat_name)
    os.chdir(cat_name)
    models = get_urls(cat)
    l = len(models)
    print(l)
    for n,model in enumerate(models):
        model_name = model.split("/")[-2]
        print(f"{n+1}/{l}",model_name)
        os.mkdir(model_name)
        os.chdir(model_name)
        photos = get(model)
        for photo in tqdm.tqdm(photos,colour="GREEN"):
            dl(photo)
        os.chdir("..")
    os.chdir("..")
