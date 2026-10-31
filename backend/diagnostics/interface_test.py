import socket


class InterfaceTest:

    def run(self):

        interfaces = []

        try:
            for name in socket.if_nameindex():
                interfaces.append({
                    "index": name[0],
                    "name": name[1]
                })

            return {
                "test": "network_interfaces",
                "success": True,
                "interfaces": interfaces
            }

        except OSError as error:
            return {
                "test": "network_interfaces",
                "success": False,
                "error": str(error)
            }