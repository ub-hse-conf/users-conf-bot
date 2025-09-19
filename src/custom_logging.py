import structlog

from src.config import IS_PROD


def init_logging(instance_id: str, version: str):
    if IS_PROD:
        __configure_prod_logging(instance_id, version)
    else:
        __configure_dev_logging()


def __configure_dev_logging():
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ]
    )

def __configure_prod_logging(instance_id: str, version: str):
    def add_instance_id(_, __, event_dict):
        event_dict["instance_id"] = instance_id
        return event_dict

    def add_stream_name(_, __, event_dict):
        event_dict["stream_name"] = "frontend"
        return event_dict

    def add_service_name(_, __, event_dict):
        event_dict["service_name"] = "cub-telegram-bot"
        return event_dict

    def add_version(_, __, event_dict):
        event_dict["version"] = version
        return event_dict

    exception_transformer = structlog.tracebacks.ExceptionDictTransformer()
    exception_format_json = structlog.processors.ExceptionRenderer(exception_transformer)

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", key="@timestamp"),
            add_instance_id,
            add_stream_name,
            add_service_name,
            add_version,
            structlog.contextvars.merge_contextvars,
            exception_format_json,
            structlog.processors.EventRenamer("message"),
            structlog.processors.JSONRenderer(),
        ]
    )