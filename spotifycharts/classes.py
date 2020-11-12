import io
import pathlib
import multiprocessing as mp

import bs4
import requests
import pandas as pd
import pendulum
from pendulum.date import Date

import spotifycharts as sc
from spotifycharts import logging
from spotifycharts import settings
from spotifycharts import exceptions


class Name(str):

    def __new__(cls,
                name):
        if name in settings.NAME_CODES:
            return super().__new__(cls,
                                   name)
        else:
            raise exceptions.ArgumentTypeError(settings.NAME_ERROR)


class Periodicity(str):

    def __new__(cls,
                periodicity):
        if periodicity in settings.PERIODICITY_CODES:
            return super().__new__(cls,
                                   periodicity)
        else:
            raise exceptions.ArgumentTypeError(settings.PERIODICITY_ERROR)


class RegionNames(list):

    def __init__(self,
                 name,
                 region_names):
        regions = sc.download_regions(name)
        if not region_names:
            super().__init__(settings.DEFAULT_REGION_NAMES)
        elif set(region_names).issubset(regions.keys()):
            super().__init__([region_name
                              for region_name in region_names])
        else:
            raise exceptions.ArgumentTypeError(settings.REGION_NAME_ERROR)


class BeginDate(Date):

    def __new__(cls,
                begin_date):
        min_datetime = pendulum.from_format(settings.FOUNDATION_DATE,
                                            settings.FILE_DATE_FORMAT)
        max_datetime = pendulum.today()
        if not begin_date:
            begin_date = max_datetime.subtract(months=settings.DEFAULT_MONTH_PERIOD)
            return super().__new__(cls,
                                   begin_date.year,
                                   begin_date.month,
                                   begin_date.day)
        try:
            begin_date = pendulum.from_format(begin_date,
                                              settings.FILE_DATE_FORMAT).date()
        except (ValueError, TypeError):
            raise exceptions.ArgumentTypeError(settings.BEGIN_DATE_ERROR)
        else:
            if min_datetime.date() <= begin_date <= max_datetime.date():
                return super().__new__(cls,
                                       begin_date.year,
                                       begin_date.month,
                                       begin_date.day)
            else:
                raise exceptions.ArgumentTypeError(settings.BEGIN_DATE_ERROR)


class EndDate(Date):

    def __new__(cls,
                end_date):
        min_datetime = pendulum.from_format(settings.FOUNDATION_DATE,
                                            settings.FILE_DATE_FORMAT)
        max_datetime = pendulum.today()
        if not end_date:
            end_date = max_datetime
            return super().__new__(cls,
                                   end_date.year,
                                   end_date.month,
                                   end_date.day)
        try:
            end_date = pendulum.from_format(end_date,
                                            settings.FILE_DATE_FORMAT).date()
        except (ValueError, TypeError):
            raise exceptions.ArgumentTypeError(settings.END_DATE_ERROR)
        else:
            if min_datetime.date() <= end_date <= max_datetime.date():
                return super().__new__(cls,
                                       end_date.year,
                                       end_date.month,
                                       end_date.day)
            else:
                raise exceptions.ArgumentTypeError(settings.END_DATE_ERROR)


class CpuCount(int):

    def __new__(cls,
                cpu_count):
        if not cpu_count:
            cpu_count = mp.cpu_count()
            return super().__new__(cls,
                                   cpu_count)
        elif cpu_count in list(range(1, mp.cpu_count() + 1)):
            return super().__new__(cls,
                                   cpu_count)
        else:
            raise exceptions.ArgumentTypeError(settings.CPU_COUNT_ERROR)


class DirectoryPath(str):

    def __new__(cls,
                directory_path):

        if not directory_path:
            directory_path = pathlib.Path.cwd()
            return super().__new__(cls,
                                   directory_path)
        try:
            directory_path = pathlib.Path(directory_path)
        except TypeError:
            raise exceptions.ArgumentTypeError(settings.DIRECTORY_PATH_ERROR)
        else:
            return super().__new__(cls,
                                   directory_path)


class Chart(pd.DataFrame):

    def __init__(self,
                 url):
        with requests.Session() as session:
            response = session.get(url + '/download')
        if response.status_code != requests.codes.OK:
            logging.logger.warning(f'{settings.LOG_CHART_DOWNLOAD_WARNING}: {url}')
            super().__init__(columns=['date'])
        parser = bs4.BeautifulSoup(response.text,
                                   'html.parser')
        chart_error = parser.select(settings.CHART_ERROR_CSS)
        chart_lost = parser.select(settings.LOST_CHART_CSS)
        if chart_error or chart_lost:
            logging.logger.warning(f'{settings.LOG_CHART_DOWNLOAD_WARNING}: {url}')
            super().__init__(columns=['date'])
        viral50_chart_file_header = response.text.splitlines()[0]
        top200_chart_file_header = response.text.splitlines()[1]
        if viral50_chart_file_header == settings.VIRAL50_CHART_FILE_HEADER:
            chart = pd.read_csv(io.StringIO(response.text),
                                sep=settings.FILE_DELIMITER,
                                encoding=settings.FILE_ENCODING,
                                skiprows=None,
                                header=0,
                                names=settings.VIRAL50_CHART_COLUMN_NAMES)
            chart.track_position = pd.to_numeric(chart.track_position)
            chart.track_name = chart.track_name.str.strip()
            chart.artist_name = chart.artist_name.str.strip()
            chart.track_url = chart.track_url.str.strip()
            logging.logger.info(f'{settings.LOG_CHART_DOWNLOAD_INFO}: {url}')
            super().__init__(chart)
        elif top200_chart_file_header == settings.TOP200_CHART_FILE_HEADER:
            chart = pd.read_csv(io.StringIO(response.text),
                                sep=settings.FILE_DELIMITER,
                                encoding=settings.FILE_ENCODING,
                                skiprows=0,
                                header=1,
                                names=settings.TOP200_CHART_COLUMN_NAMES)
            chart.track_position = pd.to_numeric(chart.track_position)
            chart.track_name = chart.track_name.str.strip()
            chart.artist_name = chart.artist_name.str.strip()
            chart.stream_count = pd.to_numeric(chart.stream_count)
            chart.track_url = chart.track_url.str.strip()
            logging.logger.info(f'{settings.LOG_CHART_DOWNLOAD_INFO}: {url}')
            super().__init__(chart)
        else:
            logging.logger.warning(f'{settings.LOG_CHART_DOWNLOAD_WARNING}: {url}')
            super().__init__(columns=['date'])
