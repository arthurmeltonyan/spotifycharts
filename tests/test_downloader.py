import os


import pandas as pd
import pytest


import spotifycharts as sc



test_arguments = 'name, periodicity, region_names, begin_date, end_date, cpu_count'
test_set = [('viral50', 'daily', None, '2019-12-30', '2020-01-05', 1),
            ('viral50', 'weekly', None, '2019-12-30', '2020-01-05', 1),
            ('top100', 'daily', None, '2019-12-30', '2020-01-05', 1),
            ('top100', 'weekly', None, '2019-12-30', '2020-01-05', 1),
            ('viral50', 'daily', ['germany', 'france', 'italy'], '2019-12-30', '2020-01-05', None),
            ('viral50', 'weekly', ['germany', 'france', 'italy'], '2019-12-30', '2020-01-05', None),
            ('top100', 'daily', ['germany', 'france', 'italy'], '2019-12-30', '2020-01-05', None),
            ('top100', 'weekly', ['germany', 'france', 'italy'], '2019-12-30', '2020-01-05', None)]
@pytest.mark.parametrize(test_arguments,
                         test_set)
def test_download(name,
                  periodicity,
                  region_names,
                  begin_date,
                  end_date,
                  cpu_count):

    if region_names:
        file_name = '_'.join(['_'.join(region_names),
                              'spotify',
                              name,
                              periodicity,
                              'track',
                              'charts',
                              'from',
                              begin_date,
                              'to',
                              end_date]) + '.csv'
    else:
        file_name = '_'.join(['global',
                              'spotify',
                              name,
                              periodicity,
                              'track',
                              'charts',
                              'from',
                              begin_date,
                              'to',
                              end_date]) + '.csv'
    tested_file_path = os.path.join('tests',
                                    'test_downloader',
                                    'tested',
                                    file_name)
    tested = sc.Downloader(name=name,
                           periodicity=periodicity,
                           region_names=region_names,
                           begin_date=begin_date,
                           end_date=end_date,
                           cpu_count=cpu_count,
                           file_path=tested_file_path).data
    untested_file_path = os.path.join('tests',
                                      'test_downloader',
                                      'untested',
                                      file_name)
    untested = sc.Downloader(name=name,
                             periodicity=periodicity,
                             region_names=region_names,
                             begin_date=begin_date,
                             end_date=end_date,
                             cpu_count=cpu_count,
                             file_path=untested_file_path).data
    assert tested['artist_name'].tolist() == untested['artist_name'].tolist() \
    and tested['track_name'].tolist() == untested['track_name'].tolist()
