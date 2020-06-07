import io
import os
import multiprocessing as mp


import pendulum
import pandas as pd
import requests
from lxml import etree as et
from tqdm import auto


from spotifycharts import classes
from spotifycharts import constants
from spotifycharts import functions



class Downloader:


    def __init__(self,
                 name,
                 periodicity,
                 region_names=None,
                 begin_date=None,
                 end_date=None,
                 cpu_count=None,
                 file_path=None):

        self._name = classes.Name(name).name
        self._periodicity = classes.Periodicity(periodicity).periodicity
        self._region_names = classes.RegionNames(name,
                                                 region_names).region_names
        self._begin_date = classes.BeginDate(begin_date).begin_date
        self._end_date = classes.EndDate(end_date).end_date
        if self._begin_date > self._end_date:
            raise classes.WrongDateRangeError
        self._cpu_count = classes.CpuCount(cpu_count).cpu_count
        self._file_path = classes.FilePath(name,
                                           periodicity,
                                           begin_date,
                                           end_date,
                                           file_path).file_path
        if not os.path.exists(self._file_path):
            regions = self.get_all_regions(self._name,
                                           self._periodicity)
            region_name, region_url = list(regions.items())[0]
            dates = self.get_all_dates(self._name,
                                       self._periodicity,
                                       region_name)
            dates = {chart_date: url_date
                     for chart_date, url_date in dates.items()
                     if self._begin_date <= chart_date <= self._end_date}
            chart_date, url_date = list(dates.items())[0]
            url = '/'.join([region_url,
                            url_date,
                            'download'])
            chart = functions.download(url,
                                       chart_date,
                                       region_name)
            chart.to_csv(self._file_path,
                         index=False)
        self._data = pd.read_csv(self._file_path).copy(deep=True)


    @classmethod
    def get_all_regions(cls,
                        name,
                        periodicity):

        name = classes.Name(name).name
        periodicity = classes.Periodicity(periodicity).periodicity
        main_url = '/'.join([constants._CHART_URL,
                             name])
        with requests.Session() as session:
            response = session.get(main_url)
        if not 200 <= response.status_code < 300:
            return {}
        parser = et.HTMLParser()
        tree = et.parse(io.BytesIO(response.content),
                        parser)
        region_elements = tree.xpath(constants._REGIONS_XPATH)
        regions = {}
        for element in region_elements:
            region_name = element.text.lower().strip()
            region_code = element.get(constants._REGION_CODE_ATTRIBUTE)
            region_url = '/'.join([constants._CHART_URL,
                                   name,
                                   region_code,
                                   periodicity])
            regions[region_name] = region_url
        return regions


    def _get_necessary_regions(self,
                               response):

        parser = et.HTMLParser()
        tree = et.parse(io.BytesIO(response.content),
                        parser)
        region_elements = tree.xpath(constants._REGIONS_XPATH)
        regions = {}
        for element in region_elements:
            region_name = element.text.lower().strip()
            if region_name in self._region_names:
                region_code = element.get(constants._REGION_CODE_ATTRIBUTE)
                region_url = '/'.join([constants._CHART_URL,
                                       self._name,
                                       region_code,
                                       self._periodicity])
                regions[region_name] = region_url
        return regions


    @classmethod
    def get_all_dates(cls,
                      name,
                      periodicity,
                      region_name='global'):

        name = classes.Name(name)._name
        periodicity = classes.Periodicity(periodicity).periodicity
        region_name = classes.RegionName(name,
                                         region_name).region_name
        regions = cls.get_all_regions(name,
                                      periodicity)
        region_url = regions[region_name]
        with requests.Session() as session:
            response = session.get(region_url)
        if not 200 <= response.status_code < 300:
            return {}
        parser = et.HTMLParser()
        tree = et.parse(io.BytesIO(response.content),
                        parser)
        date_elements = tree.xpath(constants._DATES_XPATH)
        dates = {}
        for element in date_elements:
            chart_date = pendulum.from_format(element.text,
                                              'MM/DD/YYYY').date()
            url_dates = []
            for url_date in element.get(constants._URL_DATE_ATTRIBUTE).split('--'):
                url_date = pendulum.from_format(url_date,
                                                'YYYY-MM-DD').date()
                url_date = url_date.format('YYYY-MM-DD')
                url_dates.append(url_date)
            dates[chart_date] = '--'.join(url_dates)
        return dates


    def _get_missing_dates(self,
                           response,
                           region_name):

        region_charts = self._data[self._data['region_name'] == region_name]
        file_dates = [pd.Timestamp(file_date).to_pydatetime().date()
                      for file_date in region_charts['date'].unique()]
        parser = et.HTMLParser()
        tree = et.parse(io.BytesIO(response.content),
                        parser)
        date_elements = tree.xpath(constants._DATES_XPATH)
        dates = {}
        for element in date_elements:
            chart_date = pendulum.from_format(element.text,
                                              'MM/DD/YYYY').date()
            is_date_in_range = self._begin_date <= chart_date <= self._end_date
            is_date_in_file = chart_date in file_dates
            if is_date_in_range and not is_date_in_file:
                url_dates = []
                for url_date in element.get(constants._URL_DATE_ATTRIBUTE).split('--'):
                    url_date = pendulum.from_format(url_date,
                                                    'YYYY-MM-DD').date()
                    url_date = url_date.format('YYYY-MM-DD')
                    url_dates.append(url_date)
                dates[chart_date] = '--'.join(url_dates)
        return dates


    def _get_missing_urls(self):

        triplets = []
        main_url = '/'.join([constants._CHART_URL,
                             self._name])
        with requests.Session() as session:
            response = session.get(main_url)
        if not 200 <= response.status_code < 300:
            return []
        regions = self._get_necessary_regions(response)
        if not regions:
            return []
        with auto.tqdm(regions.items()) as progress_bar:
            for region_name, region_url in progress_bar:
                current_time = pendulum.now().time().format('HH:mm')
                description = current_time + ' | generating urls'
                progress_bar.set_description(description)
                with requests.Session() as session:
                    response = session.get(region_url)
                if not 200 <= response.status_code < 300:
                    continue
                region_dates = self._get_missing_dates(response,
                                                       region_name)
                if not region_dates:
                    continue
                parser = et.HTMLParser()
                tree = et.parse(io.BytesIO(response.content),
                                parser)
                is_chart_erroneous = tree.xpath(constants._ERRONEOUS_CHART_XPATH)
                is_chart_unfound = tree.xpath(constants._UNFOUND_CHART_XPATH)
                if is_chart_erroneous or is_chart_unfound:
                    continue
                for chart_date, url_date in region_dates.items():
                    url = '/'.join([region_url,
                                    url_date,
                                    'download'])
                    triplet = (url,
                               chart_date,
                               region_name)
                    triplets.append(triplet)
        return triplets


    def download(self):

        triplets = self._get_missing_urls()
        if not triplets:
            return pd.DataFrame()
        length = len(triplets)
        url_count_per_cpu = 100
        step = url_count_per_cpu * self._cpu_count
        with auto.tqdm(range(0, length, step)) as progress_bar:
            if self._cpu_count == 1:
                for index in progress_bar:
                    current_time = pendulum.now().time().format('HH:mm')
                    description = current_time + ' | downloading charts'
                    progress_bar.set_description(description)
                    partial_data = download(*triplets[index])
                    self._data = self._data.append(partial_data,
                                                   sort=True)
                    self._data.reset_index(drop=True,
                                           inplace=True)
                    self._data.to_csv(self._file_path,
                                      index=False)
            else:
                for index in progress_bar:
                    current_time = pendulum.now().time().format('HH:mm')
                    description = current_time + ' | downloading charts'
                    progress_bar.set_description(description)
                    with mp.Pool(self._cpu_count) as pool:
                        partial_triplets = triplets[index: index + step]
                        partial_data = list(pool.starmap(functions.download,
                                                         partial_triplets))
                    self._data = self._data.append(partial_data,
                                                   sort=True)
                    self._data.reset_index(drop=True,
                                           inplace=True)
                    self._data.to_csv(self._file_path,
                                      index=False)
        self._data.drop_duplicates(inplace=True)
        self._data.sort_values(by=['region_name', 'date'],
                               ascending=[True, False],
                               inplace=True)
        self._data.reset_index(drop=True,
                               inplace=True)
        self._data.to_csv(self._file_path,
                          index=False)


    @property
    def name(self):
        return self._name


    @property
    def periodicity(self):
        return self._periodicity


    @property
    def region_names(self):
        return self._region_names


    @property
    def begin_date(self):
        return self._begin_date


    @property
    def end_date(self):
        return self._end_date


    @property
    def file_path(self):
        return self._file_path


    @property
    def data(self):
        return self._data
