import json
import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make gnb ports details"""
    return [
        {
            "name": "slu",
            "protocol": "UDP",
            "containerPort": config["slu-port"]
        },
        {
            "name": "s1c",
            "protocol": "UDP",
            "containerPort": config["slc-port"]
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
                    "name": "oai-gnb-net1",
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
                                    "address": f"{config['multus-ip1']}/{config['multus-mask1']}"
                                }
                            ]
                        }
                    })
                }
            },
            {
                "apiVersion": "k8s.cni.cncf.io/v1",
                "kind": "NetworkAttachmentDefinition",
                "metadata": {
                    "name": "oai-gnb-net2",
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
                                    "address": f"{config['multus-ip2']}/{config['multus-mask2']}"
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
                    "name": "oai-gnb-net1",
                    "default-route": [config["multus-gateway"]]
                },
                {
                     "name": "oai-gnb-net2"
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
                "name": "oai-gnb",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "RFSIMULATOR": config["rfsimulator"],
                    "USE_SA_TDD_MONO": config["use-sa-tdd-mono"],
                    "GNB_NAME": config["gnb-name"],
                    "MCC": config["mcc"],
                    "MNC": config["mnc"],
                    "MNC_LENGTH": config["mnc-length"],
                    "TAC": config["tac"],
                    "NSSAI_SST": config["nssai-sst"],
                    "NSSAI_SD0": config["nssai-sd0"],
                    "NSSAI_SD1": config["nssai-sd1"],
                    "AMF_IP_ADDRESS": config["amf-ip-address"],
                    "GNB_NGA_IF_NAME": config["gnb-nga-if-name"],
                    "GNB_NGA_IP_ADDRESS": config["gnb-nga-ip-address"],
                    "GNB_NGU_IF_NAME": config["gnb-ngu-if-name"],
                    "GNB_NGU_IP_ADDRESS": config["gnb-ngu-ip-address"],
                    "USE_ADDITIONAL_OPTIONS": config["use-additional-option"]
                },
                "kubernetes": {
                    "securityContext": {
                        "privileged": True
                    }
                }
            }
        ]
    }