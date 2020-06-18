_MAIN_URL = 'https://spotifycharts.com/{name_code}'
_REGION_URL = 'https://spotifycharts.com/{name_code}/{region_code}/{periodicity_code}'
_CHART_URL = '{region_url}/{date_code}/download'


_NAME_VALUES = {'viral50': 'viral',
                'top200': 'regional'}
_PERIODICITY_VALUES = {'daily': 'daily',
                       'weekly': 'weekly'}


_DEFAULT_REGION_NAME = 'global'


_DEFAULT_MONTH_PERIOD = 1
_FOUNDATION_DATE = '2008-10-07'


_ERROR_XPATH = './/div[@class="chart-error"]'
_UNFOUND_XPATH = './/div[@class="not-found"]'
_DATES_XPATH = './/div[@data-type="date"]//li'
_REGIONS_XPATH = './/div[@data-type="country"]//li'
_DATE_CODE_ATTRIBUTE = 'data-value'
_REGION_CODE_ATTRIBUTE = 'data-value'
_HTML_DATE_FORMAT = 'MM/DD/YYYY'


_VIRAL50_CHART_FILE_HEADER = 'Position,"Track Name",Artist,URL'
_TOP200_CHART_FILE_HEADER = 'Position,"Track Name",Artist,Streams,URL'
_FILE_DELIMETER = ','
_FILE_EXTENSION = 'csv'
_FILE_DATE_FORMAT = 'YYYY-MM-DD'
_FILE_NAME = 'spotify_{name}_{periodicity}_track_charts_from_{begin_date}_to_{end_date}' + '.' + _FILE_EXTENSION
_VIRAL50_CHART_COLUMN_NAMES = ['track_position',
                               'track_name',
                               'artist_name',
                               'track_url']
_TOP200_CHART_COLUMN_NAMES = ['track_position',
                              'track_name',
                              'artist_name',
                              'stream_count',
                              'track_url']


_PROGRESS_BAR_TIME_FORMAT = 'HH:mm'
_PROGRESS_BAR_DESCRIPTION = '{current_time} | {region_name}'


_CHART_DOWNLOAD_MESSAGE = 'unable to download the chart by this url: {url}'
_REGION_DOWNLOAD_MESSAGE = 'unable to download the regions by this url: {url}'
_NAME_MESSAGE = 'argument name must be either "viral50" or "top200": {name}'
_PERIODICITY_MESSAGE = 'argument periodicity must be either "daily" or "weekly": {periodicity}'
_REGION_NAME_MESSAGE = 'argument region_name must be string and store an item from the return of get_all_regions(): {region_name}'
_REGION_NAMES_MESSAGE = 'argument region_names must be list of strings and store items from the return of get_all_regions(): {region_names}'
_BEGIN_DATE_MESSAGE = 'argument begin_date must be \"' + _FILE_DATE_FORMAT + '\"-like string and store an item from the return of get_all_dates(): {begin_date}'
_END_DATE_MESSAGE = 'argument end_date must be \"' + _FILE_DATE_FORMAT + '\"-like string and store an item from the return of get_all_dates(): {end_date}'
_WRONG_DATE_RANGE_MESSAGE = 'arguments begin_date and end_date are incorrect: {begin_date} > {end_date}'
_CPU_COUNT_MESSAGE = 'argument cpu_count must be int and store a natural number: {cpu_count}'
_FILE_PATH_MESSAGE = 'argument file_path must be string and store the path of the ' + _FILE_EXTENSION + ' file: {file_path}'
