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


def live_ready_script() -> str:
    with open("scripts/live-ready.sh") as text_file:
        return text_file.read()


def make_volume_config() -> List[Dict[str, Any]]:
    return [
        {
            "name": "scripts",
            "mountPath": "/scripts",
            "files": [
                {
                    "path": "live-ready.sh",
                    "content": live_ready_script()
                }
            ]
        }
    ]


def make_liveness_probe() -> Dict[str, Any]:
    return {
        "exec": {
            "command": ["sh", "/scripts/live-ready.sh"]
        },
        "initialDelaySeconds": 10,
        "periodSeconds": 5
    }


def make_readiness_probe() -> Dict[str, Any]:
    return {
        "exec": {
            "command": ["sh", "/scripts/live-ready.sh"]
        },
        "initialDelaySeconds": 5,
        "periodSeconds": 5
    }


def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    volume_config = make_volume_config()
    liveness_probe = make_liveness_probe()
    readiness_probe = make_readiness_probe()
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
                },
                "volumeConfig": volume_config,
                "kubernetes": {
                    "livenessProbe": liveness_probe,
                    "readinessProbe": readiness_probe
                }
            }
        ]
    }