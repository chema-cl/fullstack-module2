from commons.utils import initialize_app
from api import args, config


def main():
    initialize_app(args.servidor, args.puerto, config)


if __name__ == '__main__':
    main()

