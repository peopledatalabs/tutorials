from pathlib import Path

import pandas as pd
import requests


# replace 'x-api-key' value with your PDL API Key
# get your key here: https://dashboard.peopledatalabs.com/main/api-keys
headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'x-api-key': '**** YOUR API KEY HERE ****'
}


def enrich_company(name: str, website: str, linkedin: str) -> dict:
    '''
    Call the PDL Company Enrichment API for the given company.

    Company Enrichment API Documentation:
        https://docs.peopledatalabs.com/docs/company-enrichment-api

    Parameters
    ----------
    name : str
      Company name (ex: 'google')
    website : str
      Company website (ex: 'google.com')
    linkedin : str
      Company LinkedIn page URL (ex: 'linkedin.com/company/google')

    Returns
    -------
    Enrichment API JSON response as dict

    Raises
    -------
    ValueError : Raised if response does not have 200 Success status code
    '''
    resp = requests.get(
        'https://api.peopledatalabs.com/v5/company/enrich',
        headers=headers,
        params={
            'name':    name,
            'website': website,
            'profile': linkedin
        }
    )
    if resp.status_code != 200:
        raise ValueError(f'Request to {resp.request.url} failed. '
                         f'Response: {resp.status_code} - {resp.text}')

    return resp.json()


def filter_for_tag(to_filter: pd.DataFrame, tags: [str]) -> pd.DataFrame:
    '''
    Filter DataFrame to only the rows that contain a tag in the list

    Parameters
    ----------
    to_filter : DataFrame
      The DataFrame to filter
    tags : list of strings
      Keep any row that has at least one tag in this list

    Returns
    -------
    Filtered DataFrame
    '''
    # create a mask (True/False) for if each row has any of the tags
    mask = to_filter['tags'].dropna().apply(
        lambda row: any([tag in row for tag in tags]))

    # apply mask to filter DataFrame
    return to_filter[mask]


def get_decision_makers(company_linkedins: [str]) -> pd.DataFrame:
    '''
    Get 50 upper level employees at each company in list using
    the PDL Person Search API

    Person Search API Documentation:
        https://docs.peopledatalabs.com/docs/person-search-api

    Parameters
    ----------
    company_linkedins : list of strings
      List of all company LinkedIn profile URLs to search

    Returns
    -------
    DataFrame of Search API responses containing 50 people that
    work at any company in the list, have upper level job titles,
    and have a known work email.
    '''
    # create the Elasticsearch query
    search_query = {
        'query': {
            'bool': {
                'must': [
                    # work for one of our targeted companies
                    {'terms': {'job_company_linkedin_url': company_linkedins}},
                    # be a decision maker
                    {'terms': {'job_title_levels': [
                        'owner', 'director', 'cxo', 'vp', 'partner']}},
                    # have a known work email
                    {'exists': {'field': 'work_email'}}
                ]
            }
        }
    }
    # get 50 matches
    resp = requests.post(
        'https://api.peopledatalabs.com/v5/person/search',
        headers=headers,
        json={
            'query':    search_query,
            'size':     50,  # number between 1-100
            'dataset': 'resume'
        }
    )

    if resp.status_code != 200:
        raise ValueError(f'Request to {resp.request.url} failed. '
                         f'Response: {resp.status_code} - {resp.text}')

    return pd.DataFrame(resp.json()['data'])


def create_csv_for_twitter(data: pd.DataFrame, filename: str) -> None:
    '''
    Format DataFrame as CSV according to Twitter Custom Audience specs:
        https://business.twitter.com/en/help/campaign-setup/campaign-targeting/custom-audiences/lists.html

    Parameters
    ----------
    data : DataFrame
      DataFrame to export as CSV
    filename : str
      Path to save the CSV to. Should end in '.csv'

    Returns
    -------
    None
    '''
    data['work_email'].to_csv(filename, header=None, index=False)


def create_csv_for_facebook(data: pd.DataFrame, filename: str) -> None:
    '''
    Format DataFrame as CSV according to Facebook Custom Audience specs:
        https://www.facebook.com/business/help/2082575038703844?id=2469097953376494

    Parameters
    ----------
    data : DataFrame
      DataFrame to export as CSV
    filename : str
      Path to save the CSV to. Should end in '.csv'

    Returns
    -------
    None
    '''
    headers = ['email', 'phone', 'fn', 'ln']
    fields = ['work_email', 'mobile_phone', 'first_name', 'last_name']
    data[fields].to_csv(filename, header=headers, index=False)


if __name__ == '__main__':
    # folder where the starting list is saved & where final CSVs will save to
    csv_location = Path.cwd()
    initial_list = csv_location / 'starting_list.csv'

    # Load company dataset into pandas DataFrame
    initial_df = pd.read_csv(initial_list, header=0)
    print(f'Starting Data Size: {initial_df.shape}')
    print(f'Starting Data Columns: {initial_df.columns.tolist()}')

    # enrich each company using PDL's Company Enrichment API
    print('Enriching companies...')
    enriched_df = initial_df.apply(
        lambda row: enrich_company(
            row['name'],
            row['website'],
            row['linkedin_url']
        ),
        result_type='expand',
        axis=1
    )
    print(enriched_df.head())
    print(f'Enriched Data Size: {enriched_df.shape}')
    print(f'Enriched Data Columns: {enriched_df.columns.tolist()}')

    # if you want to save the intermediate results so that
    # you don't have to spend PDL credits every time, you
    # can export each DataFrame as a CSV and load it the
    # next time you run the script instead of making the request
    #
    # enriched_df.to_csv(csv_location / 'enriched_companies.csv')
    # enriched_df = pd.read_csv(
    #     csv_location / 'enriched_companies.csv', header=0, index_col=0)

    # find all companies with the tag 'saas'
    print('Filtering for tag = "saas"...')
    saas_df = filter_for_tag(enriched_df, ['saas'])
    print(saas_df.head())
    print(f'Found {len(saas_df.index)} companies with "saas" tag')

    print('Searching for decision makers...')
    companies = saas_df['linkedin_url'].values.tolist()
    audience_df = get_decision_makers(companies)
    print(audience_df.head())
    print(f'Found {len(audience_df.index)} people for Custom Audience')

    # audience_df.to_csv(csv_location / 'custom_audience.csv')
    # audience_df = pd.read_csv(
    #     csv_location / 'custom_audience.csv', header=0, index_col=0)

    print('Exporting for twitter...')
    create_csv_for_twitter(audience_df, str(
        (csv_location / 'twitter.csv').resolve()))
    # preview the created CSV
    twitter = pd.read_csv(csv_location / 'twitter.csv', header=None)
    print(twitter.head())

    print('Exporting for Facebook...')
    create_csv_for_facebook(audience_df, str(
        (csv_location / 'facebook.csv').resolve()))
    # preview the created CSV
    facebook = pd.read_csv(csv_location / 'facebook.csv', header=0)
    print(facebook.head())
