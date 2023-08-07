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

from common.grpc_health.v1 import health, health_pb2_grpc
from common.register import consul
from goods_srv.handler.banner import BannerServicer
from goods_srv.handler.brand import BrandServicer
from goods_srv.handler.category import CategoryServicer
from goods_srv.handler.goods import GoodsServicer
from goods_srv.proto import goods_pb2_grpc, category_pb2_grpc, banner_pb2_grpc, brand_pb2_grpc
from goods_srv.settings import settings


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
                        default=settings.HOST,
                        # default="192.168.1.2",
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

    logger.add("logs/goods_srv_{time}.log", rotation="500 MB", encoding="utf-8")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # register goods service
    goods_pb2_grpc.add_GoodsServicer_to_server(GoodsServicer(), server)
    banner_pb2_grpc.add_BannerServicer_to_server(BannerServicer(), server)
    brand_pb2_grpc.add_BrandServicer_to_server(BrandServicer(), server)
    category_pb2_grpc.add_CategoryServicer_to_server(CategoryServicer(), server)
    # register health service
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    server.add_insecure_port(f"{args.ip}:{port}")

    service_id = str(uuid.uuid1())

    # main process listen to SIGINT and SIGTERM
    signal.signal(signal.SIGINT, partial(signal_on_exit, service_id=service_id))
    signal.signal(signal.SIGTERM, partial(signal_on_exit, service_id=service_id))

    # server start
    logger.info(f"server goods start at {args.ip}:{port}")
    server.start()

    # register service
    logger.info(f"register goods service to consul")
    register = consul.ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
    if not register.register(
        name=settings.SERVICE_NAME,
        id=service_id,
        address=args.ip,
        port=port,
        tags=settings.SERVICE_TAGS,
        check=None,
    ):
        logger.error(f"register goods service to consul failed")
        sys.exit(0)

    server.wait_for_termination()


if __name__ == "__main__":
    settings.client.add_config_watcher(settings.NACOS["DataId"], settings.NACOS["Group"], settings.update_cfg)
    serve()
