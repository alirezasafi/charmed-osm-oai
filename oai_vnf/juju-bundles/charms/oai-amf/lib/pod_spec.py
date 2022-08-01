import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make mysql ports details"""
    return [
        {
            "name": "oai-amf",
            "protocol": "TCP",  # todo: should be SCTP
            "containerPort": config["oai-amf"]
        },
        {
            "name": "http1",
            "protocol": "TCP",
            "containerPort": config["http1"]
        },
        {
            "name": "http2",
            "protocol": "TCP",
            "containerPort": config["http2"]
        },
    ]


def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    return {
        "version": 3,
        "containers": [
            {
                "name": "oai-amf",
                "image": config["image"],
                "imagePullPolicy": "Never",  # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "INSTANCE": config["instance"],
                    "PID_DIRECTORY": config["pid-directory"],
                    "MCC": config["mcc"],
                    "MNC": config["mnc"],
                    "REGION_ID": config["region-id"],
                    "AMF_SET_ID": config["amf-set-id"],
                    "SERVED_GUAMI_MCC_0": config["served-guami-mcc-0"],
                    "SERVED_GUAMI_MNC_0": config["served-guami-mnc-0"],
                    "SERVED_GUAMI_REGION_ID_0": config["served-guami-region-id-0"],
                    "SERVED_GUAMI_AMF_SET_ID_0": config["served-guami-amf-set-id-0"],
                    "SERVED_GUAMI_MCC_1": config["served-guami-mcc-1"],
                    "SERVED_GUAMI_MNC_1": config["served-guami-mnc-1"],
                    "SERVED_GUAMI_REGION_ID_1": config["served-guami-region-id-1"],
                    "SERVED_GUAMI_AMF_SET_ID_1": config["served-guami-amf-set-id-1"],
                    "PLMN_SUPPORT_MCC": config["plmn-support-mcc"],
                    "PLMN_SUPPORT_MNC": config["plmn-support-mnc"],
                    "PLMN_SUPPORT_TAC": config["plmn-support-tac"],
                    "SST_0": config["sst-0"],
                    "SD_0": config["sd-0"],
                    "SST_1": config["sst-1"],
                    "SD_1": config["sd-1"],
                    "AMF_INTERFACE_NAME_FOR_NGAP": config["amf-interface-name-for-ngap"],
                    "AMF_INTERFACE_NAME_FOR_N11": config["amf-interface-name-for-n11"],
                    "SMF_INSTANCE_ID_0": config["smf-instance-id-0"],
                    "SMF_FQDN_0": config["smf-fqdn-0"],
                    "SMF_IPV4_ADDR_0": config["smf-ipv4-addr-0"],
                    "SMF_HTTP_VERSION_0": config["smf-http-version-0"],
                    "SMF_INSTANCE_ID_1": config["smf-instance-id-1"],
                    "SELECTED_0": config["selected-0"],
                    "SMF_FQDN_1": config["smf-fqdn-1"],
                    "SMF_IPV4_ADDR_1": config["smf-ipv4-addr-1"],
                    "SMF_HTTP_VERSION_1": config["smf-http-version-1"],
                    "SELECTED_1": config["selected-1"],
                    "MYSQL_SERVER": config["mysql-server"],
                    "MYSQL_USER": config["mysql-user"],
                    "MYSQL_PASS": config["mysql-pass"],
                    "MYSQL_DB": config["mysql-db"],
                    "OPERATOR_KEY": config["operator-key"],
                    "NRF_IPV4_ADDRESS": config["nrf-ipv4-address"],
                    "NRF_PORT": config["nrf-port"],
                    "NRF_API_VERSION": config["nrf-api-version"],
                    "NRF_FQDN": config["nrf-fqdn"],
                    "NF_REGISTRATION": config["nf-registration"],
                    "SMF_SELECTION": config["smf-selection"],
                    "USE_FQDN_DNS": config["use-fqdn-dns"],
                    "EXTERNAL_AUSF": config["external-ausf"],
                    "AUSF_IPV4_ADDRESS": config["ausf-ipv4-address"],
                    "AUSF_PORT": config["ausf-port"],
                    "AUSF_FQDN": config["ausf-fqdn"],
                    "AUSF_API_VERSION": config["ausf-api-version"]
                }
            }
        ]
    }