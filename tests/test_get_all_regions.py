import os


import pandas as pd
import pytest


from spotifycharts import downloader
from spotifycharts import classes



test_arguments = 'name, periodicity'
test_set = [('viral', 'daily'),
            ('viral', 'weekly'),
            ('regional', 'daily'),
            ('regional', 'weekly')]
@pytest.mark.parametrize(test_arguments,
                         test_set)
def test_get_all_regions(name,
                         periodicity):

    file_name = '_'.join([name,
                          periodicity,
                          'regions']) + '.csv'
    file_path = os.path.join('tests',
                             'test_get_all_regions',
                             'tested',
                             file_name)
    tested = pd.read_csv(file_path)['region_name']
    tested = set(tested.tolist())
    untested = downloader.Downloader.get_all_regions(name=name,
                                                     periodicity=periodicity)
    untested = set(untested.keys())
    assert untested.issuperset(tested)
    untested = list(untested)
    untested = pd.DataFrame({'region_name': untested})
    untested.to_csv(file_path,
                    index=False)
