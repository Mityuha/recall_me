try:
    from loguru import logger
except ModuleNotFoundError:
    from unittest.mock import Mock

    logger = Mock()
    logger.debug = print
    logger.info = print
    logger.warning = print
    logger.error = print
