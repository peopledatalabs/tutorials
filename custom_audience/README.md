# Custom Audience Generation
The script [custom_audience_generator.py](./custom_audience_generator.py) corresponds to our [How to Build a Custom Audience with PDL Tutorial](https://blog.peopledatalabs.com/post/audience-generation-tutorial).

## Getting Started
1. Download the contents of this folder.
2. Install [Python 3.6+](https://www.python.org/downloads/), [requests](https://requests.readthedocs.io/en/latest/), and [pandas](https://pandas.pydata.org).
3. Get a [Free PDL License & API Key](https://docs.peopledatalabs.com/docs/quickstart#creating-an-account).
4. Set your API key on line 12 of [custom_audience_generator.py](./custom_audience_generator.py).
    ```python
    'x-api-key': '**** YOUR API KEY HERE ****'
    ```
5. Go to the `custom_audience/` folder.
    ```bash
    $ cd ~/custom_audience
    ```
6. Run the script. (NOTE: The script uses 25 [Company Enrichment](https://docs.peopledatalabs.com/docs/company-enrichment-api) and 50 [Person Search](https://docs.peopledatalabs.com/docs/person-search-api) PDL credits!)
    ```bash
    $ python custom_audience_generator.py
    ```

## Tips
For a detailed explanation of this script, please read the [tutorial](https://blog.peopledatalabs.com/post/audience-generation-tutorial).

### Getting Different Results
The tutorial was written using [v19.0](https://docs.peopledatalabs.com/changelog/july-2022-release-notes-v19) of the PDL API.

In future builds, the companies or people matched may be different than the examples in the [tutorial](https://blog.peopledatalabs.com/post/audience-generation-tutorial).

### Minimizing Credit Usage
The script uses 25 [Company Enrichment](https://docs.peopledatalabs.com/docs/company-enrichment-api) and 50 [Person Search](https://docs.peopledatalabs.com/docs/person-search-api) PDL credits.

Each time you run the script, it will use PDL credits. If you save the results of an API call and load them later (instead of making another request to PDL), it will not use credits.

To save the API results, you can export the pandas DataFrame to a CSV and load it in subsequent runs by commenting out the functions like this:

```python
# first run, make the API call (costs PDL credits)
# ----
audience_df = get_decision_makers(companies)
audience_df.to_csv(csv_location / 'custom_audience.csv')
# audience_df = pd.read_csv(
#     csv_location / 'custom_audience.csv', header=0, index_col=0)
```

```python
# future runs, do not make API call (no credits)
# ----
# audience_df = get_decision_makers(companies)
# audience_df.to_csv(csv_location / 'custom_audience.csv')
audience_df = pd.read_csv(
    csv_location / 'custom_audience.csv', header=0, index_col=0)
```
