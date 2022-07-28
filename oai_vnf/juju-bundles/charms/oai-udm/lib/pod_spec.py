import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make udm ports details"""
    return [
        {
            "name": "http",
            "protocol": "TCP",
            "containerPort": config["http"]
        }
    ]


def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    return {
        "version": 3,
        "containers": [
            {
                "name": "oai-udm",
                "image": config["image"],
                "imagePullPolicy": "Never",  # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "INSTANCE": config["instance"],
                    "PID_DIRECTORY": config["pid-directory"],
                    "UDM_NAME": config["udm-name"],
                    "SBI_IF_NAME": config["sbi-if-name"],
                    "SBI_PORT": config["sbi-port"],
                    "UDM_VERSION_NB": config["udm-version-nb"],
                    "USE_FQDN_DNS": config["use-fqdn-dns"],
                    "UDR_IP_ADDRESS": config["udr-ip-address"],
                    "UDR_PORT": config["udr-port"],
                    "UDR_VERSION_NB": config["udr-version-nb"],
                    "UDR_FQDN": config["udr-fqdn"]
                }
            }
        ]
    }