import os
import json
import csv
import sys
import codecs
from datetime import datetime, timedelta
from google.cloud import datastore
from google.oauth2 import service_account
from google.cloud import storage
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

def popular_report(property_id):
    """Runs a simple report on a Google Analytics 4 property."""
    # TODO(developer): Uncomment this variable and replace with your
    #  Google Analytics 4 property ID before running the sample.
    # property_id = "311149968"

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    print(os.environ['LC_ALL'])
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    client = BetaAnalyticsDataClient()

    current_time = datetime.now()
    start_datetime = current_time - timedelta(days=7)
    start_date = datetime.strftime(start_datetime, '%Y-%m-%d')

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
		    Dimension(name="pageTitle"),
		    Dimension(name="pagePath")
		],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date=start_date, end_date="today")],
    )
    response = client.run_report(request)

    print("Report result:")
    report = []
    for row in response.rows:
        #writer.writerow([row.dimension_values[0].value, row.dimension_values[1].value.encode('utf-8'), row.metric_values[0].value])
        report.append([row.dimension_values[0].value, row.dimension_values[1].value.encode('utf-8'), row.metric_values[0].value])
    GCS_PATH = os.environ['GCS_PATH']
    upload_data(bucket, report, str, GCS_PATH + 'popular.csv')

def upload_data(bucket_name: str, data: bytes, content_type: str, destination_blob_name: str):
    '''Uploads a file to the bucket.'''
    # bucket_name = 'your-bucket-name'
    # data = 'storage-object-content'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    # blob.content_encoding = 'gzip'
    blob.upload_from_string(
        # data=gzip.compress(data=data, compresslevel=9),
        data=bytes(data.encode('utf-8')),
        content_type=content_type, client=storage_client)
    blob.content_language = 'zh'
    blob.cache_control = 'max-age=300,public'
    blob.patch()

def upload_blob(source, destination_file):
    storage_client = storage.Client()
    #.from_service_account_json('gcs-key.json')
    bucket = storage_client.bucket(os.environ['BUCKET'])
    blob = bucket.blob(source)
    blob.upload_from_filename(destination_file)
    print("File {} uploaded to {}.".format(destination_file, destination_file))
    blob.patch()


if __name__ == "__main__":  
	if 'GA_RESOURCE_ID' in os.environ:
		ga_id = os.environ['GA_RESOURCE_ID']
	else:
		ga_id = "311149968"
	popular_report(ga_id)
