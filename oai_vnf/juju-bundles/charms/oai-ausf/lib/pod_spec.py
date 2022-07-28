import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make ausf ports details"""
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
                "name": "oai-ausf",
                "image": config["image"],
                "imagePullPolicy": "Never",  # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "INSTANCE_ID": config["instance-id"],
                    "PID_DIR": config["pid-dir"],
                    "AUSF_NAME": config["ausf-name"],
                    "SBI_IF_NAME": config["sbi-if-name"],
                    "SBI_PORT": config["sbi-port"],
                    "USE_FQDN_DNS": config["use-fqdn-dns"],
                    "UDM_IP_ADDRESS": config["udm-ip-address"],
                    "UDM_PORT": config["udm-port"],
                    "UDM_VERSION_NB": config["udm-version-nb"],
                    "UDM_FQDN": config["udm-fqdn"]
                }
            }
        ]
    }