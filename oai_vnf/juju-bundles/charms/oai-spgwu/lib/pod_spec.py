import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make mysql ports details"""
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


def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    return {
        "version": 3,
        "containers": [
            {
                "name": "oai-spgwu",
                "image": config["image"],
                "imagePullPolicy": "Never",  # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "PID_DIRECTORY": config["pid-directory"],
                    "SGW_INTERFACE_NAME_FOR_S1U_S12_S4_UP": config["sgw-interface-name-for-s1u-s12-s4-up"],
                    "SGW_INTERFACE_NAME_FOR_SX": config["sgw-interface-name-for-sx"],
                    "PGW_INTERFACE_NAME_FOR_SGI": config["pgw-interface-name-for-sgi"],
                    "NETWORK_UE_NAT_OPTION": config["network-ue-nat-option"],
                    "NETWORK_UE_IP": config["network-ue-ip"],
                    "SPGWC0_IP_ADDRESS": config["spgwc0-ip-address"],
                    "BYPASS_UL_PFCP_RULES": config["bypass-ul-pfcp-rules"],
                    "MCC": config["mcc"],
                    "MNC": config["mnc"],
                    "MNC03": config["mnc03"],
                    "TAC": config["tac"],
                    "GW_ID": config["gw-id"],
                    "REALM": config["realm"],
                    "ENABLE_5G_FEATURES": config["enable-5g-features"],
                    "REGISTER_NRF": config["register-nrf"],
                    "USE_FQDN_NRF": config["use-fqdn-nrf"],
                    "UPF_FQDN_5G": config["upf-fqdn-5g"],
                    "NRF_IPV4_ADDRESS": config["nrf-ipv4-address"],
                    "NRF_PORT": config["nrf-port"],
                    "NRF_API_VERSION": config["nrf-api-version"],
                    "NRF_FQDN": config["nrf-fqdn"],
                    "NSSAI_SST_0": config["nssai-sst-0"],
                    "NSSAI_SD_0": config["nssai-sd-0"],
                    "DNN_0": config["dnn-0"]
                }
            }
        ]
    }