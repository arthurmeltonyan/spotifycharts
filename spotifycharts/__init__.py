import io
import os


import pandas as pd
import pendulum
import httpx
from lxml import etree as et
from tqdm import auto
from pathos import multiprocessing as mp


from spotifycharts import constants
from spotifycharts import classes



def get_all_regions(name,
                    periodicity):

    name = classes._Name(name)
    periodicity = classes._Periodicity(periodicity)

    name_code = constants._NAME_VALUES[name]
    periodicity_code = constants._PERIODICITY_VALUES[periodicity]

    main_url = constants._MAIN_URL.format(name_code=name_code)
    response = httpx.get(main_url,
                         timeout=constants._TIMEOUT)
    if not 200 <= response.status_code < 300:
        return {}
    tree = et.parse(io.StringIO(response.text),
                    et.HTMLParser())
    region_elements = tree.xpath(constants._REGIONS_XPATH)
    regions = {}
    for region_element in region_elements:
        region_name = region_element.text.lower().strip()
        region_code = region_element.get(constants._REGION_CODE_ATTRIBUTE)
        region_url = constants._REGION_URL.format(name_code=name_code,
                                                  region_code=region_code,
                                                  periodicity_code=periodicity_code)
        regions[region_name] = region_url
    return regions


def get_all_dates(name,
                  periodicity,
                  region_name=None):

    name = classes._Name(name)
    periodicity = classes._Periodicity(periodicity)
    region_name = classes._RegionName(name,
                                      region_name)
    regions = get_all_regions(name,
                              periodicity)
    region_url = regions[region_name]
    response = httpx.get(region_url,
                         timeout=constants._TIMEOUT)
    if not 200 <= response.status_code < 300:
        return {}
    tree = et.parse(io.StringIO(response.text),
                    et.HTMLParser())
    date_elements = tree.xpath(constants._DATES_XPATH)
    dates = {}
    for date_element in date_elements:
        chart_date = pendulum.from_format(date_element.text,
                                          constants._HTML_DATE_FORMAT)
        chart_date = chart_date.date()
        date_codes = []
        timespan = date_element.get(constants._DATE_CODE_ATTRIBUTE)
        for date_code in timespan.split('--'):
            date_code = pendulum.from_format(date_code,
                                             constants._FILE_DATE_FORMAT)
            date_code = date_code.date()
            date_code = date_code.format(constants._FILE_DATE_FORMAT)
            date_codes.append(date_code)
        dates[chart_date] = '--'.join(date_codes)
    return dates


