import os


import pandas as pd
import pendulum
import pytest


from spotifycharts import downloader
from spotifycharts import classes



test_arguments = 'name, periodicity, region_name'
test_set = [('viral', 'daily', 'global'),
            ('viral', 'weekly', 'global'),
            ('regional', 'daily', 'global'),
            ('regional', 'weekly', 'global')]
@pytest.mark.parametrize(test_arguments,
                         test_set)
def test_get_all_dates(name,
                       periodicity,
                       region_name):

    file_name = '_'.join([region_name,
                          name,
                          periodicity,
                          'dates']) + '.csv'
    file_path = os.path.join('tests',
                             'test_get_all_dates',
                             'tested',
                             file_name)
    tested = pd.read_csv(file_path)['chart_date']
    tested = set([pendulum.from_format(date, 'YYYY-MM-DD').date()
                  for date in tested.tolist()])
    untested = downloader.Downloader.get_all_dates(name=name,
                                                   periodicity=periodicity,
                                                   region_name=region_name)
    untested = set(untested.keys())
    assert untested.issuperset(tested)
    untested = [date.format('YYYY-MM-DD')
                for date in untested]
    untested = pd.DataFrame({'chart_date': untested})
    untested.to_csv(file_path,
                    index=False)
