import sys
import argparse
import itertools
import numpy as np


class FileNotValid(Exception):
  pass


def load_file_contents(contents):
  '''
  This function loads the contents of the file
  Args:
    contents:   [str] contents of the file
  Output:
    data_type:  [int] type of message
    shape:      [array] shape of the message
    message:    [list] message in file
  '''
  contents = contents.split(',')
  (data_type, shape), message = contents[0:2], contents[2:]
  shape = np.array(shape.split(';'), dtype=int)
  return int(data_type), shape, message


def validate_file(data_type, shape, message):
    '''
    This function validates the file
    '''
    if data_type==1 and sum(shape) != len(message):
        if len(shape) > 1:
            message = ''.join(message)
            if sum(shape) != len(message.replace(' ', '')):  # remove blank spaces
                raise FileNotValid(f'length of message does not fit shape {shape}')
    if data_type==2 and np.prod(shape) != len(message):
        raise FileNotValid(f'length of message does not fit shape {shape}')
    if data_type not in [1, 2]:
        raise FileNotValid(f'data type code {data_type} not supported')
    if type(message[0]) not in [str, int]:
        raise FileNotValid(f'message type {type(message[0])} not supported')
    pass


def arrange_file(data_type, shape, message):
    '''
    This function arranges the file as TYPE, SHAPE, MESSAGE
    Args:
        data_type:      [int] Type of data, where 1 is int and 2 is string
        shape:          [array] Shape of data
        message:        [list] Message
    Output:
        out:            [str] File as defined type
    '''
    if data_type == 1:
        new_msg = ''.join(message)
    if data_type == 2:
        if type(message[0])==list:
            message = list(itertools.chain.from_iterable(message))
        new_msg = ','.join(map(str, message))
    new_shape = ';'.join(shape.astype(str))
    out = f'{data_type},{new_shape},{new_msg}'
    return out
