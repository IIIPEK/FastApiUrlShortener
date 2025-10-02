# app/core/logging_config.py
from logging.config import dictConfig

def setup_logging(level: str = "INFO") -> None:
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,  # uvicorn logging
        "formatters": {
            "default": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "default"}
        },
        "loggers": {
            "": {"handlers": ["console"], "level": level},  # root
            "uvicorn": {"level": level},
            "uvicorn.error": {"level": level},
            "uvicorn.access": {"level": level},
            # namespace of our app:
            "app": {"level": level, "handlers": ["console"], "propagate": False},
        }
    })
