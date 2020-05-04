# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotifycharts']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.5.0,<5.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pendulum>=2.1.0,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.46.0,<5.0.0']

setup_kwargs = {
    'name': 'spotifycharts',
    'version': '2020.5.1',
    'description': 'The easy-to-use package for downloading Spotify charts with Python.',
    'long_description': "spotifycharts\n*************\n\n``spotifycharts`` module provides data scientists and music enthusiasts with the simple yet effective out-of-box solution to the problem of obtaining `spotifycharts.com <https://github.com/niltonvolpato/python-progressbar>`__ data.\n\n\nInstallation\n############\n\nThe recommended way to install ``spotifycharts`` module is to simply use pip:\n\n.. code:: sh\n\n    pip3 install spotifycharts\n\nIt installs all the dependencies as well:\n\n- pendulum\n- pandas\n- requests\n- lxml\n- tqdm\n\n``spotifycharts`` officially supports only Python 3.\n\n\nUsage\n#####\n\n``download`` method downloads ``name`` charts of ``region_names`` from ``begin_date`` to ``end_date`` on a ``periodicity`` basis using ``cpu_count`` of cores and save them into the ``file_path``:\n\n.. code:: python\n\n    from spotifycharts import downloader\n    sc_downloader = downloader.Downloader(name='viral',\n                                          periodicity='weekly',\n                                          region_names=['united states'],\n                                          begin_date='30-12-2019',\n                                          end_date='05-01-2020',\n                                          cpu_count=2,\n                                          file_path='data.csv')\n    sc_downloader.download()\n\n``get_all_regions`` method lists all available regions of ``name`` charts on a ``periodicity`` basis:\n\n.. code:: python\n\n    downloader.Downloader.get_all_regions(name='viral',\n                                          periodicity='weekly')\n\n``get_all_dates`` method lists all available dates of ``name`` charts in ``region_name`` on a ``periodicity`` basis:\n\n.. code:: python\n\n    downloader.Downloader.get_all_dates(name='regional',\n                                        periodicity='daily',\n                                        region_name='france')\n\n``Downloader`` constructor also grants the access to ``name``, ``periodicity``, ``region_names``, ``begin_date``, ``end_date``, ``file_path`` and ``data`` attributes:\n\n.. code:: python\n\n      name = sc_downloader.name\n      periodicity = sc_downloader.periodicity\n      region_names = sc_downloader.region_names\n      begin_date = sc_downloader.begin_date\n      end_date = sc_downloader.end_date\n      file_path = sc_downloader.file_path\n      data = sc_downloader.data\n",
    'author': 'Arthur Meltonyan',
    'author_email': 'arthur.meltonyan@gmail.com',
    'maintainer': 'Arthur Meltonyan',
    'maintainer_email': 'arthur.meltonyan@gmail.com',
    'url': 'https://github.com/arthurmeltonyan/spotifycharts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
