import os


import pandas as pd
import pytest


from spotifycharts import downloader
from spotifycharts import classes



test_arguments = 'name, periodicity, begin_date, end_date, region_names'
test_set = [('viral', 'daily', '30-12-2019', '05-01-2020', None),
            ('viral', 'weekly', '30-12-2019', '05-01-2020', None),
            ('regional', 'daily', '30-12-2019', '05-01-2020', None),
            ('regional', 'weekly', '30-12-2019', '05-01-2020', None),
            ('viral', 'daily', '30-12-2019', '05-01-2020', ['united states', 'france']),
            ('viral', 'weekly', '30-12-2019', '05-01-2020', ['united states', 'france']),
            ('regional', 'daily', '30-12-2019', '05-01-2020', ['united states', 'france']),
            ('regional', 'weekly', '30-12-2019', '05-01-2020', ['united states', 'france'])]
@pytest.mark.parametrize(test_arguments,
                         test_set)
def test_download(name,
                  periodicity,
                  begin_date,
                  end_date,
                  region_names):

    if region_names:
        region = 'some'
    else:
        region = 'all'
    file_name = '_'.join([region,
                          name,
                          periodicity,
                          'charts',
                          begin_date,
                          end_date]) + '.csv'
    tested_file_path = os.path.join('tests',
                                    'test_download',
                                    'tested',
                                    file_name)
    untested_file_path = os.path.join('tests',
                                      'test_download',
                                      'untested',
                                      file_name)
    untested = downloader.Downloader(name=name,
                                     periodicity=periodicity,
                                     begin_date=begin_date,
                                     end_date=end_date,
                                     region_names=region_names,
                                     file_path=untested_file_path)
    untested.download()
    untested = untested.data
    tested = pd.read_csv(tested_file_path)
    assert untested['date'].tolist() == tested['date'].tolist() and \
    untested['region_name'].tolist() == tested['region_name'].tolist()
