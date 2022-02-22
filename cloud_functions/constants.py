"""Shared constants used in classes for the SAKA solution."""

# Cloud Function Environment variables.
GCP_PROJECT_ID: str = 'GCP_PROJECT_ID'
CUSTOMER_ID: str = 'CUSTOMER_ID'
SA360_SFTP_USERNAME: str = 'SA360_SFTP_USERNAME'
SA360_ACCOUNT_NAME: str = 'SA360_ACCOUNT_NAME'
SA360_LABEL: str = 'SA360_LABEL'
CLICKS_THRESHOLD: str = 'CLICKS_THRESHOLD'
CONVERSIONS_THRESHOLD: str = 'CONVERSIONS_THRESHOLD'
SEARCH_TERMS_TOKENS_THRESHOLD: str = 'SEARCH_TERMS_TOKENS_THRESHOLD'
CAMPAIGN_IDS: str = 'CAMPAIGN_IDS'

# Bulksheet Filtering Logic and Settings Defaults.
DEFAULT_CLICKS_THRESHOLD: int = 5
DEFAULT_CONVERSIONS_THRESHOLD: int = 0
DEFAULT_SEARCH_TERM_TOKENS_THRESHOLD: int = 3
DEFAULT_SA360_ACCOUNT_NAME: str = 'Google'
DEFAULT_SA360_LABEL: str = 'SA_add'

# SA360 Connection Constants.
SA360_SFTP_HOSTNAME: str = 'partnerupload.google.com'
SA360_SFTP_PORT: str = 19321

# Cloud Secret Manager Secrets.
GOOGLE_ADS_API_CREDENTIALS: str = 'google_ads_api_credentials'
SA360_SFTP_PASSWORD: str = 'sa360_sftp_password'

# Google Ads Client Constants.
CUSTOMER_ID_LENGTH = 10
DATE_RANGE = 'LAST_30_DAYS'
GOOGLE_ADS_SERVICE_NAME = 'GoogleAdsService'
SEARCH_REQUEST_TYPE = 'SearchGoogleAdsStreamRequest'
SEARCH_REPORT_COLUMNS = [
    'search_term', 'status', 'conversions', 'clicks', 'ad_group_name',
    'campaign_id', 'campaign_name', 'ctr', 'keyword_text'
]
AD_GROUP_COLUMNS = ['ad_group_name', 'ctr']
KEYWORD_COLUMNS = ['ad_group_name', 'keyword', 'match_type']

SEARCH_REPORT_QUERY = f"""
  SELECT
    search_term_view.search_term,
    search_term_view.status,
    metrics.conversions,
    metrics.clicks,
    ad_group.name,
    campaign.id,
    campaign.name,
    metrics.ctr,
    segments.keyword.info.text
   FROM
    search_term_view
   WHERE
    segments.date DURING {DATE_RANGE}
    AND search_term_view.status IN ('NONE', 'UNKNOWN')
"""

AD_GROUP_QUERY = f"""
  SELECT
    ad_group.name,
    metrics.ctr
  FROM
    ad_group
  WHERE
    segments.date DURING {DATE_RANGE}
"""

KEYWORDS_QUERY = """
  SELECT
    ad_group.name,
    ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type
  FROM
    ad_group_criterion
  WHERE
    ad_group_criterion.type = KEYWORD
"""

# Search Term Transformer Constants.
MATCH_TYPE_BROAD = 'broad'
MATCH_TYPE_EXACT = 'exact'
MATCH_TYPE_PHRASE = 'phrase'

SA_360_BULKSHEET_COLUMNS = [
    'Row type',
    'Action',
    'Account',
    'Campaign',
    'Ad group',
    'Keyword',
    'Keyword match type',
    'Label',
]