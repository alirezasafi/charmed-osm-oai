import json
import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make nr-ue ports details"""
    return [
        {
            "name": "slc",
            "protocol": "UDP",
            "containerPort": config["slc-port"]
        },
        {
            "name": "slu",
            "protocol": "UDP",
            "containerPort": config["slu-port"]
        },
        {
            "name": "x2c",
            "protocol": "UDP",
            "containerPort": config["x2c-port"]
        }
    ]


def make_network_attachment_resources(config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "network-attachment-definitions.k8s.cni.cncf.io": [
            {
                "apiVersion": "k8s.cni.cncf.io/v1",
                "kind": "NetworkAttachmentDefinition",
                "metadata": {
                    "name": "oai-nr-ue-net1",
                },
                "spec": {
                    "config": json.dumps({
                        "cniVersion": "0.3.0",
                        "type": "macvlan",
                        "master": config["multus-host-interface"],
                        "mode": "bridge",
                        "ipam": {
                            "type": "static",
                            "addresses": [
                                {
                                    "address": f"{config['multus-ip']}/{config['multus-mask']}"
                                }
                            ]
                        }
                    })
                }
            }
        ]
    }


def make_kubernetes_resources(config: Dict[str, Any]) -> Dict[str, Any]:
    pod = {
        "securityContext": {
            "runAsUser": 0,
            "runAsGroup": 0
        }
    }
    if config["multus-create"]:
        annotations = {
            "k8s.v1.cni.cncf.io/networks": json.dumps([
                {
                    "name": "oai-nr-ue-net1",
                    "default-route": [config["multus-gateway"]]
                }
            ])
        }   
        custom_resources = make_network_attachment_resources(config)
        pod["annotations"] = annotations
        return {
            "customResources": custom_resources,
            "pod": pod
        }
    return {
        "pod": pod
    }


def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    kubernetes_resources = make_kubernetes_resources(config)
    return {
        "version": 3,
        "kubernetesResources": kubernetes_resources,
        "containers": [
            {
                "name": "oai-nr-ue",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "RFSIMULATOR": config["rfsimulator"],
                    "FULL_IMSI": config["full-imsi"],
                    "FULL_KEY": config["full-key"],
                    "OPC": config["opc"],
                    "DNN": config["dnn"],
                    "NSSAI_SST": config["nssai-sst"],
                    "NSSAI_SD": config["nssai-sd"],
                    "USE_ADDITIONAL_OPTIONS": config["use-additional-options"]
                },
                "kubernetes": {
                    "securityContext": {
                        "privileged": True
                    }
                }
            }
        ]
    }