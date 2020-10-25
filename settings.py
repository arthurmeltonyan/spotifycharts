import os
import typing_extensions as te

import dotenv
dotenv.load_dotenv('spotifycharts/configuration.env')

SPOTIFY_CHARTS_URL: te.Final = os.environ['URL']


NAME_CODES: te.Final = {os.environ['VIRAL50'].split(':')[0]: os.environ['VIRAL50'].split(':')[1],
                        os.environ['TOP200'].split(':')[0]: os.environ['TOP200'].split(':')[1]}
PERIODICITY_CODES: te.Final = {os.environ['DAILY'].split(':')[0]: os.environ['DAILY'].split(':')[1],
                               os.environ['WEEKLY'].split(':')[0]: os.environ['WEEKLY'].split(':')[1]}


DEFAULT_REGION_NAME: te.Final = os.environ['DEFAULT_REGION_NAME']
DEFAULT_MONTH_PERIOD: te.Final = os.environ['DEFAULT_MONTH_PERIOD']
FOUNDATION_DATE: te.Final = os.environ['FOUNDATION_DATE']


CHART_ERROR_CSS: te.Final = os.environ['CHART_ERROR_CSS']
LOST_CHART_CSS: te.Final = os.environ['LOST_CHART_CSS']
DATE_CSS: te.Final = os.environ['DATE_CSS']
REGION_CSS: te.Final = os.environ['REGION_CSS']
DATE_CODE_ATTRIBUTE: te.Final = os.environ['DATE_CODE_ATTRIBUTE']
REGION_CODE_ATTRIBUTE: te.Final = os.environ['REGION_CODE_ATTRIBUTE']
HTML_DATE_FORMAT: te.Final = os.environ['HTML_DATE_FORMAT']
URL_DATE_FORMAT: te.Final = os.environ['URL_DATE_FORMAT']
URL_DATE_DELIMITER: te.Final = os.environ['URL_DATE_DELIMITER']


VIRAL50_CHART_FILE_HEADER: te.Final = os.environ['VIRAL50_CHART_FILE_HEADER']
TOP200_CHART_FILE_HEADER: te.Final = os.environ['TOP200_CHART_FILE_HEADER']
FILE_DELIMITER: te.Final = os.environ['FILE_DELIMITER']
FILE_ENCODING: te.Final = os.environ['FILE_ENCODING']
FILE_EXTENSION: te.Final = os.environ['FILE_EXTENSION']
FILE_DATE_FORMAT: te.Final = os.environ['INITIAL_FILE_DATE_FORMAT']
VIRAL50_CHART_COLUMN_NAMES: te.Final = os.environ['VIRAL50_CHART_COLUMN_NAMES'].split(',')
TOP200_CHART_COLUMN_NAMES: te.Final = os.environ['TOP200_CHART_COLUMN_NAMES'].split(',')


REGION_DOWNLOAD_ERROR: te.Final = os.environ['REGION_DOWNLOAD_ERROR']
DATE_DOWNLOAD_ERROR: te.Final = os.environ['DATE_DOWNLOAD_ERROR']
CHART_DOWNLOAD_ERROR: te.Final = os.environ['CHART_DOWNLOAD_ERROR']
CHART_DOWNLOAD_WARNING: te.Final = os.environ['CHART_DOWNLOAD_WARNING']
NAME_ERROR: te.Final = os.environ['NAME_ERROR']
PERIODICITY_ERROR: te.Final = os.environ['PERIODICITY_ERROR']
REGION_NAME_ERROR: te.Final = os.environ['REGION_NAME_ERROR']
BEGIN_DATE_ERROR: te.Final = os.environ['BEGIN_DATE_ERROR']
END_DATE_ERROR: te.Final = os.environ['END_DATE_ERROR']
DATE_RANGE_ERROR: te.Final = os.environ['DATE_RANGE_ERROR']
CPU_COUNT_ERROR: te.Final = os.environ['CPU_COUNT_ERROR']
DIRECTORY_PATH_ERROR: te.Final = os.environ['DIRECTORY_PATH_ERROR']
