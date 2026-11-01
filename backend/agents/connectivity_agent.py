
"""Analyzes Wi-Fi, DNS, DHCP and network connectivity."""

from backend.agents.base_agent import BaseAgent
from backend.core.schema import MsgType


class ConnectivityAgent(BaseAgent):
    name = "connectivity_agent"

    def handle(self, message):
        if message.msg_type != MsgType.REQUEST:
            return

        incident_id = message.incident_id
        wifi = message.payload.get("wifi", {}) or {}
        dns = message.payload.get("dns", {}) or {}
        dhcp = message.payload.get("dhcp", {}) or {}
        devices = message.payload.get("devices", [])

        findings = []
        evidence = []
        affected = []

        def add_affected(device_id):
            if isinstance(device_id, str) and device_id.strip():
                if device_id not in affected:
                    affected.append(device_id)

        # Wi-Fi signal strength
        signal = wifi.get("signal_dbm")

        if signal is not None:
            try:
                signal = float(signal)

                if signal < -75:
                    findings.append("weak_wifi_signal")
                    evidence.append({
                        "metric": "signal_dbm",
                        "value": signal,
                        "interpretation": "Weak Wi-Fi signal below -75 dBm",
                    })

            except (TypeError, ValueError):
                self.send(
                    "fault_correlation_agent",
                    MsgType.ERROR,
                    incident_id,
                    {"error": "Invalid Wi-Fi signal value", "agent": self.name},
                )

        # Wi-Fi retransmissions
        retrans = wifi.get("retransmission_rate_pct")

        if retrans is not None:
            try:
                retrans = float(retrans)

                if retrans > 15:
                    findings.append("high_retransmission")
                    evidence.append({
                        "metric": "retransmission_rate_pct",
                        "value": retrans,
                        "interpretation": "High Wi-Fi retransmission rate",
                    })

            except (TypeError, ValueError):
                self.send(
                    "fault_correlation_agent",
                    MsgType.ERROR,
                    incident_id,
                    {"error": "Invalid Wi-Fi retransmission value", "agent": self.name},
                )

        # DNS checks
        if isinstance(dns, dict) and dns:
            dns_status = str(dns.get("status", "")).lower()
            resolution_success = dns.get("resolution_success")
            server_reachable = dns.get("server_reachable")
            failure_rate = dns.get("failure_rate_pct", 0)

            dns_failed = (
                dns_status in ("failed", "failure", "down", "unavailable")
                or resolution_success is False
                or server_reachable is False
            )

            try:
                dns_failed = dns_failed or float(failure_rate) > 20
            except (TypeError, ValueError):
                self.send(
                    "fault_correlation_agent",
                    MsgType.ERROR,
                    incident_id,
                    {"error": "Invalid DNS failure rate", "agent": self.name},
                )

            if dns_failed:
                findings.append("dns_failure")
                evidence.append({
                    "metric": "dns_status",
                    "value": dns,
                    "interpretation": "DNS resolution or DNS server health check failed",
                })

        # DHCP checks
        if isinstance(dhcp, dict) and dhcp:
            dhcp_status = str(dhcp.get("status", "")).lower()
            lease_success = dhcp.get("lease_success")
            pool_exhausted = dhcp.get("address_pool_exhausted")
            failure_rate = dhcp.get("lease_failure_rate_pct", 0)

            dhcp_failed = (
                dhcp_status in ("failed", "failure", "down", "unavailable")
                or lease_success is False
                or pool_exhausted is True
            )

            try:
                dhcp_failed = dhcp_failed or float(failure_rate) > 20
            except (TypeError, ValueError):
                self.send(
                    "fault_correlation_agent",
                    MsgType.ERROR,
                    incident_id,
                    {"error": "Invalid DHCP failure rate", "agent": self.name},
                )

            if dhcp_failed:
                findings.append("dhcp_failure")
                evidence.append({
                    "metric": "dhcp_status",
                    "value": dhcp,
                    "interpretation": "DHCP lease or IP address assignment failed",
                })

        # Associate connectivity findings with supplied devices.
        if findings and isinstance(devices, list):
            for device in devices:
                if isinstance(device, dict):
                    add_affected(device.get("device_id"))

        confidence = min(1.0, len(set(findings)) / 2.0) if findings else 0.1

        self.send(
            recipient="fault_correlation_agent",
            msg_type=MsgType.FINDING,
            incident_id=incident_id,
            payload={
                "agent": self.name,
                "anomalies": sorted(set(findings)),
                "evidence": evidence,
                "affected_devices": affected,
            },
            confidence=confidence,
        )
