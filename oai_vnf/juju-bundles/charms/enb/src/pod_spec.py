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
       },
       {
           "name": "udp3",
           "protocol": "UDP",
           "containerPort": config["udp3-port"]
       }
   ] 


def make_probes():
    return {
        "exec": {
            "command": ["/bin/bash", "-c", "pgrep lte-softmodem"]
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
        "USE_FDD_MONO": config["use-fdd-mono"],
        "RFSIMULATOR": config["rfsimulator"],
        "ENB_NAME": config["enb-name"],
        "MCC": config["mcc"],
        "MNC": config["mnc"],
        "MNC_LENGTH": config["mnc-length"],
        "TAC": config["tac"],
        "UTRA_BAND_ID": config["utra-band-id"],
        "DL_FREQUENCY_IN_MHZ": config["dl-freq"],
        "UL_FREQUENCY_OFFSET_IN_MHZ": config["ul-freq-offset"],
        "NID_CELL": config["nid-cell"],
        "NB_PRB": config["nb-prb"],
        "MME_S1C_IP_ADDRESS": config["mme-s1c-ip-addr"],
        "ENB_S1C_IF_NAME": config["enb-s1c-if-name"],
        "ENB_S1C_IP_ADDRESS": config["enb-s1c-ip-addr"],
        "ENB_S1U_IF_NAME": config["enb-s1u-if-name"],
        "ENB_S1U_IP_ADDRESS": config["enb-s1u-ip-addr"],
        "ENB_X2_IP_ADDRESS": config["enb-x2-ip-addr"],
        "FLEXRAN_ENABLED": config["flexran-enabled"],
        "FLEXRAN_INTERFACE_NAME": config["flexran-if-name"],
        "FLEXRAN_IPV4_ADDRESS": config["flexran-ipv4-addr"],
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
                "name": "enb",
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