#!/usr/bin/env python3
import sys
sys.path.append('lib')

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import ActiveStatus, BlockedStatus, WaitingStatus, MaintenanceStatus
from pod_spec import make_pod_spec

logger = logging.getLogger(__name__)

VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]


class OaiHssCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self._stored.set_default(spec=None)
        self.framework.observe(self.on.start, self._on_start)
        # self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_start(self, event):
        """container start hook"""
        unit = self.model.unit
        unit.status = MaintenanceStatus("Apply hss pod spec")
        if not self.framework.model.unit.is_leader():
            return
        spec = make_pod_spec(self.framework.model.config)
        self.framework.model.pod.set_spec(spec)
        self._stored.spec = spec
        unit.status = ActiveStatus("HSS service is ready")


if __name__ == "__main__":  # pragma: nocover
    main(OaiHssCharm)
