import argparse
# import docker or local
try:
    from trainer.model_train import training # for docker
except ImportError:
    from model_train import training  # for local debug


if __name__ == '__main__':
    # Parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--job-version',
        nargs='+',
        help='Name for trainer job and filder')
    parser.add_argument(
        '--trainded-dir',
        nargs='+',
        help='Training file local or GCS')
    args, _ = parser.parse_known_args()

    # Send to train
    training(args)
