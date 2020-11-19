from loguru import logger

from spotifycharts import settings

logger.remove()
logger.add(f'all_{settings.LOG_FILE_NAME}',
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
logger.add(f'info_{settings.LOG_FILE_NAME}',
           level=settings.LOG_LEVEL,
           format=settings.LOG_FORMAT,
           filter=lambda record: record['level'].name == 'INFO',
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
logger.add(f'warning_{settings.LOG_FILE_NAME}',
           level=settings.LOG_LEVEL,
           format=settings.LOG_FORMAT,
           filter=lambda record: record['level'].name == 'WARNING',
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
