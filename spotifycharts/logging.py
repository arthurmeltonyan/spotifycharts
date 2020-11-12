from loguru import logger

from spotifycharts import settings

logger.remove()
logger.add(settings.LOG_FILE_NAME,
           level=settings.LOG_LEVEL,
           format=settings.LOG_FORMAT,
           filter=None,
           colorize=None,
           serialize=False,
           backtrace=True,
           diagnose=True,
           enqueue=False,
           catch=True,
           rotation=settings.LOG_ROTATION,
           retention=settings.LOG_RETENTION,
           compression=None,
           delay=False,
           mode='a',
           buffering=settings.LOG_BUFFERING,
           encoding=settings.LOG_ENCODING)
