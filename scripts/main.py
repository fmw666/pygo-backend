"""
python main.py --run (default)
python main.py --copy_proto
python main.py --run_proto
python main.py --init_nacos

python main.py --help
"""

import argparse
import os
import subprocess


def run():
    # cd ../apis/**_web && go run main.go
    os.listdir("../apis")
    for d in os.listdir("../apis"):
        if d.endswith("_web"):
            print(d)
            os.chdir("../apis/" + d)
            subprocess.run(["go", "run", "main.go"])
            break
    
    # cd ../services/**_srv && python server.py
    os.listdir("../services")
    for d in os.listdir("../services"):
        if d.endswith("_srv"):
            print(d)
            os.chdir("../services/" + d)
            subprocess.run(["python", "server.py"])
            break


def copy_proto():
    # copy proto/*.proto to ../apis/**_web/proto and ../services/**_srv/proto
    # if proto/*.proto named as user.proto. move to ../apis/user_web/proto and ../services/user_srv/proto
    for f in os.listdir("proto"):
        if f.endswith(".proto"):
            print(f)
            for d in os.listdir("../apis"):
                if d.endswith("_web"):
                    print(d)
                    os.chdir("../apis/" + d)
                    subprocess.run(["cp", "../../proto/" + f, "./proto"])
                    break
            for d in os.listdir("../services"):
                if d.endswith("_srv"):
                    print(d)
                    os.chdir("../services/" + d)
                    subprocess.run(["cp", "../../proto/" + f, "./proto"])
                    break


def run_proto():
    print("run_proto")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="run")
    parser.add_argument("--copy_proto", action="store_true", help="copy_proto")
    parser.add_argument("--run_proto", action="store_true", help="run_proto")
    args = parser.parse_args()

    if args.run:
        run()
    elif args.copy_proto:
        copy_proto()
    elif args.run_proto:
        run_proto()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
