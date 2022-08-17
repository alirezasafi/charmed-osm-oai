import json
import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make spgwu ports details"""
    return [
        {
            "name": "oai-spgwu-tiny",
            "protocol": "UDP",
            "containerPort": config["oai-spgwu-tiny"]
        },
        {
            "name": "s1u",
            "protocol": "UDP",
            "containerPort": config["s1u"]
        },
        {
            "name": "iperf",
            "protocol": "UDP",
            "containerPort": config["iperf"]
        }
    ]


def live_ready_script() -> str:
    with open("scripts/live-ready.sh") as text_file:
        return text_file.read()


def make_volume_config() -> List[Dict[str, Any]]:
    return [
        {
            "name": "scripts",
            "mountPath": "/scripts",
            "files": [
                {
                    "path": "live-ready.sh",
                    "content": live_ready_script()
                }
            ]
        }
    ]


def make_liveness_probe() -> Dict[str, Any]:
    return {
        "exec": {
            "command": ["sh", "/scripts/live-ready.sh"]
        },
        "initialDelaySeconds": 10,
        "periodSeconds": 5
    }


def make_readiness_probe() -> Dict[str, Any]:
    return {
        "exec": {
            "command": ["sh", "/scripts/live-ready.sh"]
        },
        "initialDelaySeconds": 5,
        "periodSeconds": 5
    }


def make_network_attachment_resources(config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "network-attachment-definitions.k8s.cni.cncf.io": [
            {
                "apiVersion": "k8s.cni.cncf.io/v1",
                "kind": "NetworkAttachmentDefinition",
                "metadata": {
                    "name": "oai-5g-mini-n3-net1",
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
                    "name": "oai-5g-mini-n3-net1",
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
    volume_config = make_volume_config()
    liveness_probe = make_liveness_probe()
    readiness_probe = make_readiness_probe()
    kubernetes_resources = make_kubernetes_resources(config)
    return {
        "version": 3,
        "kubernetesResources": kubernetes_resources,
        "containers": [
            {
                "name": "oai-spgwu",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "ports": ports,
                "envConfig": {
                    "GW_ID": config["gw-id"],
                    "MNC03": config["mnc03"],
                    "MCC": config["mcc"],
                    "REALM": config["realm"],
                    "PID_DIRECTORY": config["pid-directory"],
                    "SGW_INTERFACE_NAME_FOR_S1U_S12_S4_UP": config["sgw-interface-name-for-s1u-s12-s4-up"],
                    "THREAD_S1U_PRIO": config["thread-s1u-prio"],
                    "S1U_THREADS": config["s1u-threads"],
                    "SGW_INTERFACE_NAME_FOR_SX": config["sgw-interface-name-for-sx"],
                    "THREAD_SX_PRIO": config["thread-sx-prio"],
                    "SX_THREADS": config["sx-threads"],
                    "PGW_INTERFACE_NAME_FOR_SGI": config["pgw-interface-name-for-sgi"],
                    "THREAD_SGI_PRIO": config["thread-sgi-prio"],
                    "SGI_THREADS": config["sgi-threads"],
                    "NETWORK_UE_NAT_OPTION": config["network-ue-nat-option"],
                    "GTP_EXTENSION_HEADER_PRESENT": config["gtp-extention-header-present"],
                    "NETWORK_UE_IP": config["network-ue-ip"],
                    "SPGWC0_IP_ADDRESS": config["spgwc0-ip-address"],
                    "BYPASS_UL_PFCP_RULES": config["bypass-ul-pfcp-rules"],
                    "ENABLE_5G_FEATURES": config["enable-5g-features"],
                    "REGISTER_NRF": config["register-nrf"],
                    "USE_FQDN_NRF": config["use-fqdn-nrf"],
                    "NRF_IPV4_ADDRESS": config["nrf-ipv4-address"],
                    "NRF_PORT": config["nrf-port"],
                    "NRF_API_VERSION": config["nrf-api-version"],
                    "NRF_FQDN": config["nrf-fqdn"],
                    "NSSAI_SST_0": config["nssai-sst-0"],
                    "NSSAI_SD_0": config["nssai-sd-0"],
                    "DNN_0": config["dnn-0"],
                    "NSSAI_SST_1": config["nssai-sst-1"],
                    "NSSAI_SD_1": config["nssai-sd-1"],
                    "DNN_1": config["dnn-1"],
                    "NSSAI_SST_2": config["nssai-sst-2"],
                    "NSSAI_SD_2": config["nssai-sd-2"],
                    "DNN_2": config["dnn-2"],
                    "NSSAI_SST_3": config["nssai-sst-3"],
                    "NSSAI_SD_3": config["nssai-sd-3"],
                    "DNN_3": config["dnn-3"],
                    "UPF_FQDN_5G": config["upf-fqdn-5g"],
                    "MNC": config["mnc"],
                    # "TAC": config["tac"],
                },
                "volumeConfig": volume_config,
                "kubernetes": {
                    "livenessProbe": liveness_probe,
                    "readinessProbe": readiness_probe,
                    "securityContext": {
                        "privileged": True
                    }
                }
            }
        ]
    }