def normalize_telemetry(data: dict) -> dict:
    """
    Converts collector/scenario telemetry into the standard
    format used by the intelligence modules.
    """

    if not isinstance(data, dict):
        raise ValueError("Telemetry must be a dictionary")

    # Support both a complete scenario and a telemetry dictionary.
    telemetry = data.get("telemetry", data)

    if not isinstance(telemetry, dict):
        telemetry = {}

    aliases = {
        "latency": ["latency", "latency_ms"],
        "packet_loss": ["packet_loss", "packet_loss_pct"],
        "jitter": ["jitter", "jitter_ms"],
        "cpu_usage": ["cpu_usage", "cpu_utilization_pct"],
        "memory_usage": ["memory_usage", "memory_utilization_pct"],
    }

    normalized = {}

    for standard_key, possible_keys in aliases.items():
        value = None

        for key in possible_keys:
            if telemetry.get(key) is not None:
                value = telemetry[key]
                break

        normalized[standard_key] = value

    # CPU and memory may be inside the devices list.
    devices = data.get("devices", [])

    if isinstance(devices, list):
        for metric, device_key in [
            ("cpu_usage", "cpu_utilization_pct"),
            ("memory_usage", "memory_utilization_pct"),
        ]:
            device_values = [
                device.get(device_key)
                for device in devices
                if isinstance(device, dict)
                and device.get(device_key) is not None
            ]

            if device_values:
                try:
                    device_max = max(float(v) for v in device_values)

                    current = normalized[metric]
                    if current is None or device_max > float(current):
                        normalized[metric] = device_max

                except (ValueError, TypeError):
                    pass

    # Convert numeric strings to numbers.
    for key, value in normalized.items():
        if value is not None:
            try:
                normalized[key] = float(value)
            except (ValueError, TypeError):
                normalized[key] = None

    return normalized