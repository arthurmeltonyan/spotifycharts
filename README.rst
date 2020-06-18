spotifycharts
*************

``spotifycharts`` provides data scientists and music enthusiasts with the simple yet effective out-of-box solution to the problem of obtaining `spotifycharts.com <https://github.com/niltonvolpato/python-progressbar>`__ data.


Installation
############

Dependencies are listed below:

- pendulum
- pandas
- pathos
- httpx
- lxml
- tqdm

``spotifycharts`` officially supports only Python 3.

The recommended way to install ``spotifycharts`` is to simply use pip:

.. code:: sh

    pip install spotifycharts


Usage
#####

``Downloader`` class downloads ``name`` charts of ``region_names`` from ``begin_date`` to ``end_date`` on a ``periodicity`` basis with the use of ``cpu_count`` cores saving them into the ``file_path`` and also grants the access to its corresponding attributes:

.. code:: python

    import spotifycharts as sc
    downloader = sc.Downloader(name='viral50',
                               periodicity='weekly',
                               region_names=['united states'],
                               begin_date='2019-12-30',
                               end_date='2020-01-05',
                               cpu_count=2,
                               file_path='data.csv')
    data = downloader.data

``get_all_regions`` lists all available regions of ``name`` charts on a ``periodicity`` basis:

.. code:: python

    import spotifycharts as sc
    regions = sc.get_all_regions(name='top200',
                                 periodicity='weekly')

``get_all_dates`` lists all available dates of ``name`` charts in ``region_name`` on a ``periodicity`` basis:

.. code:: python

    import spotifycharts as sc
    dates = sc.get_all_dates(name='top200',
                             periodicity='daily',
                             region_name='france')
