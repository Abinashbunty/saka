import unittest
from unittest import mock

from google.ads.googleads import errors as google_ads_errors
import google_ads_client as google_ads_client_lib
import pandas as pd
from parameterized import parameterized
from test_utils import fakes

# A fake stream of search term report rows.
_FAKE_SEARCH_TERM_STREAM = [
    fakes.FakeStream([
        fakes.FakeStreamRow(
            search_term='Search term 1',
            status=0,
            conversions=10,
            clicks=20,
            ctr=1,
            ad_group_name='ad group 1',
            campaign_id='123',
            campaign_name='Campaign 1',
            keyword_text='Keyword Term'),
        fakes.FakeStreamRow(
            search_term='Search term 2',
            status=0,
            conversions=20,
            clicks=30,
            ctr=1,
            ad_group_name='ad group 2',
            campaign_id='456',
            campaign_name='Campaign 2',
            keyword_text='Keyword Term'),
        fakes.FakeStreamRow(
            search_term='Search term 3',
            status=0,
            conversions=40,
            clicks=50,
            ctr=1,
            ad_group_name='ad group 3',
            campaign_id='789',
            campaign_name='Campaign 3',
            keyword_text='Keyword Term')
    ])
]


def _build_expected_search_terms_df() -> pd.DataFrame:
  """Builds the expected search terms DataFrame based on _FAKE_STREAM.

  Returns:
    A DataFrame built using the rows in the _FAKE_STREAM.
  """
  expected_cols = ['search_term',
                   'status',
                   'conversions',
                   'clicks',
                   'ad_group_name',
                   'campaign_id',
                   'campaign_name',
                   'ctr',
                   'keyword_text']

  rows = []

  for fake_stream_row in _FAKE_SEARCH_TERM_STREAM[0].results:
    row = {}

    row['search_term'] = fake_stream_row.search_term_view.search_term
    row['status'] = fake_stream_row.search_term_view.status
    row['conversions'] = fake_stream_row.metrics.conversions
    row['clicks'] = fake_stream_row.metrics.clicks
    row['ad_group_name'] = fake_stream_row.ad_group.name
    row['campaign_id'] = fake_stream_row.campaign.id
    row['campaign_name'] = fake_stream_row.campaign.name
    row['ctr'] = fake_stream_row.metrics.ctr
    row['keyword_text'] = fake_stream_row.segments.keyword.info.text

    rows.append(row)

  return pd.DataFrame(rows, columns=expected_cols)


class GoogleAdsTest(unittest.TestCase):

  def test_get_search_terms(self):
    """Tests that get_search_terms returns the expected DataFrame."""

    # Arrange
    # The API client is used to get the API service, and the API service
    # is used to return a stream of results. To mock this, we do the following:

    # 1. Set up a mock client
    mock_client = mock.MagicMock()

    # 2. Set up a mock service
    mock_service = mock.MagicMock()

    # 3. Set the mock service to return a fake stream of search term data
    mock_service.search_stream.return_value = _FAKE_SEARCH_TERM_STREAM

    # 4. Set up the mock client to return the mock service
    mock_client.get_service.return_value = mock_service

    with mock.patch('google.ads.googleads.client.GoogleAdsClient.load_from_dict'
                   ) as mock_ads_client:
      mock_ads_client.return_value = mock_client
      expected_df = _build_expected_search_terms_df()
      google_ads_client = google_ads_client_lib.GoogleAdsClient({})

      # Act
      actual_df = google_ads_client.get_search_terms(customer_id='0123456789')

      # Assert
      pd.testing.assert_frame_equal(expected_df, actual_df)

  @parameterized.expand([
      ('12345'),  # Too short
      ('12345678910'),  # Too long
      ('abc1234567'),  # Non-numeric
  ])
  def test_get_search_terms_invalid_client_id_raises_error(self, customer_id):
    """Tests invalid client ids raise the expected error."""
    # Arrange
    mock_client = mock.MagicMock()
    mock_service = mock.MagicMock()
    mock_client.get_service.return_value = mock_service

    with mock.patch('google.ads.googleads.client.GoogleAdsClient.load_from_dict'
                   ) as mock_ads_client:
      mock_ads_client.return_value = mock_client
      google_ads_client = google_ads_client_lib.GoogleAdsClient({})

      # Act / Assert
      with self.assertRaises(google_ads_client_lib.SAGoogleAdsClientError):
        google_ads_client.get_search_terms(customer_id=customer_id)

  def test_get_search_terms_client_error_raises_error(self):
    """Tests error while initializing a client raises the expected error."""
    # Arrange
    mock_client = mock.MagicMock()
    mock_service = mock.MagicMock()
    mock_client.get_service.return_value = mock_service

    with mock.patch('google.ads.googleads.client.GoogleAdsClient.load_from_dict'
                   ) as mock_ads_client:
      mock_ads_client.side_effect = google_ads_errors.GoogleAdsException(
          error=ValueError('Invalid Credential Key'),
          call=None,
          failure=None,
          request_id='')

      # Act / Assert
      with self.assertRaises(google_ads_client_lib.SAGoogleAdsClientError):
        google_ads_client_lib.GoogleAdsClient({})

  def test_get_search_terms_service_error_raises_error(self):
    """Tests error while using the API service raises the expected error."""
    # Arrange
    mock_client = mock.MagicMock()
    mock_service = mock.MagicMock()
    mock_service.search_stream.side_effect = google_ads_errors.GoogleAdsException(
        error=RuntimeError('API Unavailable'),
        call=None,
        failure=None,
        request_id='')
    mock_client.get_service.return_value = mock_service

    with mock.patch('google.ads.googleads.client.GoogleAdsClient.load_from_dict'
                   ) as mock_ads_client:
      mock_ads_client.return_value = mock_client
      google_ads_client = google_ads_client_lib.GoogleAdsClient({})

      # Act / Assert
      with self.assertRaises(google_ads_client_lib.SAGoogleAdsClientError):
        google_ads_client.get_search_terms(customer_id='0123456789')


if __name__ == '__main__':
  unittest.main()