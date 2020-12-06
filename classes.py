import io
import pathlib
import multiprocessing as mp

import bs4
import httpx
import pandas as pd
from tqdm import auto
import pendulum
from pendulum.date import Date

import spotifycharts as sc
from spotifycharts import settings
from spotifycharts import exceptions


class Name(str):

    def __new__(cls,
                name):
        if name in settings.NAME_CODES:
            return str.__new__(cls,
                               name)
        else:
            raise exceptions.ArgumentTypeError(settings.NAME_ERROR)


class Periodicity(str):

    def __new__(cls,
                periodicity):
        if periodicity in settings.PERIODICITY_CODES:
            return str.__new__(cls,
                               periodicity)
        else:
            raise exceptions.ArgumentTypeError(settings.PERIODICITY_ERROR)


class RegionNames(str):

    def __new__(cls,
                name,
                region_names):
        regions = sc.download_regions(name)
        if not region_names:
            region_names = [settings.DEFAULT_REGION_NAME]
        if set(region_names).issubset(regions.keys()):
            return [str.__new__(cls,
                                region_name)
                    for region_name in region_names]
        else:
            raise exceptions.ArgumentTypeError(settings.REGION_NAME_ERROR)


class BeginDate(Date):

    def __new__(cls,
                begin_date):
        min_date = pendulum.from_format(settings.FOUNDATION_DATE,
                                        settings.FILE_DATE_FORMAT).date()
        max_date = pendulum.today().date()
        if not begin_date:
            begin_date = max_date.subtract(months=settings.DEFAULT_MONTH_PERIOD)
            begin_date = begin_date.format(settings.FILE_DATE_FORMAT)
        begin_date = pendulum.from_format(begin_date,
                                          settings.FILE_DATE_FORMAT).date()
        if min_date <= begin_date <= max_date:
            return super().__new__(cls,
                                   begin_date.year,
                                   begin_date.month,
                                   begin_date.day)
        else:
            raise exceptions.ArgumentTypeError(settings.BEGIN_DATE_ERROR)


class EndDate(Date):

    def __new__(cls,
                end_date):
        min_date = pendulum.from_format(settings.FOUNDATION_DATE,
                                        settings.FILE_DATE_FORMAT).date()
        max_date = pendulum.today().date()
        if not end_date:
            end_date = max_date
            end_date = end_date.format(settings.FILE_DATE_FORMAT)
        end_date = pendulum.from_format(end_date,
                                        settings.FILE_DATE_FORMAT).date()
        if min_date <= end_date <= max_date:
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
        if cpu_count in list(range(1, mp.cpu_count() + 1)):
            return int.__new__(cls,
                               cpu_count)
        else:
            raise exceptions.ArgumentTypeError(settings.CPU_COUNT_ERROR)


class DirectoryPath(str):

    def __new__(cls,
                directory_path):

        if not directory_path:
            directory_path = pathlib.Path.cwd().as_posix()
        try:
            directory_path = pathlib.Path(directory_path)
        except (TypeError, AttributeError):
            raise exceptions.ArgumentTypeError(settings.DIRECTORY_PATH_ERROR)
        else:
            return str.__new__(cls,
                               directory_path)


class Chart(pd.DataFrame):

    def __init__(self,
                 url):
        url = url + '/download'
        with httpx.Client() as client:
            response = client.get(url)
        if response.status_code != httpx.codes.OK:
            auto.tqdm.write(f'{settings.CHART_DOWNLOAD_ERROR}: {url}')
        parser = bs4.BeautifulSoup(response.text,
                                   'html.parser')
        chart_error = parser.select(settings.CHART_ERROR_CSS)
        chart_lost = parser.select(settings.LOST_CHART_CSS)
        if chart_error or chart_lost:
            auto.tqdm.write(f'{settings.CHART_DOWNLOAD_ERROR}: {url}')
        viral50_chart_file_header = response.text.splitlines()[0]
        top200_chart_file_header = response.text.splitlines()[1]
        if viral50_chart_file_header == settings.VIRAL50_CHART_FILE_HEADER:
            chart = pd.read_csv(io.StringIO(response.text),
                                sep=settings.FILE_DELIMITER,
                                skiprows=None,
                                header=0,
                                names=settings.VIRAL50_CHART_COLUMN_NAMES)
            if chart.shape[0] != 50:
                auto.tqdm.write(f'{settings.CHART_DOWNLOAD_WARNING}: {url}')
            chart.track_position = pd.to_numeric(chart.track_position)
            chart.track_name = chart.track_name.str.strip()
            chart.artist_name = chart.artist_name.str.strip()
            super().__init__(chart)
        elif top200_chart_file_header == settings.TOP200_CHART_FILE_HEADER:
            chart = pd.read_csv(io.StringIO(response.text),
                                sep=settings.FILE_DELIMITER,
                                skiprows=0,
                                header=1,
                                names=settings.TOP200_CHART_COLUMN_NAMES)
            if chart.shape[0] != 200:
                auto.tqdm.write(f'{settings.CHART_DOWNLOAD_WARNING}: {url}')
            chart.track_position = pd.to_numeric(chart.track_position)
            chart.stream_count = pd.to_numeric(chart.stream_count)
            chart.track_name = chart.track_name.str.strip()
            chart.artist_name = chart.artist_name.str.strip()
            super().__init__(chart)
        else:
            auto.tqdm.write(f'{settings.CHART_DOWNLOAD_ERROR}: {url}')
