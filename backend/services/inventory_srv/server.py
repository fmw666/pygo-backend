import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import signal
import socket
import uuid
from concurrent import futures
from functools import partial

import grpc
from loguru import logger
from rocketmq.client import PushConsumer

from common.grpc_health.v1 import health, health_pb2_grpc
from common.register import consul
from inventory_srv.handler.inventory import InventoryServicer, reback_inventory
from inventory_srv.proto import inventory_pb2_grpc
from inventory_srv.settings import settings


def signal_on_exit(signo, frame, service_id=None):
    logger.info(f"deregister service {service_id} from consul...")
    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
    register.deregister(service_id)
    logger.info(f"deregister service {service_id} from consul success")
    sys.exit(0)


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port


def serve():
    # python server.py --ip=127.0.0.1 --port=50051
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        nargs="?",
                        type=str,
                        default="192.168.200.129",
                        help="binding ip"
                        )
    parser.add_argument("--port",
                        nargs="?",
                        type=int,
                        default=0,
                        help="listening port"
                        )

    args = parser.parse_args()

    if args.port == 0:
        port = get_free_tcp_port()
    else:
        port = args.port

    logger.add("logs/inventory_srv_{time}.log", rotation="500 MB", encoding="utf-8")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # register inventory service
    inventory_pb2_grpc.add_InventoryServicer_to_server(InventoryServicer(), server)
    # register health service
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    server.add_insecure_port(f"{args.ip}:{port}")

    service_id = str(uuid.uuid1())

    # main process listen to SIGINT and SIGTERM
    signal.signal(signal.SIGINT, partial(signal_on_exit, service_id=service_id))
    signal.signal(signal.SIGTERM, partial(signal_on_exit, service_id=service_id))

    # server start
    logger.info(f"server inventory start at {args.ip}:{port}")
    server.start()

    # register service
    logger.info(f"register inventory service to consul")
    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
    if not register.register(
        name=settings.SERVICE_NAME,
        id=service_id,
        address=args.ip,
        port=port,
        tags=settings.SERVICE_TAGS,
        check=None,
    ):
        logger.error(f"register inventory service to consul failed")
        sys.exit(0)

    # listen the rocketmq topic, and update the inventory
    consumer = PushConsumer("pygo_inventory")
    consumer.set_name_server_address(f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}")
    consumer.subscribe("order_reback", callback=reback_inventory)
    consumer.start()

    server.wait_for_termination()
    consumer.shutdown()


if __name__ == "__main__":
    settings.client.add_config_watcher(settings.NACOS["DataId"], settings.NACOS["Group"], settings.update_cfg)
    serve()
