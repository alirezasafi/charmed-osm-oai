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
            },
            "restartPolicy": "Always",
            "dnsPolicy": "ClusterFirst",
            "terminationGracePeriodSeconds": 30
        }
    }


def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    volume_config = make_volume_config()
    liveness_probe = make_liveness_probe()
    readiness_probe = make_readiness_probe()
    kubernetes_resources = make_kubernetes_resources()
    return {
        "version": 3,
        "kubernetesResources": kubernetes_resources,
        "containers": [
            {
                "name": "oai-ausf",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
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