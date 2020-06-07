import os


import pandas as pd
import pendulum
import pytest


import spotifycharts as sc



test_arguments = 'name, periodicity'
test_set = [('viral50', 'daily'),
            ('viral50', 'weekly'),
            ('top200', 'daily'),
            ('top200', 'weekly')]
@pytest.mark.parametrize(test_arguments,
                         test_set)
def test_get_all_dates(name,
                       periodicity):

    file_name = '_'.join([name,
                          periodicity,
                          'dates']) + '.csv'
    file_path = os.path.join('tests',
                             'test_get_all_dates',
                             'tested',
                             file_name)
    tested = pd.read_csv(file_path)
    tested = tested['chart_date'].tolist()
    untested = sc.get_all_dates(name=name,
                                periodicity=periodicity)
    untested = set([date.format('YYYY-MM-DD')
                    for date in untested])
    assert untested.issuperset(tested)
    untested = sorted(list(untested),
                      reverse=True)
    untested = pd.DataFrame({'chart_date': untested})
    untested.to_csv(file_path,
                    index=False)
