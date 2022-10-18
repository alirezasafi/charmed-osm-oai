import logging
import json
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]):
   """make service ports"""
   return [
       {
           "name": "udp1",
           "protocol": "UDP",
           "containerPort": config["udp1-port"]
       },
       {
           "name": "udp2",
           "protocol": "UDP",
           "containerPort": config["udp2-port"]
       }
   ] 


def make_probes():
    return {
        "exec": {
            "command": ["/bin/bash", "-c", "pgrep oai_spgwu"]
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
        "PID_DIRECTORY": config["pid-directory"],
        "INSTANCE": config["instance"],
        "SGW_INTERFACE_NAME_FOR_S1U_S12_S4_UP": config["sgw-interface-name-for-s1u"],
        "PGW_INTERFACE_NAME_FOR_SGI": config["pgw-interface-name-for-sgi"],
        "SGW_INTERFACE_NAME_FOR_SX": config["sgw-interface-name-for-sx"],
        "SPGWC0_IP_ADDRESS": config["spgwc0-ip-addr"],
        "NETWORK_UE_IP": config["network-ue-ip"],
        "NETWORK_UE_NAT_OPTION": config["network-ue-nat-option"],
        "MCC": config["mcc"],
        "MNC": config["mnc"],
        "MNC03": config["mnc03"],
        "TAC": config["tac"],
        "GW_ID": config["gw-id"],
        "REALM": config["realm"],
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
                "name": "oai-spgwu",
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