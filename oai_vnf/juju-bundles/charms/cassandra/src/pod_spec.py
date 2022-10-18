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
       },
       {
           "name": "http2",
           "protocol": "TCP",
           "containerPort": config["http2-port"]
       },
       {
           "name": "http3",
           "protocol": "TCP",
           "containerPort": config["http3-port"]
       },
       {
           "name": "http4",
           "protocol": "TCP",
           "containerPort": config["http4-port"]
       },
       {
           "name": "http5",
           "protocol": "TCP",
           "containerPort": config["http5-port"]
       }
   ] 


def oai_db_init_content():
    with open('initialization/oai_db.cql') as text_file:
        return text_file.read()


def make_config_map():
    return [
        {
            "name": "db-init",
            "mountPath": "/home",
            "files": [
                {
                    "path": "oai_db.cql",
                    "content": oai_db_init_content()
                }
            ]
        }
    ]


def make_probes():
    return {
        "exec": {
            "command": ["/bin/bash", "-c", "nodetool status"]
        },
        "initialDelaySeconds": 10,
        "periodSeconds": 15,
        "timeoutSeconds": 10,
        "successThreshold": 1,
        "failureThreshold": 5
    }


def make_env_config(config):
    return {
        "CASSANDRA_CLUSTER_NAME": config["cluster-name"],
        "CASSANDRA_ENDPOINT_SNITCH": config["endpoint-snich"]
    }


def make_network_attachment(config: Dict[str, Any]):
    return {
        "network-attachment-definitions.k8s.cni.cncf.io": [
            {
                "apiVersion": "k8s.cni.cncf.io/v1",
                "kind": "NetworkAttachmentDefinition",
                "metadata": {
                    "name": config["net-name"]
                },
                "spec": {
                    "config": json.dumps({
                        "cniVersion": "0.3.0",
                        "name": config["net-name"],
                        "type": "macvlan",
                        "master": config["host-interface"],
                        "mode": "bridge",
                        "ipam": {
                            "type": "host-local",
                            "subnet": f"{config['net-gateway']}/{config['net-mask']}"
                        }
                    })
                }
            }
        ]
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
    custom_resources = make_network_attachment(config)
    pod["annotations"] = annotations
    return {
        "customResources": custom_resources,
        "pod": pod
    }


def make_pod_spec(config: Dict[str, Any]):
    """make pod specification details"""
    ports = make_pod_ports(config)
    config_map = make_config_map()
    probes = make_probes()
    environments = make_env_config(config)
    k8s_resources = make_k8s_resources(config)
    return {
        "version": 3,
        "kubernetesResources": k8s_resources,
        "containers": [
            {
                "name": "cassandra",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "ports": ports,
                "envConfig": environments,
                "volumeConfig": config_map,
                "kubernetes": {
                    "livenessProbe": probes,
                    "readinessProbe": probes
                }
            }
        ]
    }