import os
import json
import csv
import sys
from datetime import datetime, timedelta
from google.cloud import datastore
from google.oauth2 import service_account
from google.cloud import storage
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

sys.setdefaultencoding('utf-8')

def popular_report(property_id):
    """Runs a simple report on a Google Analytics 4 property."""
    # TODO(developer): Uncomment this variable and replace with your
    #  Google Analytics 4 property ID before running the sample.
    # property_id = "311149968"

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
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
    with open('./popular.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in response.rows:
            writer.writerow([row.dimension_values[0].value, row.dimension_values[1].value, row.metric_values[0].value])
    GCS_PATH = os.environ['GCS_PATH']
    upload_blob('./popular.csv', GCS_PATH + 'popular.csv')


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
