import argparse
import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta



CLIENT_SECRETS_FILE = 'client_secret.json'

# These OAuth 2.0 access scopes allow for read-only access to the authenticated
# user's account for both YouTube Data API resources and YouTube Analytics Data.
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v1'

# Authorize the request and store authorization credentials.
def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()

  api_service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
  return api_service

# Remove keyword arguments that are not set.
def remove_empty_args(args):
  original_args = vars(args)
  good_args = {}
  if original_args is not None:
    for key, value in original_args.iteritems():
      # The channel_id and content_owner arguments are provided as a means
      # of properly setting the "ids" parameter value. However, they should
      # not be included in the API request (since they're not parameters
      # supported by this method).
      if value and key != 'channel_id' and key != 'content_owner':
        good_args[key] = value
  return good_args

# Set the "ids" request parameter for the YouTube Analytics API request.
def set_ids_parameter(args):
  if args.content_owner:
    args.ids = 'contentOwner==' + args.content_owner
    if args.filters == '':
      args.filters = 'claimedStatus==claimed'
  elif args.channel_id:
    args.ids = 'channel==' + args.channel_id
  else:
    args.ids = 'channel==MINE'
  args = remove_empty_args(args)
  print args
  return args

def run_analytics_report(youtube_analytics, args):
  
  analytics_query_response = youtube_analytics.reports().query(
    **args
  ).execute()

  #print 'Analytics Data for Channel %s' % channel_id

  for column_header in analytics_query_response.get('columnHeaders', []):
    print '%-20s' % column_header['name'],
  print

  for row in analytics_query_response.get('rows', []):
    for value in row:
      print '%-20s' % value,
    print

if __name__ == '__main__':
  now = datetime.now()
  one_day_ago = (now - timedelta(days=1)).strftime('%Y-%m-%d')
  one_week_ago = (now - timedelta(days=7)).strftime('%Y-%m-%d')

  parser = argparse.ArgumentParser()

  # Set channel ID or content owner. Default is authenticated user's channel.
  parser.add_argument('--channel-id', default='',
      help='YouTube channel ID for which data should be retrieved. ' +
           'Note that the default behavior is to retrieve data for ' +
           'the authenticated user\'s channel.')
  parser.add_argument('--content-owner', default='',
      help='The name of the content owner for which data should be ' +
           'retrieved. If you retrieve data for a content owner, then ' +
           'your API request must also set a value for the "filters" ' +
           'parameter. See the help for that parameter for more details.')

  # Metrics, dimensions, filters
  parser.add_argument('--metrics', help='Report metrics',
    default='views,estimatedMinutesWatched,averageViewDuration')
  parser.add_argument('--dimensions', help='Report dimensions', default='')
  parser.add_argument('--filters', default='',
      help='Filters for the report. Note that the filters request parameter ' +
           'must be set in YouTube Analytics API requests for content owner ' +
           'reports. The script sets "filters=claimedStatus==claimed" if a ' +
           'content owner is specified and filters are not specified.')

  # Report dates. Defaults to start 7 days ago, end yesterday.
  parser.add_argument('--start-date', default=one_week_ago,
    help='Start date, in YYYY-MM-DD format')
  parser.add_argument('--end-date', default=one_day_ago,
    help='End date, in YYYY-MM-DD format')

  parser.add_argument('--max-results', help='Max results')
  parser.add_argument('--sort', help='Sort order', default='')

  args = parser.parse_args()
  args = set_ids_parameter(args)

  youtube_analytics = get_authenticated_service()
  try:
    run_analytics_report(youtube_analytics, args)
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
