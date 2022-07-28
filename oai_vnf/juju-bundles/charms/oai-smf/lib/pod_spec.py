import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make mysql ports details"""
    return [
        {
            "name": "oai-smf",
            "protocol": "UDP",
            "containerPort": config["oai-smf"]
        },
        {
            "name": "http1",
            "protocol": "TCP",
            "containerPort": config["http1"]
        },
        {
            "name": "http1",
            "protocol": "TCP",
            "containerPort": config["http2"]
        }
    ]


def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    return {
        "version": 3,
        "containers": [
            {
                "name": "oai-smf",
                "image": config["image"],
                "imagePullPolicy": "Never",  # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "INSTANCE": config["instance"],
                    "PID_DIRECTORY": config["pid-directory"],
                    "SMF_INTERFACE_NAME_FOR_N4": config["smf-interface-name-for-n4"],
                    "SMF_INTERFACE_NAME_FOR_SBI": config["smf-interface-name-for-sbi"],
                    "SMF_INTERFACE_PORT_FOR_SBI": config["smf-interface-port-for-sbi"],
                    "SMF_INTERFACE_HTTP2_PORT_FOR_SBI": config["smf-interface-http2-port-for-sbi"],
                    "SMF_API_VERSION": config["smf-api-version"],
                    "DEFAULT_DNS_IPV4_ADDRESS": config["default-dns-ipv4-address"],
                    "DEFAULT_DNS_SEC_IPV4_ADDRESS": config["default-dns-sec-ipv4-address"],
                    "AMF_IPV4_ADDRESS": config["amf-ipv4-address"],
                    "AMF_PORT": config["amf-port"],
                    "AMF_API_VERSION": config["amf-api-version"],
                    "AMF_FQDN": config["amf-fqdn"],
                    "UDM_IPV4_ADDRESS": config["udm-ipv4-address"],
                    "UDM_PORT": config["udm-port"],
                    "UDM_API_VERSION": config["udm-api-version"],
                    "UDM_FQDN": config["udm-fqdn"],
                    "UPF_IPV4_ADDRESS": config["upf-ipv4-address"],
                    "UPF_FQDN_0": config["upf-fqdn-0"],
                    "NRF_IPV4_ADDRESS": config["nrf-ipv4-address"],
                    "NRF_PORT": config["nrf-port"],
                    "NRF_API_VERSION": config["nrf-api-version"],
                    "USE_LOCAL_SUBSCRIPTION_INFO": config["use-local-subscription-info"],
                    "NRF_FQDN": config["nrf-fqdn"],
                    "REGISTER_NRF": config["register-nrf"],
                    "DISCOVER_UPF": config["discover-upf"],
                    "USE_FQDN_DNS": config["use-fqdn-dns"],
                    "DNN_RANGE1": config["dnn-range1"],
                    "DNN_RANGE0": config["dnn-range0"],
                    "DNN_NI1": config["dnn-ni1"]
                }
            }
        ]
    }