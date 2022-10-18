import logging
import json
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]):
   """make service ports"""
   return [
       {
           "name": "http1",
           "protocol": "TCP",
           "containerPort": config["http1-port"]
       }
   ] 


def redis_config_content():
    with open('configurations/redis.conf') as text_file:
        return text_file.read()


def make_config_map():
    return [
        {
            "name": "redis-conf",
            "mountPath": "/usr/local/etc/redis",
            "files": [
                {
                    "path": "redis.conf",
                    "content": redis_config_content()
                }
            ]
        }
    ]


def make_probes():
    return {
        "exec": {
            "command": ["/bin/bash", "-c", "redis-cli -h 192.168.61.6 -p 6380 ping"]
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
    ports = make_pod_ports(config)
    config_map = make_config_map()
    probes = make_probes()
    k8s_resources = make_k8s_resources(config)
    return {
        "version": 3,
        "kubernetesResources": k8s_resources,
        "containers": [
            {
                "name": "redis",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "command": ["/bin/bash", "-c", "redis-server /usr/local/etc/redis/redis.conf"],
                "ports": ports,
                "volumeConfig": config_map,
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