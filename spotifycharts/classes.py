import io
import os
import multiprocessing as mp


import pendulum
import requests
from lxml import etree as et


from spotifycharts import constants



class DownloadError(ConnectionError):

    def __str__(self):

        return constants.DOWNLOAD_MESSAGE


class NameError(TypeError):

    def __str__(self):

        return constants.NAME_MESSAGE

class Name():

    def __init__(self,
                 name):

        try:
            name = name.lower().strip()
            if name not in ['viral', 'regional']:
                raise NameError
            self._name = name
        except:
            raise NameError

    @property
    def name(self):

        return self._name


class PeriodicityError(TypeError):

    def __str__(self):

        return constants.PERIODICITY_MESSAGE

class Periodicity():

    def __init__(self,
                 periodicity):

        try:
            periodicity = periodicity.lower().strip()
            if periodicity not in ['daily', 'weekly']:
                raise PeriodicityError
            self._periodicity = periodicity
        except:
            raise PeriodicityError

    @property
    def periodicity(self):

        return self._periodicity


class RegionNameError(TypeError):

    def __str__(self):

        return constants.REGION_NAME_MESSAGE

class RegionName():

    def __init__(self,
                 name,
                 region_name):

        self._name = Name(name).name

        main_url = '/'.join([constants._CHART_URL,
                             name])
        with requests.Session() as session:
            response = session.get(main_url)
        if not 200 <= response.status_code < 300:
            raise DownloadError
        parser = et.HTMLParser()
        tree = et.parse(io.BytesIO(response.content),
                        parser)
        region_elements = tree.xpath(constants._REGIONS_XPATH)
        all_region_names = [element.text.lower().strip()
                            for element in region_elements]
        try:
            region_name = region_name.lower().strip()
            if region_name not in all_region_names:
                raise RegionNameError
            self._region_name = region_name
        except:
            raise RegionNameError

    @property
    def region_name(self):

        return self._region_name


class RegionNamesError(TypeError):

    def __str__(self):

        return constants.REGION_NAMES_MESSAGE

class RegionNames():

    def __init__(self,
                 name,
                 region_names=None):

        self._name = Name(name).name

        main_url = '/'.join([constants._CHART_URL,
                             self._name])
        with requests.Session() as session:
            response = session.get(main_url)
        if not 200 <= response.status_code < 300:
            raise DownloadError
        parser = et.HTMLParser()
        tree = et.parse(io.BytesIO(response.content),
                        parser)
        region_elements = tree.xpath(constants._REGIONS_XPATH)
        all_region_names = [element.text.lower().strip()
                            for element in region_elements]
        if not region_names:
            self._region_names = all_region_names
        else:
            try:
                region_names = set([region_name.lower().strip()
                                    for region_name in region_names])
                if not region_names.issubset(all_region_names):
                    raise RegionNamesError
                self._region_names = region_names
            except:
                raise RegionNamesError

    @property
    def region_names(self):

        return self._region_names


class BeginDateError(TypeError):

    def __str__(self):

        return constants.BEGIN_DATE_MESSAGE

class BeginDate():

    def __init__(self,
                 begin_date=None):

        min_date = pendulum.date(2008, 10, 7)
        max_date = pendulum.today().date()

        if not begin_date:
            self._begin_date = max_date.subtract(days=30)
        else:
            try:
                begin_date = pendulum.from_format(begin_date.strip(),
                                                  'DD-MM-YYYY').date()
                if max_date < begin_date:
                    raise BeginDateError
                elif begin_date < min_date:
                    begin_date = min_date
                self._begin_date = begin_date
            except:
                raise BeginDateError

    @property
    def begin_date(self):

        return self._begin_date


class EndDateError(TypeError):

    def __str__(self):

        return constants.END_DATE_MESSAGE

class EndDate():

    def __init__(self,
                 end_date=None):

        min_date = pendulum.date(2008, 10, 7)
        max_date = pendulum.today().date()

        if not end_date:
            self._end_date = max_date
        else:
            try:
                end_date = pendulum.from_format(end_date.strip(),
                                                'DD-MM-YYYY').date()
                if min_date > end_date:
                    raise EndDateError
                elif end_date > max_date:
                    end_date = max_date
                self._end_date = end_date
            except:
                raise EndDateError

    @property
    def end_date(self):

        return self._end_date


class WrongDateRangeError(TypeError):

    def __str__(self):

        return constants.WRONG_DATE_RANGE_MESSAGE


class CpuCountError(TypeError):

    def __str__(self):

        return constants.CPU_COUNT_MESSAGE

class CpuCount():

    def __init__(self,
                 cpu_count=None):

        min_cpu_count = 1
        max_cpu_count = mp.cpu_count()

        if not cpu_count:
            self._cpu_count = max_cpu_count
        else:
            try:
                if not isinstance(cpu_count, int):
                    raise CpuCountError
                elif min_cpu_count > cpu_count:
                    cpu_count = min_cpu_count
                elif cpu_count > max_cpu_count:
                    cpu_count = max_cpu_count
                self._cpu_count = cpu_count
            except:
                raise CpuCountError

    @property
    def cpu_count(self):

        return self._cpu_count


class FilePathError(TypeError):

    def __str__(self):

        return constants.FILE_PATH_MESSAGE

class FilePath():

    def __init__(self,
                 name,
                 periodicity,
                 begin_date=None,
                 end_date=None,
                 file_path=None):

        self._name = Name(name).name
        self._periodicity = Periodicity(periodicity).periodicity
        self._begin_date = BeginDate(begin_date).begin_date
        self._end_date = EndDate(end_date).end_date

        if not file_path:
            directory_path = os.getcwd()
            file_name = '_'.join(['spotify',
                                  self._name,
                                  self._periodicity,
                                  'track',
                                  'charts',
                                  'from',
                                  self._begin_date.strftime('%Y-%m-%d'),
                                  'to',
                                  self._end_date.strftime('%Y-%m-%d') + '.csv'])
        else:
            try:
                directory_path = os.path.dirname(file_path)
                file_name = os.path.basename(file_path)
                if not file_name.lower().endswith('.csv'):
                    raise FilePathError
            except:
                raise FilePathError
        file_path = os.path.join(directory_path,
                                 file_name)
        self._file_path = file_path

    @property
    def file_path(self):

        return self._file_path
