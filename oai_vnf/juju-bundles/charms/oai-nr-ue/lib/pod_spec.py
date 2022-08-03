import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make nr-ue ports details"""
    return [
        {
            "name": "slc",
            "protocol": "UDP",
            "containerPort": config["slc-port"]
        },
        {
            "name": "slu",
            "protocol": "UDP",
            "containerPort": config["slu-port"]
        },
        {
            "name": "x2c",
            "protocol": "UDP",
            "containerPort": config["x2c-port"]
        }
    ]


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
    kubernetes_resources = make_kubernetes_resources()
    return {
        "version": 3,
        "kubernetesResources": kubernetes_resources,
        "containers": [
            {
                "name": "oai-nr-ue",
                "image": config["image"],
                "imagePullPolicy": "Never",  # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "RFSIMULATOR": config["rfsimulator"],
                    "FULL_IMSI": config["full-imsi"],
                    "FULL_KEY": config["full-key"],
                    "OPC": config["opc"],
                    "DNN": config["dnn"],
                    "NSSAI_SST": config["nssai-sst"],
                    "NSSAI_SD": config["nssai-sd"],
                    "USE_ADDITIONAL_OPTIONS": config["use-additional-options"]
                },
                "kubernetes": {
                    "securityContext": {
                        "privileged": True
                    }
                }
            }
        ]
    }