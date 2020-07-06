import argparse
from trainer.model import train_and_evaluate

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--job-name',
        nargs='+',
        help='Name for trainer job and filder')
    parser.add_argument(
        '--train-files',
        nargs='+',
        help='Training file local or GCS')

    args, _ = parser.parse_known_args()
    train_and_evaluate(args)
