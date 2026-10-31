from backend.diagnostics.ping_test import PingTest
from backend.diagnostics.dns_test import DNSTest
from backend.diagnostics.packet_loss_test import PacketLossTest
from backend.diagnostics.latency_test import LatencyTest
from backend.diagnostics.interface_test import InterfaceTest
from backend.diagnostics.bandwidth_test import BandwidthTest

class DiagnosticRunner:
    def run_all(self, host="8.8.8.8", bandwidth_server=None):
        tests = []

        runners = [
            ("ping", lambda: PingTest().run(host=host)),
            ("dns", lambda: DNSTest().run(hostname="example.com")),
            ("packet_loss", lambda: PacketLossTest().run(host=host)),
            ("latency", lambda: LatencyTest().run(host=host)),
            ("interfaces", lambda: InterfaceTest().run()),
            ("bandwidth", lambda: BandwidthTest().run(
                test_server=bandwidth_server
            )),
        ]

        for name, run_test in runners:
            try:
                result = run_test()
                tests.append(result)
            except Exception as error:
                tests.append({
                    "test": name,
                    "success": False,
                    "error": str(error)
                })

        return tests