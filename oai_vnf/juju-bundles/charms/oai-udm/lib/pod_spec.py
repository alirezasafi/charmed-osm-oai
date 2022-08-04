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


def make_kubernetes_resources() -> Dict[str, Any]:
    return {
        "pod": {
            "securityContext": {
                "runAsUser": 0,
                "runAsGroup": 0
            }
        }
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
                    "SBI_HTTP2_PORT": config["sbi-http2-port"],
                    "UDM_VERSION_NB": config["udm-version-nb"],
                    "USE_FQDN_DNS": config["use-fqdn-dns"],
                    "UDR_IP_ADDRESS": config["udr-ip-address"],
                    "UDR_PORT": config["udr-port"],
                    "UDR_VERSION_NB": config["udr-version-nb"],
                    "UDR_FQDN": config["udr-fqdn"],
                    "NRF_IPV4_ADDRESS": config["nrf-ipv4-address"],
                    "NRF_PORT": config["nrf-port"],
                    "NRF_API_VERSION": config["nrf-api-version"],
                    "NRF_FQDN": config["nrf-fqdn"]
                },
                "volumeConfig": volume_config,
                "kubernetes": {
                    "livenessProbe": liveness_probe,
                    "readinessProbe": readiness_probe,
                    "securityContext": {
                        "privileged": False
                    }
                }
            }
        ]
    }