"""
python main.py --init_config
python main.py --init_nacos
python main.py --init_mysql
python main.py --init_jenkins
python main.py --test_connect
python main.py --init (init_config, init_nacos, init_mysql, init_jenkins)

python main.py --help
"""

import argparse

from utils import (init_config, init_nacos, init_mysql, init_jenkins,
                   test_connect)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--init_config",
                        action="store_true", help="init config")
    parser.add_argument("--init_nacos",
                        action="store_true", help="init nacos")
    parser.add_argument("--init_mysql",
                        action="store_true", help="init mysql")
    parser.add_argument("--init_jenkins",
                        action="store_true", help="init jenkins")
    parser.add_argument("--test_connect",
                        action="store_true", help="test connect")
    parser.add_argument("--init",
                        action="store_true", help="init all")
    args = parser.parse_args()

    if args.init_config:
        init_config.execute()
    elif args.init_nacos:
        init_nacos.execute()
    elif args.init_mysql:
        init_mysql.execute()
    elif args.init_jenkins:
        init_jenkins.execute()
    elif args.test_connect:
        test_connect.execute()
    elif args.init:
        # in strict order
        init_config.execute()
        init_nacos.execute()
        init_mysql.execute()
        init_jenkins.execute()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
