import io
import os


import pendulum
from pendulum.date import Date
import requests
from lxml import etree as et
from pathos import multiprocessing as mp


from spotifycharts import constants



class _Name(str):

    def __new__(cls,
                name):

        try:
            name = name.lower().strip()
            if name not in constants._NAME_VALUES:
                raise TypeError
        except:
            message = constants._NAME_MESSAGE
            message = message.format(name=name)
            raise TypeError(message)
        else:
            return str.__new__(cls,
                               name)


class _Periodicity(str):

    def __new__(cls,
                periodicity):

        try:
            periodicity = periodicity.lower().strip()
            if periodicity not in constants._PERIODICITY_VALUES:
                raise TypeError
        except:
            message = constants._PERIODICITY_MESSAGE
            message = message.format(periodicity=periodicity)
            raise TypeError(message)
        else:
            return str.__new__(cls,
                               periodicity)


class _RegionName(str):

    def __new__(cls,
                name,
                region_name):

        name = _Name(name)

        name_code = constants._NAME_VALUES[name]

        main_url = constants._MAIN_URL.format(name_code=name_code)
        with requests.Session() as session:
            response = session.get(main_url)
        if response.status_code != 200:
            message = constants._REGION_DOWNLOAD_MESSAGE
            message = message.format(url=main_url)
            raise ConnectionError(message)
        tree = et.parse(io.StringIO(response.text),
                        et.HTMLParser())
        region_elements = tree.xpath(constants._REGIONS_XPATH)
        all_region_names = [region_element.text.lower().strip()
                            for region_element in region_elements]
        if not region_name:
            return str.__new__(cls,
                               constants._DEFAULT_REGION_NAME)
        try:
            region_name = region_name.lower().strip()
            if region_name not in all_region_names:
                raise TypeError
        except:
            message = constants._REGION_NAME_MESSAGE
            message = message.format(region_name=region_name)
            raise TypeError(message)
        else:
            return str.__new__(cls,
                               region_name)


class _RegionNames(str):

    def __new__(cls,
                name,
                region_names):

        name = _Name(name)

        name_code = constants._NAME_VALUES[name]

        main_url = constants._MAIN_URL.format(name_code=name_code)
        with requests.Session() as session:
            response = session.get(main_url)
        if response.status_code != 200:
            message = constants._REGION_DOWNLOAD_MESSAGE
            message = message.format(url=main_url)
            raise ConnectionError(message)
        tree = et.parse(io.StringIO(response.text),
                        et.HTMLParser())
        region_elements = tree.xpath(constants._REGIONS_XPATH)
        all_region_names = [region_element.text.lower().strip()
                            for region_element in region_elements]
        if not region_names:
            return [str.__new__(cls,
                                constants._DEFAULT_REGION_NAME)]
        try:
            region_names = set([region_name.lower().strip()
                                for region_name in region_names])
            if not region_names.issubset(all_region_names):
                raise TypeError
        except:
            region_names = ', '.join(region_names)
            message = constants._REGION_NAMES_MESSAGE
            message = message.format(region_names=region_names)
            raise TypeError(message)
        else:
            return [str.__new__(cls,
                                region_name)
                    for region_name in region_names]


class _DateRange(Date):

    def __new__(cls,
                begin_date,
                end_date):

        min_date = pendulum.from_format(constants._FOUNDATION_DATE,
                                        constants._FILE_DATE_FORMAT).date()
        max_date = pendulum.today().date()

        if not begin_date:
            months = constants._DEFAULT_MONTH_PERIOD
            begin_date = Date.__new__(cls,
                                      max_date.subtract(months=months).year,
                                      max_date.subtract(months=months).month,
                                      max_date.subtract(months=months).day)
        else:
            try:
                begin_date = pendulum.from_format(begin_date.strip(),
                                                  constants._FILE_DATE_FORMAT)
                begin_date = begin_date.date()
                if max_date < begin_date:
                    raise TypeError
                elif begin_date < min_date:
                    begin_date = Date.__new__(cls,
                                            min_date.year,
                                            min_date.month,
                                            min_date.day)
            except:
                begin_date = begin_date.format(constants._FILE_DATE_FORMAT)
                message = constants._BEGIN_DATE_MESSAGE
                message = message.format(begin_date=begin_date)
                raise TypeError(message)
            else:
                begin_date = Date.__new__(cls,
                                        begin_date.year,
                                        begin_date.month,
                                        begin_date.day)

        if not end_date:
            end_date = Date.__new__(cls,
                                    max_date.year,
                                    max_date.month,
                                    max_date.day)
        else:
            try:
                end_date = pendulum.from_format(end_date.strip(),
                                                constants._FILE_DATE_FORMAT)
                end_date = end_date.date()
                if min_date > end_date:
                    raise TypeError
                elif end_date > max_date:
                    end_date = Date.__new__(cls,
                                            max_date.year,
                                            max_date.month,
                                            max_date.day)
            except:
                end_date = end_date.format(constants._FILE_DATE_FORMAT)
                message = constants._END_DATE_MESSAGE
                message = message.format(end_date=end_date)
                raise TypeError(message)
            else:
                end_date = Date.__new__(cls,
                                        end_date.year,
                                        end_date.month,
                                        end_date.day)

        if begin_date > end_date:
            message = constants._WRONG_DATE_RANGE_MESSAGE
            message = message.format(begin_date=begin_date,
                                     end_date=end_date)
            raise TypeError(message)

        return begin_date, end_date


class _CpuCount(int):

    def __new__(cls,
                cpu_count):

        min_cpu_count = 1
        max_cpu_count = mp.cpu_count()

        if not cpu_count:
            return int.__new__(cls,
                               max_cpu_count)
        try:
            if not isinstance(cpu_count, int):
                raise TypeError
            elif min_cpu_count > cpu_count:
                return int.__new__(cls,
                                   min_cpu_count)
            elif cpu_count > max_cpu_count:
                return int.__new__(cls,
                                   max_cpu_count)
        except:
            cpu_count = str(cpu_count)
            message = constants._CPU_COUNT_MESSAGE
            message = message.format(cpu_count=cpu_count)
            raise TypeError(message)
        else:
            return int.__new__(cls,
                               cpu_count)


class _FilePath(str):

    def __new__(cls,
                name,
                periodicity,
                begin_date,
                end_date,
                file_path):

        name = _Name(name)
        periodicity = _Periodicity(periodicity)
        begin_date, end_date = _DateRange(begin_date,
                                          end_date)
        begin_date = begin_date.format(constants._FILE_DATE_FORMAT)
        end_date = end_date.format(constants._FILE_DATE_FORMAT)

        if not file_path:
            directory_path = os.getcwd()
            file_name = constants._FILE_NAME
            file_name = file_name.format(name=name,
                                         periodicity=periodicity,
                                         begin_date=begin_date,
                                         end_date=end_date)
            file_path = os.path.join(directory_path,
                                     file_name)
            return str.__new__(cls,
                               file_path)
        try:
            directory_path = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            if file_path != file_name and not os.path.exists(directory_path):
                os.makedirs(directory_path)
            if not file_name.lower().strip().endswith(constants._FILE_EXTENSION):
                raise TypeError
        except:
            message = constants._FILE_PATH_MESSAGE
            message = message.format(file_path=file_path)
            raise TypeError(message)
        else:
            return str.__new__(cls,
                               file_path)