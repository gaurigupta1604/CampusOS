import logging, structlog
def configure_logging():
    logging.basicConfig(level=logging.INFO,format="%(message)s")
    structlog.configure(processors=[structlog.contextvars.merge_contextvars,structlog.processors.add_log_level,structlog.processors.TimeStamper(fmt="iso"),structlog.processors.JSONRenderer()])
    return structlog.get_logger()
logger=configure_logging()
