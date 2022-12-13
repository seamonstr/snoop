from logging.config import fileConfig


def configure_logging(logging_cfg: str):
    """
    Expects a logging config filename, either absolute or relative to CWD
    """
    fileConfig(logging_cfg)
