import os


import pandas as pd
import pytest


import spotifycharts as sc



test_arguments = 'name, periodicity'
test_set = [('viral50', 'daily'),
            ('viral50', 'weekly'),
            ('top200', 'daily'),
            ('top200', 'weekly')]
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
    tested = pd.read_csv(file_path)
    tested = tested['region_name'].tolist()
    untested = sc.get_all_regions(name=name,
                                  periodicity=periodicity)
    untested = set(untested.keys())
    assert untested.issuperset(tested)
    untested = sorted(list(untested),
                      reverse=False)
    untested = pd.DataFrame({'region_name': untested})
    untested.to_csv(file_path,
                    index=False)
