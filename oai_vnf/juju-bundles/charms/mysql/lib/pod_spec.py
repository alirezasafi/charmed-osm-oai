import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make mysql ports details"""
    return [
        {
            "name": "mysql",
            "protocol": "TCP",
            "containerPort": config["mysql-port"]
        },
        {
            "name": "mysqlx",
            "protocol": "TCP",
            "containerPort": config["mysqlx-port"]
        }
    ]


def healthcheck_config() -> str:
    with open('scripts/healthcheck.sh') as text_file:
        return text_file.read()


def oai_db_initialization() -> str:
    with open('initialization/oai_db.sql') as text_file:
        return text_file.read()


def make_volume_config() -> List[Dict[str, Any]]:
    return [
        {
            "name": "migrations",
            "mountPath": "/docker-entrypoint-initdb.d",
            "files": [
                {
                    "path": "oai_db.sql",
                    "content": oai_db_initialization()
                }
            ]
        }
    ]



def make_liveness_probe() -> Dict[str, Any]:
    return {
        "exec": {
            "command": ["mysqladmin", "ping"]  
        },
        "initialDelaySeconds": 50,
        "periodSeconds": 15,
        "timeoutSeconds": 10,
        "successThreshold": 1,
        "failureThreshold": 3
    }


def make_kubernetes_resources() -> Dict[str, Any]:
    return {
        "pod": {
            "securityContext": {
                "runAsUser": 999,
                "fsGroup": 999
            }
        }
    }

    
def make_readiness_probe() -> Dict[str, Any]:
    return {
        "exec": {
            "command": ["mysqladmin", "ping"]  
        },
        "initialDelaySeconds": 15,
        "periodSeconds": 15,
        "timeoutSeconds": 10,
        "successThreshold": 1,
        "failureThreshold": 3
    }


def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    volume_config = make_volume_config()
    liveness_probe = make_liveness_probe()
    readiness_probe = make_readiness_probe()
    kubernetes_resources = make_kubernetes_resources()
    return {
        "version": 3,
        "kubernetesResources": kubernetes_resources,
        "containers": [
            {
                "name": "mysql",
                "image": config["image"],
                "imagePullPolicy": "IfNotPresent",
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "MYSQL_DATABASE": config["mysql-db"],
                    "MYSQL_USER": config["mysql-user"],
                    "MYSQL_PASSWORD": config["mysql-password"],
                    "MYSQL_ROOT_PASSWORD": config["mysql-root-password"],
                    "MYSQL_ALLOW_EMPTY_PASSWORD": config["mysql-allow-empty-password"]
                },
                "volumeConfig": volume_config,
                "kubernetes": {
                    "livenessProbe": liveness_probe,
                    "readinessProbe": readiness_probe
                }
            }
        ]
    }