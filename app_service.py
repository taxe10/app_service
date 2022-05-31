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


@app.post(URL_PREFIX + '/reverse', tags=['applications'])
def reverse_message(message: str):
    '''
    This call reverses a given message
    Args:
        message:    [str] message to reverse
    Output:
        rev_msg:    [str] reversed message
    '''
    rev_msg = subprocess.check_output(f'python3 app1.py \"{message}\"', shell=True).decode()
    logger.info(f'Output of APP1: {rev_msg}')
    return rev_msg


@app.post(URL_PREFIX + '/convert', tags=['applications'])
def convert_message(message: str):
    '''
    This call converts a message from STR->INT or INT->STR
    Args:
        message:    [str] message to convert
    Output:
        conv_msg:   [str] converted message
    '''
    conv_msg = subprocess.check_output(f'python3 app2.py \"{message}\"', shell=True).decode()
    logger.info(f'Output of APP2: {conv_msg}')
    return conv_msg


@app.post(URL_PREFIX + '/save', tags=['applications'])
def save_message(message: str):
    '''
    This call saves a given message as a file
    Args:
        message:    [str] message to be saved
    Output:
        out:        [str] name of the output file
    '''
    out = subprocess.check_output(f'python3 app3.py \"{message}\"', shell=True).decode()
    logger.info(f'Output of APP3: {out}')
    return out


@app.post(URL_PREFIX + '/file_service', tags=['applications'])
def file_service(filename: str):
    '''
    This call reads the contents of a file and proceeds to execute the apps
    Args:
        filename:   [str] Name of the file
    Output:
        out3:       [str] Name of the output file
    '''
    f = open(filename, "r")
    fcontents = f.read().splitlines()  # each line as an element in a list
    logger.info(f'Received: {fcontents}')
    out1 = reverse_message(fcontents[0])
    out2 = convert_message(out1)
    out3 = save_message(out2)
    return out3


@app.post(URL_PREFIX + '/online_service', tags=['applications'])
def online_service(fcontents: str):
    '''
    This call execute the apps using the input string
    Args:
        fcontents:      [str] Contents of the file
    Output:
        out2:           [str] Output file after reverse and convert
    '''
    logger.info(f'Received: {fcontents}')
    out1 = reverse_message(fcontents)
    out2 = convert_message(out1)
    return out2


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
