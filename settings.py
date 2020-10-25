import typing_extensions as te

import environs
configuration = environs.Env()
configuration.read_env('spotifycharts/configuration.env')

SPOTIFY_CHARTS_URL: te.Final = configuration.str('URL')


NAME_CODES: te.Final = {configuration.list('VIRAL50')[0]: configuration.list('VIRAL50')[1],
                        configuration.list('TOP200')[0]: configuration.list('TOP200')[1]}
PERIODICITY_CODES: te.Final = {configuration.list('DAILY')[0]: configuration.list('DAILY')[1],
                               configuration.list('WEEKLY')[0]: configuration.list('WEEKLY').split(':')[1]}


DEFAULT_MONTH_PERIOD: te.Final = configuration.int('DEFAULT_MONTH_PERIOD')
DEFAULT_REGION_NAME: te.Final = configuration.str('DEFAULT_REGION_NAME')
FOUNDATION_DATE: te.Final = configuration.str('FOUNDATION_DATE')


CHART_ERROR_CSS: te.Final = configuration.str('CHART_ERROR_CSS')
LOST_CHART_CSS: te.Final = configuration.str('LOST_CHART_CSS')
DATE_CSS: te.Final = configuration.str('DATE_CSS')
REGION_CSS: te.Final = configuration.str('REGION_CSS')
DATE_CODE_ATTRIBUTE: te.Final = configuration.str('DATE_CODE_ATTRIBUTE')
REGION_CODE_ATTRIBUTE: te.Final = configuration.str('REGION_CODE_ATTRIBUTE')
HTML_DATE_FORMAT: te.Final = configuration.str('HTML_DATE_FORMAT')
URL_DATE_FORMAT: te.Final = configuration.str('URL_DATE_FORMAT')
URL_DATE_DELIMITER: te.Final = configuration.str('URL_DATE_DELIMITER')


VIRAL50_CHART_FILE_HEADER: te.Final = configuration.str('VIRAL50_CHART_FILE_HEADER')
TOP200_CHART_FILE_HEADER: te.Final = configuration.str('TOP200_CHART_FILE_HEADER')
FILE_DELIMITER: te.Final = configuration.str('FILE_DELIMITER')
FILE_ENCODING: te.Final = configuration.str('FILE_ENCODING')
FILE_EXTENSION: te.Final = configuration.str('FILE_EXTENSION')
FILE_DATE_FORMAT: te.Final = configuration.str('INITIAL_FILE_DATE_FORMAT')
VIRAL50_CHART_COLUMN_NAMES: te.Final = configuration.list('VIRAL50_CHART_COLUMN_NAMES')
TOP200_CHART_COLUMN_NAMES: te.Final = configuration.list('TOP200_CHART_COLUMN_NAMES')


REGION_DOWNLOAD_ERROR: te.Final = configuration.str('REGION_DOWNLOAD_ERROR')
DATE_DOWNLOAD_ERROR: te.Final = configuration.str('DATE_DOWNLOAD_ERROR')
CHART_DOWNLOAD_ERROR: te.Final = configuration.str('CHART_DOWNLOAD_ERROR')
CHART_DOWNLOAD_WARNING: te.Final = configuration.str('CHART_DOWNLOAD_WARNING')
NAME_ERROR: te.Final = configuration.str('NAME_ERROR')
PERIODICITY_ERROR: te.Final = configuration.str('PERIODICITY_ERROR')
REGION_NAME_ERROR: te.Final = configuration.str('REGION_NAME_ERROR')
BEGIN_DATE_ERROR: te.Final = configuration.str('BEGIN_DATE_ERROR')
END_DATE_ERROR: te.Final = configuration.str('END_DATE_ERROR')
DATE_RANGE_ERROR: te.Final = configuration.str('DATE_RANGE_ERROR')
CPU_COUNT_ERROR: te.Final = configuration.str('CPU_COUNT_ERROR')
DIRECTORY_PATH_ERROR: te.Final = configuration.str('DIRECTORY_PATH_ERROR')
