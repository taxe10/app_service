import argparse
from itertools import cycle
import sys
import numpy as np

from helper_utils import load_message, validate_message, arrange_message, FileNotValid

LIST_UPPER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
LIST_SYMBOLS = ['[',"'\\",']','^','-','`']
LIST_LOWER = list(map(lambda x: x.lower(), LIST_UPPER))
LIST_ABC = LIST_UPPER + LIST_SYMBOLS + LIST_LOWER
LIST_NUM = list(range(len(LIST_ABC)))
DEFAULT_NUM = len(LIST_ABC)-1


def str2int(segment, shape, max_shape):
    '''
    This function converts a string to a list of integers
    Args:
        segment:    [str] Input string
        shape:      [array] Shape of input string
        max_shape:  [int] Maximum element in shape
    Output:
        out_array:  [list] List of integers
    '''
    out_array = []
    shapecycle = cycle(shape)
    current_shape = next(shapecycle)
    length = 0
    for element in segment:
        if element in LIST_ABC:
            out_array.append(LIST_NUM[LIST_ABC.index(element)])
        else:
            out_array.append(DEFAULT_NUM)
        if len(out_array) == current_shape + length:
            out_array = out_array + [DEFAULT_NUM] * (max_shape - current_shape)
            length = len(out_array)
            current_shape = next(shapecycle)
    return out_array


def int2str(segment):
    '''
    This function converts a list of integers to a string
    Args:
        segment:    [list] List of integers
    Output:
        out_text:   [str] Output string
    '''
    out_text = ''
    for element in segment:
        out_text = out_text + LIST_ABC[min(element, DEFAULT_NUM)]
    return out_text


def convert_message(data_type, shape, message):
    '''
    This function converts the input message
    Args:
        message:      [list] message to translate
    Output:
        conv_msg:     [list] converted message
    '''
    if data_type == 1:
        max_shape = np.max(shape)
        if len(shape)>1:
            conv_shape = np.array([len(shape), max_shape])
        else:
            conv_shape = np.array([max_shape])
        conv_msg = str2int(''.join(message), shape, max_shape)
    if data_type == 2:
        if len(shape) > 1:
            conv_shape = np.repeat(shape[1], shape[0])
        else:
            conv_shape = shape
        conv_msg = int2str(np.array(message, dtype=int))
    return conv_msg, conv_shape


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('message', help='message')
    args = parser.parse_args()

    data_type, shape, message = load_message(args.message)
    validate_message(data_type, shape, message)

    conv_msg, conv_shape = convert_message(data_type, shape, message)
    out = arrange_message(3 - data_type, conv_shape, conv_msg)
    sys.stdout.write(out)
