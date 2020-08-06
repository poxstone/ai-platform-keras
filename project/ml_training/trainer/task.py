import argparse
# import docker or local
try:
    from trainer.model_train import training, evaluate # for docker
except ImportError:
    from model_train import training, evaluate  # for local debug


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
    # for tests
    parser.add_argument(
        '--is-test',
        nargs='+',
        help='boolean')
    parser.add_argument(
        '--img-index',
        nargs='+',
        help='integer [0-10000] to test training')
    args, _ = parser.parse_known_args()

    # Send to train
    if args.is_test and args.is_test[0] == 'true':
        evaluate(args)
    else:
        training(args)
