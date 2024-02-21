import argparse
import yaml


parser = argparse.ArgumentParser(description='Configurate service')
parser.add_argument('--servidor', help='servidor al que conectarse', default='localhost')
parser.add_argument('--puerto',  help='puerto del servidor',  default=5000)
parser.add_argument('--config', required=True, help='ruta de la configuración')
args = parser.parse_args()


def read_conf():
    with open(args.config, "r") as file:
        return yaml.safe_load(file)


config = read_conf()
