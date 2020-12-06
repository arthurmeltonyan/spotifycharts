import pathlib
import multiprocessing as mp

import bs4
import httpx
import pendulum
import pandas as pd
from tqdm import auto

from spotifycharts import classes
from spotifycharts import settings
from spotifycharts import exceptions


def download_regions(name):
    name = classes.Name(name)
    name_code = settings.NAME_CODES[name]
    url = f'{settings.SPOTIFY_CHARTS_URL}/{name_code}'
    with httpx.Client() as client:
        response = client.get(url)
    regions = {}
    if response.status_code != httpx.codes.OK:
        return regions
    parser = bs4.BeautifulSoup(response.text,
                               'html.parser')
    elements = parser.select(settings.REGION_CSS)
    for element in elements:
        region_name = element.text.lower().strip()
        region_code = element.get(settings.REGION_CODE_ATTRIBUTE)
        regions[region_name] = region_code
    return regions


def download_dates(name,
                   periodicity,
                   region_name):
    name = classes.Name(name)
    periodicity = classes.Periodicity(periodicity)
    region_name = classes.RegionNames(name,
                                      [region_name])[0]
    name_code = settings.NAME_CODES[name]
    periodicity_code = settings.PERIODICITY_CODES[periodicity]
    region_code = download_regions(name)[region_name]
    region_url = f'{settings.SPOTIFY_CHARTS_URL}/{name_code}/{region_code}/{periodicity_code}'
    with httpx.Client() as client:
        response = client.get(region_url)
    dates = {}
    if response.status_code != httpx.codes.OK:
        return dates
    parser = bs4.BeautifulSoup(response.text,
                               'html.parser')
    chart_error = parser.select(settings.CHART_ERROR_CSS)
    chart_lost = parser.select(settings.LOST_CHART_CSS)
    if chart_error or chart_lost:
        return dates
    date_elements = parser.select(settings.DATE_CSS)
    for date_element in date_elements:
        date = pendulum.from_format(date_element.text,
                                    settings.HTML_DATE_FORMAT)
        date = date.date()
        date_codes = []
        time_period = date_element.get(settings.DATE_CODE_ATTRIBUTE)
        for date_code in time_period.split(settings.URL_DATE_DELIMITER):
            date_code = pendulum.from_format(date_code,
                                             settings.URL_DATE_FORMAT)
            date_code = date_code.format(settings.FILE_DATE_FORMAT)
            date_codes.append(date_code)
        dates[date] = settings.URL_DATE_DELIMITER.join(date_codes)
    return dates


class Downloader:

    def __setitem__(self,
                    region_name,
                    data):
        try:
            begin_date = self.begin_date.format(settings.FILE_DATE_FORMAT)
            end_date = self.end_date.format(settings.FILE_DATE_FORMAT)
            file_name = f'from_{begin_date}_to_{end_date}.{settings.FILE_EXTENSION}'
            directory_path = f'spotify_charts/{self.name}/{self.periodicity}/{region_name}'
            file_path = pathlib.Path(directory_path).joinpath(file_name)
            data.reset_index(drop=True,
                             inplace=True)
            data.sort_values(by=['date', 'track_position'],
                             ascending=[False, True],
                             inplace=True)
            data.to_csv(file_path,
                        sep=settings.FILE_DELIMITER,
                        encoding=settings.FILE_ENCODING,
                        index=False)
        except (KeyError, AttributeError):
            pass

    def __getitem__(self,
                    region_name):
        try:
            begin_date = self.begin_date.format(settings.FILE_DATE_FORMAT)
            end_date = self.end_date.format(settings.FILE_DATE_FORMAT)
            file_name = f'from_{begin_date}_to_{end_date}.{settings.FILE_EXTENSION}'
            directory_path = f'spotify_charts/{self.name}/{self.periodicity}/{region_name}'
            file_path = pathlib.Path(directory_path).joinpath(file_name)
            data = pd.read_csv(file_path,
                               sep=settings.FILE_DELIMITER,
                               encoding=settings.FILE_ENCODING)
            return data
        except KeyError:
            if self.name == 'top200':
                return pd.DataFrame(columns=settings.TOP200_CHART_COLUMN_NAMES)
            else:
                return pd.DataFrame(columns=settings.VIRAL50_CHART_COLUMN_NAMES)

    def __delitem__(self,
                    region_name):
        try:
            begin_date = self.begin_date.format(settings.FILE_DATE_FORMAT)
            end_date = self.end_date.format(settings.FILE_DATE_FORMAT)
            file_name = f'from_{begin_date}_to_{end_date}.{settings.FILE_EXTENSION}'
            directory_path = f'spotify_charts/{self.name}/{self.periodicity}/{region_name}'
            file_path = pathlib.Path(directory_path).joinpath(file_name)
            file_path.unlink()
            file_path.parent.rmdir()
        except KeyError:
            pass

    def __init__(self,
                 name,
                 periodicity,
                 region_names=None,
                 begin_date=None,
                 end_date=None,
                 cpu_count=None,
                 directory_path=None):
        self.name = classes.Name(name)
        self.periodicity = classes.Periodicity(periodicity)
        self.region_names = classes.RegionNames(name, region_names)
        self.begin_date = classes.BeginDate(begin_date)
        self.end_date = classes.EndDate(end_date)
        if self.begin_date > self.end_date:
            raise exceptions.ArgumentTypeError(settings.DATE_RANGE_ERROR)
        self.cpu_count = classes.CpuCount(cpu_count)
        self.directory_path = classes.DirectoryPath(directory_path)
        all_regions = download_regions(self.name)
        regions = {}
        for region_name in all_regions:
            if region_name in self.region_names:
                regions[region_name] = all_regions[region_name]
        regions_items = auto.tqdm(regions.items())
        for region_name, region_code in regions_items:
            region_charts = self[region_name]
            file_dates = []
            for file_date in region_charts['date'].unique():
                file_date = pendulum.instance(pd.Timestamp(file_date).to_pydatetime()).date()
                file_dates.append(file_date)
            current_time = pendulum.now().format('HH:mm')
            description = f'{current_time} | {region_name}'
            regions_items.set_description(description)
            all_dates = download_dates(self.name,
                                       self.periodicity,
                                       region_name)
            urls = []
            dates = []
            for date, date_code in all_dates.items():
                if self.begin_date <= date <= self.end_date and date not in file_dates:
                    url = f'{settings.SPOTIFY_CHARTS_URL}/{self.name_code}/{region_code}/{self.periodicity_code}/{date_code}'
                    urls.append(url)
                    dates.append(date)
            downloaded_charts = []
            for url, date in auto.tqdm(zip(urls, dates),
                                       total=len(urls)):
                chart = classes.Chart(url)
                chart['region_name'] = region_name
                chart['date'] = date
                downloaded_charts.append(chart)
            self[region_name] = region_charts.append(downloaded_charts,
                                                     sort=True)
        regions_items.close()

    @property
    def name_code(self):
        return settings.NAME_CODES[self.name]

    @property
    def periodicity_code(self):
        return settings.PERIODICITY_CODES[self.periodicity]
