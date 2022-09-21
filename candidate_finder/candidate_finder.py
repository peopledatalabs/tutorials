import csv

# See https://github.com/peopledatalabs/peopledatalabs-python
from peopledatalabs import PDLPY

# Create a client, specifying your API key
client = PDLPY(
    api_key='YOUR API KEY HERE'
)

# number of profiles to save (max 100)
NUM_PROFILES = 50

# Elasticsearch query for candidates matching the job description
ES_QUERY = {
    'query': {
        'bool': {
            'must': [
                {
                    'exists': {
                        'field': 'full_name'
                    }
                },
                {
                    'exists': {
                        'field': 'emails'
                    }
                },
                {
                    'exists': {
                        'field': 'linkedin_url'
                    }
                },
                {
                    'term': {
                        'location_country': 'united states'
                    }
                },
                {
                    'terms': {
                        'education.degrees': [
                            'bachelors',
                            'masters'
                        ]
                    }
                },
                {
                    'term': {
                        'education.majors': 'computer science'
                    }
                },
                {
                    'terms': {
                        'skills': [
                            'html',
                            'css',
                            'javascript',
                            'react'
                        ]
                    }
                },
                {
                    'terms': {
                        'skills': [
                            'python',
                            'django'
                        ]
                    }
                },
                {
                    'terms': {
                        'skills': [
                            'amazon web services',
                            'aws',
                            'cloud computing'
                        ]
                    }
                },
                {
                    'range': {
                        'inferred_years_experience': {
                            'gte': 5,
                            'lte': 10
                        }
                    }
                }
            ],
            'must_not': [
                {
                    'terms': {
                        'job_title_levels': [
                            'cxo',
                            'vp',
                            'director',
                            'owner',
                            'partner',
                            'manager'
                        ]
                    }
                },
                {
                    'term': {
                        'education.degrees': 'doctorates'
                    }
                }
            ]
        }
    }
}

# Person Search API parameters
# https://docs.peopledatalabs.com/docs/input-parameters-person-search-api
PARAMS = {
  'dataset': 'resume',
  'query': ES_QUERY,
  'size': NUM_PROFILES
}


def save_to_csv(profiles: [dict], filename: str, fields: [str], delim=','):
    '''
    Writes profiles to CSV, maps specified fields to columns

    Parameters
    ----------
    profiles : [dict]
      All profiles to save (Person Search API response['data'])
    filename : name
      Name of the CSV file to create
    fields : [str]
      All field names in profiles to save as columns in CSV
    delim: str
      Delimiter to use when creating CSV (default: ',')

    Returns
    -------
    None
    '''
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=delim)
        # Write header row
        writer.writerow(fields)

        # Write each profile to a row, only include each listed field's value
        count = 0
        for profile in profiles:
            writer.writerow([profile[field] for field in fields])
            count += 1

    print(f'Wrote {count} lines to: "{filename}"')


if __name__ == '__main__':
    # Pass the parameters object to the Person Search API
    response = client.person.search(**PARAMS).json()
    all_profiles = response['data']

    print(f'{response["total"]} total candidates match our criteria')
    print(f'Exporting the Top {NUM_PROFILES} to CSV...')

    # Use utility function to save all records retrieved to CSV
    csv_header_fields = [
        'job_title',
        'full_name',
        'id',
        'work_email',
        'linkedin_url'
    ]
    csv_filename = 'candidate_profiles.csv'
    save_to_csv(all_profiles, csv_filename, csv_header_fields)
