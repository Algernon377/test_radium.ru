import requests

import time
import re
import json
import hashlib
import os
import asyncio


async def load_header_async(link: str, directory: str):
    """
    Makes a request to the address (link=str) ,
    takes everything in the <head> tag from the received response and
    saves it in the directory (directory=str)
    """
    req = await asyncio.get_event_loop().run_in_executor(None, requests.get, link)
    if not req.status_code:
        print(f'Ошибка сервера. ошибка:{req.status_code}')
        raise ValueError('Сервер не отвечает, проверьте правильность введенного url')
    data_header = re.search(r'(?<=<head>)(.*)(?=</head>)', req.text, re.DOTALL)[0]
    with open(f'{directory}/file{time.time() % 1}.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_header, json_file)
    req.close()


async def run_async(num_of_req: int, link: str, directory: str):
    """
    Makes a certain number of requests (num_of_req=int)
    to the address (link=str) and
    saves to the directory (directory=str)
    """
    tasks = []
    for _ in range(num_of_req):
        task = asyncio.create_task(load_header_async(link, directory))
        tasks.append(task)
    await asyncio.gather(*tasks)


def make_hash(directory: str):
    hash_list = []
    for _ in os.listdir(f'{directory}'):
        with open(f'{directory}/{_}', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            hash_object = hashlib.sha256(json.dumps(json_data).encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            hash_list.append(hex_dig)
    return hash_list


link = 'https://gitea.radium.group/radium/project-configuration'
directory = os.path.join(os.getcwd(), "save_headers")
num_of_req = 3

if __name__ == '__main__':
    asyncio.run(run_async(num_of_req, link, directory))
    all_hash = make_hash(directory)
    print(all_hash)
