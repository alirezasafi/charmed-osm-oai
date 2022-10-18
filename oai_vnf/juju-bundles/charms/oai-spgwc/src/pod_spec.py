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
            "command": ["/bin/bash", "-c", "pgrep oai_spgwc"]
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
        "SGW_INTERFACE_NAME_FOR_S11": config["sgw-interface-name-for-s11"],
        "PGW_INTERFACE_NAME_FOR_SX": config["pgw-interface-name-for-sx"],
        "DEFAULT_DNS_IPV4_ADDRESS": config["default-dns-ipv4-addr"],
        "DEFAULT_DNS_SEC_IPV4_ADDRESS": config["default-dns-sec-ipv4-addr"],
        "PUSH_PROTOCOL_OPTION": config["push-protocol-option"],
        "APN_NI_1": config["apn-ni-1"],
        "APN_NI_2": config["apn-ni-2"],
        "DEFAULT_APN_NI_1": config["default-apn-ni-1"],
        "UE_IP_ADDRESS_POOL_1": config["ue-ip-addr-pool-1"],
        "UE_IP_ADDRESS_POOL_2": config["ue-ip-addr-pool-2"],
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
                "name": "oai-spgwc",
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