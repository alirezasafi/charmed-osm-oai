import json
import logging
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
        }
    ]


def make_probes():
    return {
        "exec": {
            "command": ["/bin/bash", "-c", "pgrep oai_hss"]
        },
        "initialDelaySeconds": 10,
        "periodSeconds": 15,
        "timeoutSeconds": 10,
        "successThreshold": 1,
        "failureThreshold": 5
    }


def make_env_config(config: Dict[str, Any]):
    return {
        "REALM": config["realm"],
        "HSS_FQDN": config["hss-fqdn"],
        "PREFIX": config["prefix"],
        "cassandra_Server_IP": config["cassandra-ip"],
        "OP_KEY": config["op-key"],
        "LTE_K": config["lte-k"],
        "APN1": config["apn1"],
        "APN2": config["apn2"],
        "FIRST_IMSI": config["first-imsi"],
        "NB_USERS": config["nb-users"]
    }


def make_network_attachment(config: Dict[str, Any]):
    return {
        "network-attachment-definitions.k8s.cni.cncf.io": [
            {
                "apiVersion": "k8s.cni.cncf.io/v1",
                "kind": "NetworkAttachmentDefinition",
                "metadata": {
                    "name": config["pub-net-name"]
                },
                "spec": {
                    "config": json.dumps({
                        "cniVersion": "0.3.0",
                        "name": config["pub-net-name"],
                        "type": "macvlan",
                        "master": config["host-interface"],
                        "mode": "bridge",
                        "ipam": {
                            "type": "host-local",
                            "subnet": f"{config['pub-net-gateway']}/{config['pub-net-mask']}"
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
                "name": config["pv-net-name"],
                "interface": config["pv-interface"],
                "ips": [config["pv-ip-addr"]],
                "default": True
            },
            {
                "name": config["pub-net-name"],
                "interface": config["pub-interface"],
                "ips": [config["pub-ip-addr"]]
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
    probes = make_probes()
    environmets = make_env_config(config)
    k8s_resources = make_k8s_resources(config)
    return {
        "version": 3,
        "kubernetesResources": k8s_resources,
        "containers": [
            {
                "name": "oai-hss",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "ports": ports,
                "envConfig": environmets,
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