_CHART_URL = 'https://spotifycharts.com'
_REGIONS_XPATH = './/div[@data-type="country"]//li'
_REGION_CODE_ATTRIBUTE = 'data-value'
_DATES_XPATH = './/div[@data-type="date"]//li'
_URL_DATE_ATTRIBUTE = 'data-value'
_ERRONEOUS_CHART_XPATH = './/div[@class="chart-error"]'
_UNFOUND_CHART_XPATH = './/div[@class="not-found"]'


_ERRONEOUS_CHART_XPATH = './/div[@class="chart-error"]'
_UNFOUND_CHART_XPATH = './/div[@class="not-found"]'
_VIRAL_CHART_HEADER = 'Position,"Track Name",Artist,URL'
_REGIONAL_CHART_HEADER = 'Position,"Track Name",Artist,Streams,URL'
_VIRAL_CHART_COLUMNS = ['track_position',
                        'track_name',
                        'artist_name',
                        'track_url']
_REGIONAL_CHART_COLUMNS = ['track_position',
                           'track_name',
                           'artist_name',
                           'stream_count',
                           'track_url']


DOWNLOAD_MESSAGE = 'unable to download the chart by this url: '
NAME_MESSAGE = 'argument name must be either "viral" or "regional"'
PERIODICITY_MESSAGE = 'argument periodicity must be either "daily" or "weekly"'
REGION_NAME_MESSAGE = 'argument region_name must be string and store an item out of the return of get_all_regions()'
REGION_NAMES_MESSAGE = 'argument region_names must be list of strings and store items out of the return of get_all_regions()'
BEGIN_DATE_MESSAGE = 'argument begin_date must be "dd-mm-yyyy"-like string and store an item out of the return of get_all_dates()'
END_DATE_MESSAGE = 'argument end_date must be "dd-mm-yyyy"-like string and store an item out of the return of get_all_dates()'
WRONG_DATE_RANGE_MESSAGE = 'arguments begin_date and end_date are incorrect because begin_date > end_date'
CPU_COUNT_MESSAGE = 'argument cpu_count must be a positive integer number'
FILE_PATH_MESSAGE = 'argument file_path must be string and store the path of the csv file'
