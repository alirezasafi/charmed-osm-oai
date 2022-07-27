#!/usr/bin/env python3
# Copyright 2022 Ubuntu
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""
import sys
sys.path.append('lib')

import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus

from pod_spec import make_pod_spec

logger = logging.getLogger(__name__)


class MysqlCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self._stored.set_default(spec=None)
        
        # observe 
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.start, self._on_config_changed)
        # self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)

    def _apply_spec(self):
        if not self.framework.model.unit.is_leader():
            return
        spec = make_pod_spec(self.framework.model.config)
        if spec == self._stored.spec:
            return
        self.framework.model.pod.set_spec(spec)
        self._stored.spec = spec
 
    def _on_config_changed(self, event):
        """change configuration"""
        unit = self.model.unit
        unit.status = MaintenanceStatus("Apply new pod spec")
        self._apply_spec()
        unit.status = ActiveStatus("Ready")


if __name__ == "__main__":
    main(MysqlCharm)
