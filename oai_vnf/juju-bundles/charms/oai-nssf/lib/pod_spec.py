import yaml
import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make nssf ports details"""
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


def nssf_slice_config() -> str:
    with open("scripts/nssf_slice_config.yaml") as yaml_file:
        nssf_config = yaml.safe_load(yaml_file)
    return yaml.dump(nssf_config)


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
        },
        {
            "name": "nssf-slice-config",
            "mountPath": "/tmp",
            "files": [
                {
                    "path": "nssf_slice_config.yaml",
                    "content": nssf_slice_config()
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


def make_kubernetes_resource() -> Dict[str, Any]:
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
    kubernetes_resource = make_kubernetes_resource()
    return {
        "version": 3,
        "kubernetesResource": kubernetes_resource,
        "containers": [
            {
                "name": "oai-nssf",
                "image": config["image"],
                "imagePullPolicy": "Never",  # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "INSTANCE": config["instance"],
                    "PID_DIRECTORY": config["pid-directory"],
                    "NSSF_NAME": config["nssf-name"],
                    "NSSF_FQDN": config["nssf-fqdn"],
                    "SBI_IF_NAME": config["sbi-if-name"],
                    "SBI_PORT_HTTP1": config["sbi-port-http1"],
                    "SBI_PORT_HTTP2": config["sbi-port-http2"],
                    "SBI_API_VERSION": config["sbi-api-version"],
                    "NSSF_SLICE_CONFIG": config["nssf-slice-config"]
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