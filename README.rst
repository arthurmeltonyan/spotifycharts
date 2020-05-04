spotifycharts
*************

``spotifycharts`` module provides data scientists and music enthusiasts with the simple yet effective out-of-box solution to the problem of obtaining `spotifycharts.com <https://github.com/niltonvolpato/python-progressbar>`__ data.


Installation
############

The recommended way to install ``spotifycharts`` module is to simply use pip:

.. code:: sh

    pip3 install spotifycharts

It installs all the dependencies as well:

- pendulum
- pandas
- requests
- lxml
- tqdm

``spotifycharts`` officially supports only Python 3.


Usage
#####

``download`` method downloads ``name`` charts of ``region_names`` from ``begin_date`` to ``end_date`` on a ``periodicity`` basis using ``cpu_count`` of cores and save them into the ``file_path``:

.. code:: python

    from spotifycharts import downloader
    sc_downloader = downloader.Downloader(name='viral',
                                          periodicity='weekly',
                                          region_names=['united states'],
                                          begin_date='30-12-2019',
                                          end_date='05-01-2020',
                                          cpu_count=2,
                                          file_path='data.csv')
    sc_downloader.download()

``get_all_regions`` method lists all available regions of ``name`` charts on a ``periodicity`` basis:

.. code:: python

    downloader.Downloader.get_all_regions(name='viral',
                                          periodicity='weekly')

``get_all_dates`` method lists all available dates of ``name`` charts in ``region_name`` on a ``periodicity`` basis:

.. code:: python

    downloader.Downloader.get_all_dates(name='regional',
                                        periodicity='daily',
                                        region_name='france')

``Downloader`` constructor also grants the access to ``name``, ``periodicity``, ``region_names``, ``begin_date``, ``end_date``, ``file_path`` and ``data`` attributes:

.. code:: python

      name = sc_downloader.name
      periodicity = sc_downloader.periodicity
      region_names = sc_downloader.region_names
      begin_date = sc_downloader.begin_date
      end_date = sc_downloader.end_date
      file_path = sc_downloader.file_path
      data = sc_downloader.data
