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


def make_probes():
    return {
        "exec": {
            "command": ["/bin/bash", "-c", "pgrep lte-uesoftmodem"]
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


def make_env_config(config: Dict[str, Any]):
    return {
        "TZ": config["tz"],
        "HOSTNAME": config["host-name"],
        "RFSIMULATOR": config["rfsimulator"],
        "MCC": config["mcc"],
        "MNC": config["mnc"],
        "SHORT_IMSI": config["short-imsi"],
        "LTE_KEY": config["lte-key"],
        "OPC": config["opc"],
        "MSISDN": config["misisdn"],
        "HPLMN": config["hplmn"],
        "USE_ADDITIONAL_OPTIONS": config["use-additional-options"],
    }


def make_pod_spec(config: Dict[str, Any]):
    """make pod specification details"""
    ports = make_pod_ports(config)
    probes = make_probes()
    k8s_resources = make_k8s_resources(config)
    environments = make_env_config(config)
    return {
        "version": 3,
        "kubernetesResources": k8s_resources,
        "containers": [
            {
                "name": "ue0",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "envConfig": environments,
                "ports": ports,
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