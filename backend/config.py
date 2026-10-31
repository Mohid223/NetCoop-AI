import os


class Settings:

    APP_NAME = "NetCoop AI"

    APP_VERSION = "2.0.0"

    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    DEFAULT_PING_HOST = os.getenv(
        "DEFAULT_PING_HOST",
        "8.8.8.8"
    )

    DIAGNOSTIC_TIMEOUT = int(
        os.getenv("DIAGNOSTIC_TIMEOUT", "10")
    )

    MAX_DIAGNOSTIC_SAMPLES = int(
        os.getenv("MAX_DIAGNOSTIC_SAMPLES", "20")
    )

    AUTO_REMEDIATION_ENABLED = False

    HUMAN_APPROVAL_REQUIRED = True


settings = Settings()