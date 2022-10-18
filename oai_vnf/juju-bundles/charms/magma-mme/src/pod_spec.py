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
           "name": "http1",
           "protocol": "TCP",
           "containerPort": config["http1-port"]
       },
       {
           "name": "http2",
           "protocol": "TCP",
           "containerPort": config["http2-port"]
       }
   ] 


def entrypoint_content():
    with open('configurations/entrypoint.sh') as text_file:
        return text_file.read()


def mme_config_content():
    with open('configurations/mme.conf') as text_file:
        return text_file.read()


def mme_fd_config_content():
    with open('configurations/mme_fd.conf.tmplt') as text_file:
        return text_file.read()

def make_config_map():
    return [
        {
            "name": "mme-entrypoint",
            "mountPath": "/magma-mme/bin",
            "files": [
                {
                    "path": "entrypoint.sh",
                    "content": entrypoint_content(),
                }
            ]
        },
        {
            "name": "mme-config",
            "mountPath": "/magma-mme/etc",
            "files": [
                {
                    "path": "mme.conf",
                    "content": mme_config_content()
                },
                {
                    "path": "mme_fd.conf.tmplt",
                    "content": mme_fd_config_content()
                }
            ]
        }
    ]


def make_probes():
    return {
        "exec": {
            "command": ["/bin/bash", "-c", "pgrep oai_mme"]
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
        "REALM": config["realm"],
        "PREFIX": config["prefix"],
        "HSS_HOSTNAME": config["hss-hostname"],
        "HSS_FQDN": config["hss-fqdn"],
        "HSS_REALM": config["hss-realm"],
        "MME_FQDN": config["mme-fqdn"],
        "FEATURES": config["features"]
    }


def make_pod_spec(config: Dict[str, Any]):
    """make pod specification details"""
    ports = make_pod_ports(config)
    config_map = make_config_map()
    probes = make_probes()
    k8s_resources = make_k8s_resources(config)
    environments = make_env_config(config)
    return {
        "version": 3,
        "kubernetesResources": k8s_resources,
        "containers": [
            {
                "name": "magma-mme",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "command": ["/bin/bash", "-c", "/magma-mme/bin/entrypoint.sh"],
                "ports": ports,
                "envConfig": environments,
                # "volumeConfig": config_map,
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