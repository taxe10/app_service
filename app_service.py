import logging
from fastapi import FastAPI
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


@app.post(URL_PREFIX + '/file_service', tags=['applications'])
def full_service(filename: str):
    # Load local file
    f = open(filename, "r")
    contents = f.read().splitlines()  # each line as an element in a list
    logger.info(f'Received: {contents}')
    # Start pipeline
    output_app1 = subprocess.check_output(f'python3 app1.py \"{contents[0]}\"', shell=True).decode()
    logger.info(f'Output of APP1: {output_app1}')
    output_app2 = subprocess.check_output(f'python3 app2.py \"{output_app1}\"', shell=True).decode()
    logger.info(f'Output of APP2: {output_app2}')
    output_app3 = subprocess.check_output(f'python3 app3.py \"{output_app2}\"', shell=True).decode()
    logger.info(f'Output saved locally as {output_app3}')
    return output_app3


@app.post(URL_PREFIX + '/alt_service', tags=['applications'])
def alt_service(fcontents: str):
    # Start pipeline
    output_app1 = subprocess.check_output(f'python3 app1.py \"{fcontents}\"', shell=True).decode()
    logger.info(f'Output of APP1: {output_app1}')
    output_app2 = subprocess.check_output(f'python3 app2.py \"{output_app1}\"', shell=True).decode()
    logger.info(f'Output of APP2: {output_app2}')
    out = f'Output of APP1: {output_app1}\nOutput of APP2: {output_app2}'
    return out

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
