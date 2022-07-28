import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make udr ports details"""
    return [
        {
            "name": "http1",
            "protocol": "TCP",
            "containerPort": config["http1"]
        },
        {
            "name": "http2",
            "protocol": "TCP",
            "containerPort": config["http2"]
        }
    ]


def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    return {
        "version": 3,
        "containers": [
            {
                "name": "oai-udr",
                "image": config["image"],
                "imagePullPolicy": "Never",  # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "INSTANCE": config["instance"],
                    "PID_DIRECTORY": config["pid-directory"],
                    "UDR_INTERFACE_NAME_FOR_NUDR": config["udr-interface-name-for-nudr"],
                    "UDR_INTERFACE_PORT_FOR_NUDR": config["udr-interface-port-for-nudr"],
                    "UDR_INTERFACE_HTTP2_PORT_FOR_NUDR": config["udr-interface-http2-port-for-nudr"],
                    "UDR_API_VERSION": config["udr-api-version"],
                    "MYSQL_IPV4_ADDRESS": config["mysql-ipv4-address"],
                    "MYSQL_USER": config["mysql-user"],
                    "MYSQL_PASS": config["mysql-pass"],
                    "MYSQL_DB": config["mysql-db"],
                    "WAIT_MYSQL": config["wait-mysql"]
                }
            }
        ]
    }