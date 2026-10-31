"""Analyzes WiFi quality and connectivity scope."""
from backend.agents.base_agent import BaseAgent
from backend.core.schema import MsgType


class ConnectivityAgent(BaseAgent):
    name = "connectivity_agent"

    def handle(self, message):
        if message.msg_type != MsgType.REQUEST:
            return

        incident_id = message.incident_id
        wifi = message.payload.get("wifi", {}) or {}
        devices = message.payload.get("devices", [])

        findings = []
        evidence = []
        affected = []

        # WiFi Signal
        signal = wifi.get("signal_dbm")
        if signal is not None:
            try:
                signal = float(signal)
                if signal < -75:
                    findings.append("weak_wifi_signal")
                    evidence.append({
                        "metric": "signal_dbm",
                        "value": signal,
                        "interpretation": "Weak WiFi signal (< -75 dBm)",
                    })
            except (TypeError, ValueError):
                self.send(
                    "fault_correlation_agent",
                    MsgType.ERROR,
                    incident_id,
                    {"error": f"bad signal_dbm={signal!r}"},
                )

        # Retransmission rate
        retrans = wifi.get("retransmission_rate_pct")
        if retrans is not None:
            try:
                retrans = float(retrans)
                if retrans > 15:
                    findings.append("high_retransmission")
                    evidence.append({
                        "metric": "retransmission_rate_pct",
                        "value": retrans,
                        "interpretation": "High WiFi retransmission rate",
                    })
            except (TypeError, ValueError):
                pass

        confidence = min(1.0, len(findings) / 2.0) if findings else 0.1

        self.send(
            recipient="fault_correlation_agent",
            msg_type=MsgType.FINDING,
            incident_id=incident_id,
            payload={
                "agent": self.name,
                "anomalies": findings,
                "evidence": evidence,
                "affected_devices": affected,
            },
            confidence=confidence,
        )