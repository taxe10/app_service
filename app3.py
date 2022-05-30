import sys
import argparse


def save_file(filename, message):
  f = open(filename, 'w')
  f.write(str(message))
  f.close()
  return(f'{filename} saved successfully')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('message', help='message')
    args = parser.parse_args()
    
    filename = 'out.txt'
    out_app3 = save_file(filename, args.message)
    sys.stdout.write(filename)
    