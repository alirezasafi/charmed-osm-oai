import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make nrf ports details"""
    return [
        {
            "name": "http1",
            "protocol": "TCP",
            "containerPort": config["http1"]
        },
        {
            "name": "http2",
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
                "name": "oai-nrf",
                "image": config["image"],
                "imagePullPolicy": "Never",  # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "INSTANCE": config["instance"],
                    "PID_DIRECTORY": config["pid-directory"],
                    "NRF_INTERFACE_NAME_FOR_SBI": config["nrf-interface-name-for-sbi"],
                    "NRF_INTERFACE_PORT_FOR_SBI": config["nrf-interface-port-for-sbi"],
                    "NRF_INTERFACE_HTTP2_PORT_FOR_SBI": config["nrf-interface-http2-port-for-sbi"],
                    "NRF_API_VERSION": config["nrf-api-version"]
                }
            }
        ]
    }