import logging
from fastapi import FastAPI
import requests
import subprocess
import uvicorn


# logging
logger = logging.getLogger('app_service')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel('INFO')

# url definition
URL_PREFIX = "/api/v0"
app = FastAPI(openapi_url='/api/app_service/openapi.json',
              docs_url='/api/app_service/docs',
              redoc_url='/api/app_service/redoc')


@app.post(URL_PREFIX + '/reverse', tags=['applications'])
def reverse_message(message: str):
    rev_msg = subprocess.check_output(f'python3 app1.py \"{message}\"', shell=True).decode()
    logger.info(f'Output of APP1: {rev_msg}')
    return rev_msg


@app.post(URL_PREFIX + '/convert', tags=['applications'])
def convert_message(message: str):
    conv_msg = subprocess.check_output(f'python3 app2.py \"{message}\"', shell=True).decode()
    logger.info(f'Output of APP2: {conv_msg}')
    return conv_msg


@app.post(URL_PREFIX + '/save', tags=['applications'])
def save_message(message: str):
    out = subprocess.check_output(f'python3 app3.py \"{message}\"', shell=True).decode()
    logger.info(f'Output of APP3: {out}')
    return out


@app.post(URL_PREFIX + '/file_service', tags=['applications'])
def file_service(filename: str):
    # Load local file
    f = open(filename, "r")
    contents = f.read().splitlines()  # each line as an element in a list
    logger.info(f'Received: {contents}')
    out1 = requests.post(f'http://localhost:8080{URL_PREFIX}/reverse?message={contents[0]}').json()
    out2 = requests.post(f'http://localhost:8080{URL_PREFIX}/convert?message={out1}').json()
    out3 = requests.post(f'http://localhost:8080{URL_PREFIX}/save?message={out2}').json()
    return out3


@app.post(URL_PREFIX + '/alt_service', tags=['applications'])
def online_service(fcontents: str):
    logger.info(f'Received: {fcontents}')
    out1 = requests.post(f'http://localhost:8080{URL_PREFIX}/reverse?message={fcontents}').json()
    out2 = requests.post(f'http://localhost:8080{URL_PREFIX}/convert?message={out1}').json()
    out3 = requests.post(f'http://localhost:8080{URL_PREFIX}/save?message={out2}').json()
    return out3


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
