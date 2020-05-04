import io


import pandas as pd
import requests
from lxml import etree as et
from tqdm.auto import tqdm


from spotifycharts import classes
from spotifycharts import constants



def download(url,
             chart_date,
             region_name):

    try:
        with requests.Session() as session:
            response = session.get(url)
        if not 200 <= response.status_code < 300:
            raise classes.DownloadError
        parser = et.HTMLParser()
        tree = et.parse(io.BytesIO(response.content),
                        parser)
        is_chart_erroneous = tree.xpath(constants._ERRONEOUS_CHART_XPATH)
        is_chart_unfound = tree.xpath(constants._UNFOUND_CHART_XPATH)
        if is_chart_erroneous or is_chart_unfound:
            raise classes.DownloadError
        name = url.split('/')[3]
        chart = response.text[response.text.find('Position'):]
        header = chart.splitlines()[0]
        is_chart_viral = name == 'viral' and header == constants._VIRAL_CHART_HEADER
        is_chart_regional = name == 'regional' and header == constants._REGIONAL_CHART_HEADER
        if not is_chart_viral and not is_chart_regional:
            raise classes.DownloadError
        chart = pd.read_csv(io.StringIO(chart),
                            sep=',')
        if chart.shape[1] == 4:
            chart.columns = constants._VIRAL_CHART_COLUMNS
        else:
            chart.columns = constants._REGIONAL_CHART_COLUMNS
        chart['artist_name'] = chart['artist_name'].str.lower().str.strip()
        chart['track_name'] = chart['track_name'].str.lower().str.strip()
        chart['region_name'] = region_name
        chart['date'] = chart_date.format('YYYY-MM-DD')
        return chart
    except classes.DownloadError as exception:
        tqdm.write(str(exception) + url)
        return pd.DataFrame()
