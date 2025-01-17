# SAKA (SA360 Keyword Automator)

*Copyright 2022 Google LLC. This solution, including any related sample code or
data, is made available on an “as is,” “as available,” and “with all faults”
basis, solely for illustrative purposes, and without warranty or representation
of any kind. This solution is experimental, unsupported and provided solely for
your convenience. Your use of it is subject to your agreements with Google, as
applicable, and may constitute a beta feature as defined under those agreements.
To the extent that you make any data available to Google in connection with your
use of the solution, you represent and warrant that you have all necessary and
appropriate rights, consents and permissions to permit Google to use and process
that data. By using any portion of this solution, you acknowledge, assume and
accept all risks, known and unknown, associated with its usage, including with
respect to your deployment of any portion of this solution in your systems, or
usage in connection with your business, if at all.*

## Overview

SAKA is a Google Cloud-based packaged solution that automates uploads of
keywords to SA360 based on Google Ads search terms report results. Search terms
that have been identified to have some level of impact by this solution and that
do not yet exist as keywords in the campaign ad group will be added by SAKA with
the goal of increasing keyword coverage and ad performance.

## Prerequisites

In order to use this solution, you must have the following:

-   [ ] A Google Ads Account.
-   [ ] A Google Ads API developer token.
-   [ ] A Search Ads 360 Account ("SA360"), with FTP server access. See
    [here](https://support.google.com/searchads/answer/7409125?hl=en) for
    details.
-   [ ] A
    [Google Cloud Platform ("GCP") project](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
    with an attached billing account. (If a billing account has not been set on
    the project, set one by
    [following these instructions](https://cloud.google.com/billing/docs/how-to/modify-project))

***For users not using GCP Cloud Shell, the steps below are also required:***

-   [ ] Have
    [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
    installed locally on your machine.
-   [ ] [Install the Google Cloud SDK](https://cloud.google.com/sdk/) to be able
    to run the installation script. Ensure both alpha and beta are installed,
    and update components to the latest versions:

    -   `gcloud components install alpha`

    -   `gcloud components install beta`

    -   `gcloud components update`

## Cost / Components

The following GCP components are used by SAKA:

Service Name              | Required API Activation       | Pricing Information
------------------------- | ----------------------------- | -------------------
Cloud Build               | cloudbuild.googleapis.com     | [https://cloud.google.com/build/pricing](https://cloud.google.com/build/pricing)
Cloud Functions           | cloudfunctions.googleapis.com | [https://cloud.google.com/functions/pricing](https://cloud.google.com/functions/pricing)
Cloud Scheduler           | cloudscheduler.googleapis.com | [https://cloud.google.com/scheduler/pricing](https://cloud.google.com/scheduler/pricing)
Cloud Logging             | logging.googleapis.com        | [https://cloud.google.com/stackdriver/pricing#google-clouds-operations-suite-pricing](https://cloud.google.com/stackdriver/pricing#google-clouds-operations-suite-pricing)
Cloud PubSub              | pubsub.googleapis.com         | [https://cloud.google.com/pubsub/pricing](https://cloud.google.com/pubsub/pricing)
Cloud Secret Manager      | secretmanager.googleapis.com  | [https://cloud.google.com/secret-manager/pricing](https://cloud.google.com/secret-manager/pricing)
Cloud Source Repositories | sourcerepo.googleapis.com     | [https://cloud.google.com/source-repositories/pricing](https://cloud.google.com/source-repositories/pricing)

Check the pricing page for each component to confirm currrent pricing.

## Setup Guide

This section will explain how to setup SAKA for use in a GCP environment.

### 1. Download / Clone the Repository

In GCP Cloud Shell or your local terminal, either clone this repository using
git, or download the code as a tarball by clicking the "tgz" link in the main
branch and extract it.

### 2. Generate Google Ads API Credentials

The next step ("Configuration") will require several Google Ads API credentials.
These can be generated by clicking on the "Instructions" links below.

*   Developer Token:
    [Instructions](https://developers.google.com/google-ads/api/docs/first-call/dev-token)
*   Client ID / Secret:
    [Instructions](https://developers.google.com/google-ads/api/docs/first-call/oauth-cloud-project)
*   Refresh Token:
    [Download Python script](https://github.com/googleads/googleads-python-lib/blob/master/examples/adwords/authentication/generate_refresh_token.py)

To get the refresh token, after downloading the Python script linked above, run
it as follows:

```
python generate_refresh_token.py --client_id INSERT_CLIENT_ID --client_secret INSERT_CLIENT_SECRET
```

When prompted to login to a Google account, select the account that has
permission to modify your Google Ads data.

### 3. Configuration

-   In GCP Cloud Shell or your local terminal, navigate to the root directory of
    the SAKA repository and edit the `environment_variables.sh` file. Supply
    values for the variables, noting the ones that are optional. Explanations of
    each environment variable are shown next to the respective variable.

### 4. Installation

-   In GCP Cloud Shell or your local terminal, run the install script in the
    repository's root directory using the following command: `bash
    install_to_gcp.sh`.
-   If you see any errors that a resource already exists, it is likely due to
    the script having been run more than once. In this case these errors can be
    safely ignored.
-   After the script completes, in order to deploy the SAKA solution to your GCP
    project, it is required to perform a git push to the Cloud Source Repository
    that was created by the install_to_gcp.sh script in the previous step.
    (reference:
    [Cloud Source Repositories](https://cloud.google.com/source-repositories/docs/pushing-code-from-a-repository)).
-   Set up authentication to the Cloud Source Repository by following the
    instructions on
    [this page](https://cloud.google.com/source-repositories/docs/authentication).
-   Run the following git commands in the same local repository you cloned and
    ran the initialization script in:

    1.  ```
        git remote add gcp ssh://[EMAIL]@source.developers.google.com:2022/p/[PROJECT_ID]/r/[REPO_NAME]
        ```
        (where `PROJECT_ID` is your GCP project ID and `REPO_NAME` is the
        repository name you set for `SOURCE_REPO` in `environment_variables.sh`)
    2.  ```
        git add --all -- ':!environment_variables.sh'
        ```
    3.  ```
        git commit -m "[Your commit message]"
        ```
    4.  ```
        git push --all gcp
        ```
        If you see a prompt for choosing a configuration,
        choose option i.

-   Cloud Build will auto-trigger on the git push and deploy the code to GCP. It
    should take around 5 minutes. You can check the status in your GCP
    Console's [Cloud Build dashboard or history
    tab](https://cloud.google.com/cloud-build/docs/view-build-results#viewing_build_results).

-   Ensure that the Cloud Build logs show no errors.

## Confirming Installation

To confirm that the components were installed to your GCP environment, navigate
to and check each of the following components in your GCP project from its admin
console:

-   Cloud Functions
    -   Check that a Cloud Function called "extract_and_upload_keywords" exists
        and has a green check mark to the left of it.
-   Cloud Scheduler
    -   Check that a Cloud Scheduler job called "triggerSakaFunction" exists and
        has a green check mark to the left of it.
-   Pub/Sub
    -   Navigate to Topics and check that there is a topic called
        "trigger-extract-and-upload-keywords-cloud-function" showing in the UI.
-   Security
    -   Navigate to Secret Manager and verify that there are two secrets created
        with the names: "google_ads_api_credentials" and "sa360_sftp_password".

## Search Term to Keyword Logic

The logic that determines if and how a search term should be added as a keyword
is determined in the `search_term_transformer.py > _get_match_type` method.

By default, the logic is as follows:

*   Only add search terms where:

    *   Conversions > conversions threshold (default=0, update via
        `CONVERSIONS_THRESHOLD` environment variable) 
        OR
    *   CTR > Ad Group CTR AND clicks > clicks threshold (default=5, update via
        `CLICKS_THRESHOLD` environment variable)

*   If the number of tokens in the threshold > tokens threshold (default=3,
    update via `SEARCH_TERM_TOKENS_THRESHOLD` environment variable), add the
    search term as a `BROAD` keyword

*   Otherwise, add the search term as an `EXACT` and `PHRASE` keyword.

## Confirming Run Operation

After installation, SAKA is scheduled to run by default once daily. This can be
confirmed by navigating to GCP's Cloud Scheduler and checking the
`triggerSakaFunction` job's "Last run result" column (It should show "Success"),
or clicking on the job's "View" button in the "Logs" column.

If there were any issues, detailed logs can be viewed from the Cloud Function's
Logs tab for troubleshooting.

## FAQ

### "CRITERION already exists" Errors in SA 360

If you see the error:

```
Mutation failed because a matching CRITERION already exists for AD_GROUP
```

It likely means the search term already exists as a keyword for the specified ad
group, so this error can safely be ignored.

### Narrowing Down to Specific Campaigns

By default, SAKA will extract search terms for **all** campaigns for the
specified customer ID. If you want to only extract search terms for certain
campaigns, update the `CAMPAIGN_IDS` environment variable (either by editing
`environment_variables.sh` and re-running the installer, or directly in the
Cloud Function's settings) to a comma-separated list of the IDs for the
campaigns you want to query.

For example, `CAMPAIGN_IDS` can be formatted as follows:

```
123,456,789
```

### Updating "Search Term to Keyword" Logic

There are two ways to update the logic that determines if and how a search term
should be added as a keyword.

#### Updating the Environment Variables

The `CLICKS_THRESHOLD`, `CONVERSIONS_THRESHOLD`, and
`SEARCH_TERM_TOKENS_THRESHOLD` environment variables can be used to tweak the
thresholds used in the current filtering logic.

#### Customizing the Code

If you want to create totally different logic, update `_get_match_type()` in
`search_term_transformer.py`. This method is responsible for determining if and
how a search term should be added as a keyword.
