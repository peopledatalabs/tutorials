# Custom Audience Generation
The script [candidate_finder.py](./candidate_finder.py) corresponds to our [How to Find Candidates using a Job Description tutorial](>> LINK TBD <<).

## Getting Started
1. Download the contents of this folder.
2. Install [Python 3.6+](https://www.python.org/downloads/) and [PDL's Python SDK](https://pypi.org/project/peopledatalabs/).
3. Get a [Free PDL License & API Key](https://docs.peopledatalabs.com/docs/quickstart#creating-an-account).
4. Set your API key on line 8 of [candidate_finder.py](./candidate_finder.py#L8).
    ```python
        api_key='YOUR API KEY HERE'
    ```
5. Go to the `candidate_finder/` folder.
    ```bash
    $ cd ~/candidate_finder
    ```
6. Run the script. (NOTE: The script uses 50 [Person Search](https://docs.peopledatalabs.com/docs/person-search-api) PDL credits!)
    ```bash
    $ python candidate_finder.py
    ```
7. Candidate profiles will be saved in the created `candidate_profiles.csv` file in the same folder as the script.


## Tips
For a detailed explanation of this script, please watch the [tutorial](>> LINK TBD <<).

### Getting Different Results
The tutorial was written using [v19.0](https://docs.peopledatalabs.com/changelog/july-2022-release-notes-v19) of the PDL API, and [v1.1.0](https://pypi.org/project/peopledatalabs/1.1.0/) of PDL's Python SDK.

In future builds, the people matched may be different than the examples in the [tutorial](>> LINK TBD <<).
