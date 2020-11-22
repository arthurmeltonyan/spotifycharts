import fastapi
from fastapi import status
from fastapi import responses

from application.api import spotifycharts as sc


downloading = fastapi.APIRouter()


@downloading.get('/regions/{name}',
                 response_class=responses.ORJSONResponse,
                 status_code=status.HTTP_200_OK)
def download_regions(name):
    try:
        region_names = [region_name.replace(' ', '_')
                        for region_name in sc.download_regions(name).keys()]
    except sc.exceptions.ArgumentTypeError as exception:
        responses.status_code = status.HTTP_400_BAD_REQUEST
        return {'error_message': str(exception)}
    else:
        return {'name': name,
                'region_names': region_names}


@downloading.get('/dates/{name}/{periodicity}/{region_name}',
                 response_class=responses.ORJSONResponse,
                 status_code=status.HTTP_200_OK)
def download_dates(name,
                   periodicity,
                   region_name):
    try:
        dates = [date
                 for date in sc.download_dates(name,
                                               periodicity,
                                               region_name.replace('_', ' ')).keys()]
    except sc.exceptions.ArgumentTypeError as exception:
        responses.status_code = status.HTTP_400_BAD_REQUEST
        return {'error_message': str(exception)}
    else:
        return {'name': name,
                'periodicity': periodicity,
                'dates': dates}


@downloading.get('/charts/{name}/{periodicity}/{region_name}/{begin_date}--{end_date}',
                 response_class=responses.ORJSONResponse,
                 status_code=status.HTTP_200_OK)
def download_charts(name,
                    periodicity,
                    region_name,
                    begin_date,
                    end_date):
    try:
        downloader = sc.Downloader(name=name,
                                   periodicity=periodicity,
                                   region_names=[region_name.replace('_', ' ')],
                                   begin_date=begin_date,
                                   end_date=end_date,
                                   directory_path='downloaded')
        charts = [chart.to_dict(orient='records')
                  for date, chart in downloader[region_name.replace('_', ' ')].groupby('date')]
    except sc.exceptions.ArgumentTypeError as exception:
        responses.status_code = status.HTTP_400_BAD_REQUEST
        return {'error_message': str(exception)}
    else:
        return {'name': name,
                'periodicity': periodicity,
                'region_name': region_name.replace('_', ' '),
                'charts': charts}
