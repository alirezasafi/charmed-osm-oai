import logging
import json
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_probes():
    return {
        "exec": {
            "command": ["/bin/bash", "-c", "ping -c 2 192.168.61.5"]
        },
        "initialDelaySeconds": 10,
        "periodSeconds": 15,
        "timeoutSeconds": 10,
        "successThreshold": 1,
        "failureThreshold": 5
    }


def make_k8s_resources(config: Dict[str, Any]):
    pod = {
        "restartPolicy": "Always",
        "dnsPolicy": "ClusterFirst",
        "terminationGracePeriodSeconds": 30
    }
    annotations = {
        "k8s.v1.cni.cncf.io/networks": json.dumps([
            {
                "name": config["net-name"],
                "interface": config["interface"],
                "ips": [config["ip-addr"]],
                "default": True
            }
        ])
    }
    pod["annotations"] = annotations
    return {
        "pod": pod
    }

def make_pod_spec(config: Dict[str, Any]):
    """make pod specification details"""
    probes = make_probes()
    k8s_resources = make_k8s_resources(config)
    return {
        "version": 3,
        "kubernetesResources": k8s_resources,
        "containers": [
            {
                "name": "trf-gen",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "command": ["/bin/bash", "-c", "ip route add 12.0.0.0/24 via 192.168.61.5 dev eth1; sleep infinity"],
                "kubernetes": {
                    "livenessProbe": probes,
                    "readinessProbe": probes,
                    "securityContext": {
                        "privileged": True
                    }
                }
            }
        ]
    }