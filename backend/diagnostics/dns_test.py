import socket
import time


class DNSTest:

    def run(self, hostname="example.com"):

        start = time.perf_counter()

        try:
            addresses = socket.getaddrinfo(
                hostname,
                None,
                type=socket.SOCK_STREAM
            )

            duration = (time.perf_counter() - start) * 1000

            unique_ips = sorted({
                item[4][0] for item in addresses
            })

            return {
                "test": "dns_resolution",
                "hostname": hostname,
                "success": True,
                "resolved_addresses": unique_ips,
                "resolution_time_ms": round(duration, 2)
            }

        except socket.gaierror as error:
            return {
                "test": "dns_resolution",
                "hostname": hostname,
                "success": False,
                "error": str(error)
            }