class ChartData:


    def __init__(self,
                 name,
                 periodicity,
                 region_names=None,
                 begin_date=None,
                 end_date=None,
                 cpu_count=None,
                 file_path=None):

        self._name = classes._Name(name)
        self._periodicity = classes._Periodicity(periodicity)
        self._region_names = classes._RegionNames(name,
                                                  region_names)
        self._begin_date, self._end_date = classes._DateRange(begin_date,
                                                              end_date)
        self._cpu_count = classes._CpuCount(cpu_count)
        self._file_path = classes._FilePath(name,
                                            periodicity,
                                            begin_date,
                                            end_date,
                                            file_path)
        if os.path.exists(self._file_path):
            self._data = pd.read_csv(self._file_path).copy(deep=True)
        else:
            regions = get_all_regions(self._name,
                                      self._periodicity)
            regions = {region_name: region_url
                       for region_name, region_url in regions.items()
                       if region_name in self._region_names}
            region_name, region_url = list(regions.items())[0]
            dates = get_all_dates(self._name,
                                  self._periodicity,
                                  region_name)
            dates = {chart_date: date_code
                     for chart_date, date_code in dates.items()
                     if self._begin_date <= chart_date <= self._end_date}
            chart_date, date_code = list(dates.items())[0]
            chart_url = constants._CHART_URL.format(region_url=region_url,
                                                    date_code=date_code)
            self._data = self._download_chart(chart_url,
                                              region_name,
                                              chart_date)
            self._data.to_csv(self._file_path,
                              index=False)
        self._download_necessary_charts()


    def _get_necessary_regions(self,
                               response):

        name_code = constants._NAME_VALUES[self._name]
        periodicity_code = constants._PERIODICITY_VALUES[self._periodicity]

        tree = et.parse(io.StringIO(response.text),
                        et.HTMLParser())
        region_elements = tree.xpath(constants._REGIONS_XPATH)
        regions = {}
        for region_element in region_elements:
            region_name = region_element.text.lower().strip()
            if region_name in self._region_names:
                region_code = region_element.get(constants._REGION_CODE_ATTRIBUTE)
                region_url = constants._REGION_URL.format(name_code=name_code,
                                                          region_code=region_code,
                                                          periodicity_code=periodicity_code)
                regions[region_name] = region_url
        return regions


    def _get_necessary_dates(self,
                             response,
                             region_name):

        region_charts = self._data[self._data['region_name'] == region_name]
        file_dates = [pd.Timestamp(file_date).to_pydatetime().date()
                      for file_date in region_charts['date'].unique()]
        tree = et.parse(io.StringIO(response.text),
                        et.HTMLParser())
        date_elements = tree.xpath(constants._DATES_XPATH)
        dates = {}
        for date_element in date_elements:
            chart_date = pendulum.from_format(date_element.text,
                                              constants._HTML_DATE_FORMAT)
            chart_date = chart_date.date()
            is_date_in_range = self._begin_date <= chart_date <= self._end_date
            is_date_in_file = chart_date in file_dates
            if is_date_in_range and not is_date_in_file:
                date_codes = []
                timespan = date_element.get(constants._DATE_CODE_ATTRIBUTE)
                for date_code in timespan.split('--'):
                    date_code = pendulum.from_format(date_code,
                                                     constants._FILE_DATE_FORMAT)
                    date_code = date_code.date()
                    date_code = date_code.format(constants._FILE_DATE_FORMAT)
                    date_codes.append(date_code)
                dates[chart_date] = '--'.join(date_codes)
        return dates


    def _download_necessary_charts(self):

        name_code = constants._NAME_VALUES[self._name]

        main_url = constants._MAIN_URL.format(name_code=name_code)
        response = httpx.get(main_url,
                             timeout=constants._TIMEOUT)
        if not 200 <= response.status_code < 300:
            return
        regions = self._get_necessary_regions(response)
        if not regions:
            return
        with auto.tqdm(regions.items()) as progress_bar:
            for region_name, region_url in progress_bar:
                current_time = pendulum.now().time()
                current_time = current_time.format(constants._PROGRESS_BAR_TIME_FORMAT)
                description = constants._PROGRESS_BAR_DESCRIPTION
                description = description.format(current_time=current_time,
                                                 region_name=region_name)
                progress_bar.set_description(description)
                response = httpx.get(region_url)
                if not 200 <= response.status_code < 300:
                    continue
                region_dates = self._get_necessary_dates(response,
                                                         region_name)
                if not region_dates:
                    continue
                tree = et.parse(io.StringIO(response.text),
                                et.HTMLParser())
                error = tree.xpath(constants._ERROR_XPATH)
                unfound = tree.xpath(constants._UNFOUND_XPATH)
                if error or unfound:
                    continue
                chart_urls = []
                chart_dates = []
                for chart_date, date_code in region_dates.items():
                    chart_url = constants._CHART_URL.format(region_url=region_url,
                                                            date_code=date_code)
                    chart_urls.append(chart_url)
                    chart_dates.append(chart_date)
                region_names = [region_name] * len(chart_urls)
                with mp.ProcessingPool(self._cpu_count) as pool:
                    partial_data = pool.imap(ChartData._download_chart,
                                             chart_urls,
                                             region_names,
                                             chart_dates)
                    partial_data = list(partial_data)
                self._data = self._data.append(partial_data,
                                               sort=True)
                self._data.reset_index(drop=True,
                                       inplace=True)
                self._data.to_csv(self._file_path,
                                  sep=constants._FILE_DELIMETER,
                                  index=False)
            self._data.drop_duplicates(inplace=True)
            self._data.sort_values(by=['region_name', 'date'],
                                   ascending=[True, False],
                                   inplace=True)
            self._data.reset_index(drop=True,
                                   inplace=True)
            self._data.to_csv(self._file_path,
                              sep=constants._FILE_DELIMETER,
                              index=False)


    @staticmethod
    def _download_chart(chart_url,
                        region_name,
                        chart_date):

        response = httpx.get(chart_url,
                             timeout=constants._TIMEOUT)
        if not 200 <= response.status_code < 300:
            message = constants._CHART_DOWNLOAD_MESSAGE
            message = message.format(url=chart_url)
            auto.tqdm.write(message)
            return pd.DataFrame()
        tree = et.parse(io.StringIO(response.text),
                        et.HTMLParser())
        error = tree.xpath(constants._ERROR_XPATH)
        unfound = tree.xpath(constants._UNFOUND_XPATH)
        if error or unfound:
            message = constants._CHART_DOWNLOAD_MESSAGE
            message = message.format(url=chart_url)
            auto.tqdm.write(message)
            return pd.DataFrame()
        viral50_header = response.text.splitlines()[0]
        top200_header = response.text.splitlines()[1]
        if viral50_header == constants._VIRAL50_CHART_FILE_HEADER:
            chart = pd.read_csv(io.StringIO(response.text),
                                sep=constants._FILE_DELIMETER,
                                skiprows=None,
                                header=0,
                                names=constants._VIRAL50_CHART_COLUMN_NAMES)
        elif top200_header == constants._TOP200_CHART_FILE_HEADER:
            chart = pd.read_csv(io.StringIO(response.text),
                                sep=constants._FILE_DELIMETER,
                                skiprows=0,
                                header=1,
                                names=constants._TOP200_CHART_COLUMN_NAMES)
            chart['stream_count'] = pd.to_numeric(chart['stream_count'])
        else:
            message = constants._CHART_DOWNLOAD_MESSAGE
            message = message.format(url=chart_url)
            auto.tqdm.write(message)
            return pd.DataFrame()
        chart['track_position'] = pd.to_numeric(chart['track_position'])
        chart['track_name'] = chart['track_name'].str.lower().str.strip()
        chart['artist_name'] = chart['artist_name'].str.lower().str.strip()
        chart['region_name'] = region_name.lower().strip()
        chart['date'] = chart_date.format(constants._FILE_DATE_FORMAT)
        chart.sort_values(by='track_position',
                          ascending=True,
                          inplace=True)
        return chart


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
    def cpu_count(self):

        return self._cpu_count


    @property
    def data(self):

        return self._data