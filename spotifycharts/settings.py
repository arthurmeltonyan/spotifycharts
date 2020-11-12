import environs
configuration = environs.Env()
configuration.read_env('spotifycharts/configuration.env')


SPOTIFY_CHARTS_URL = configuration.str('SPOTIFY_CHARTS_URL')


NAME_CODES = {configuration.list('VIRAL50')[0]: configuration.list('VIRAL50')[1],
              configuration.list('TOP200')[0]: configuration.list('TOP200')[1]}
PERIODICITY_CODES = {configuration.list('DAILY')[0]: configuration.list('DAILY')[1],
                     configuration.list('WEEKLY')[0]: configuration.list('WEEKLY')[1]}


DEFAULT_REGION_NAMES = configuration.list('DEFAULT_REGION_NAMES')
DEFAULT_MONTH_PERIOD = configuration.int('DEFAULT_MONTH_PERIOD')
FOUNDATION_DATE = configuration.str('FOUNDATION_DATE')


CHART_ERROR_CSS = configuration.str('CHART_ERROR_CSS')
LOST_CHART_CSS = configuration.str('LOST_CHART_CSS')
DATE_CSS = configuration.str('DATE_CSS')
REGION_CSS = configuration.str('REGION_CSS')
DATE_CODE_ATTRIBUTE = configuration.str('DATE_CODE_ATTRIBUTE')
REGION_CODE_ATTRIBUTE = configuration.str('REGION_CODE_ATTRIBUTE')
HTML_DATE_FORMAT = configuration.str('HTML_DATE_FORMAT')
URL_DATE_FORMAT = configuration.str('URL_DATE_FORMAT')
URL_DATE_DELIMITER = configuration.str('URL_DATE_DELIMITER')


VIRAL50_CHART_FILE_HEADER = configuration.str('VIRAL50_CHART_FILE_HEADER')
TOP200_CHART_FILE_HEADER = configuration.str('TOP200_CHART_FILE_HEADER')
FILE_DELIMITER = configuration.str('FILE_DELIMITER')
FILE_ENCODING = configuration.str('FILE_ENCODING')
FILE_EXTENSION = configuration.str('FILE_EXTENSION')
FILE_DATE_FORMAT = configuration.str('FILE_DATE_FORMAT')
VIRAL50_CHART_COLUMN_NAMES = configuration.list('VIRAL50_CHART_COLUMN_NAMES')
TOP200_CHART_COLUMN_NAMES = configuration.list('TOP200_CHART_COLUMN_NAMES')


PROGRESSBAR_TIME_FORMAT = configuration.str('PROGRESSBAR_TIME_FORMAT')


NAME_ERROR = configuration.str('NAME_ERROR')
PERIODICITY_ERROR = configuration.str('PERIODICITY_ERROR')
REGION_NAME_ERROR = configuration.str('REGION_NAME_ERROR')
BEGIN_DATE_ERROR = configuration.str('BEGIN_DATE_ERROR')
END_DATE_ERROR = configuration.str('END_DATE_ERROR')
DATE_RANGE_ERROR = configuration.str('DATE_RANGE_ERROR')
CPU_COUNT_ERROR = configuration.str('CPU_COUNT_ERROR')
DIRECTORY_PATH_ERROR = configuration.str('DIRECTORY_PATH_ERROR')


LOG_FILE_NAME = configuration.str('LOG_FILE_NAME')
LOG_LEVEL = configuration.str('LOG_LEVEL')
LOG_FORMAT = configuration.str('LOG_FORMAT')
LOG_ROTATION = configuration.str('LOG_ROTATION')
LOG_RETENTION = configuration.str('LOG_RETENTION')
LOG_BUFFERING = configuration.int('LOG_BUFFERING')
LOG_ENCODING = configuration.str('LOG_ENCODING')
LOG_REGIONS_DOWNLOAD_WARNING = configuration.str('LOG_REGIONS_DOWNLOAD_WARNING')
LOG_REGIONS_DOWNLOAD_INFO = configuration.str('LOG_REGIONS_DOWNLOAD_INFO')
LOG_DATES_DOWNLOAD_WARNING = configuration.str('LOG_DATES_DOWNLOAD_WARNING')
LOG_DATES_DOWNLOAD_INFO = configuration.str('LOG_DATES_DOWNLOAD_INFO')
LOG_CHART_DOWNLOAD_WARNING = configuration.str('LOG_CHART_DOWNLOAD_WARNING')
LOG_CHART_DOWNLOAD_INFO = configuration.str('LOG_CHART_DOWNLOAD_INFO')
