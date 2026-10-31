class BandwidthTest:

    def run(self, test_server=None):

        if not test_server:
            return {
                "test": "bandwidth",
                "success": False,
                "status": "not_configured",
                "message": (
                    "Configure an authorized iperf3 test server "
                    "before running bandwidth measurements."
                )
            }

        return {
            "test": "bandwidth",
            "success": False,
            "status": "integration_required",
            "message": "iperf3 integration is not implemented yet."
        }