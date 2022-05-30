import sys
import argparse
import itertools
import numpy as np

from helper_utils import load_file_contents, validate_file, arrange_file, FileNotValid


def reverse_message(data_type, shape, message):
  '''
  This function reverses the message
  Args:
    data_type:  [int] type of message
    shape:      [array] shape of the message
    message:    [list] message to be reversed
  Output:
    rev_msg:    [list] reversed message
  '''
  ## DATA TYPE -> STRING
  if data_type == 1:
    message = ''.join(message)      # consolidate in 1 string
    if len(shape)>1:                # if list of strings, remove blank spaces
      message = message.replace(' ', '')
    message = ' ' + message         # adding this for the routine later
    rev_msg = []
    for ii in range(len(shape)):
      if ii==0:
        rev_msg.append(message[shape[ii]:0:-1])
      else:
        current = sum(shape[:ii])
        rev_msg.append(message[current+shape[ii]:current:-1])
  ## DATA TYPE -> INTEGER
  if data_type == 2:
    message = np.array(message, dtype=int)
    message = np.reshape(message, shape)
    if len(message.shape)>1:
      rev_msg = np.flip(message, axis=1)
    else:
      rev_msg = np.flip(message)
    rev_msg = rev_msg.tolist()
  return rev_msg


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('message', help='filename')
    args = parser.parse_args()

    data_type, shape, message = load_file_contents(args.message)
    validate_file(data_type, shape, message)

    rev_msg = reverse_message(data_type, shape, message)
    out = arrange_file(data_type, shape, rev_msg)
    sys.stdout.write(out)
