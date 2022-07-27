import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)

def make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """make mysql ports details"""
    return [
        {
            "name": "mysql",
            "containerPort": config["mysql-port"]
        },
        {
            "name": "mysqlx",
            "containerPort": config["mysqlx-port"]
        }
    ]

def make_pod_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    """make pod spec details"""
    ports = make_pod_ports(config)
    return {
        "version": 3,
        "containers": [
            {
                "name": "mysql",
                "image": config["image"],
                "imagePullPolicy": "Never", # todo: use IfNotPresent,
                "ports": ports,
                "envConfig": {
                    "TZ": config["time-zone"],
                    "MYSQL_DATABASE": config["mysql-db"],
                    "MYSQL_USER": config["mysql-user"],
                    "MYSQL_PASSWORD": config["mysql-password"],
                    "MYSQL_ROOT_PASSWORD": config["mysql-root-password"]
                }
            }
        ]
    }