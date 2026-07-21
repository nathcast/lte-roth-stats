import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Rothamsted Long-term Experiments Datasets Downloads Stats dashboard',
    page_icon='rres-logo.jpg', 
    layout="wide"
)


col1, col2 = st.columns([6, 1])

with col1:
    st.title("Rothamsted Long-term Experiments Datasets Downloads")
    st.caption("Engagement metrics tool")

with col2:
    st.image("rres-logo.jpg", width=200)
# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data


def get_lte_countries():
    """Grab LTE Download data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/lte_countries.csv'
    raw_lte_countries_df = pd.read_csv(DATA_FILENAME)

    # Convert years from string to integers
    raw_lte_countries_df['year'] = pd.to_numeric(raw_lte_countries_df['year'])

    return raw_lte_countries_df




def get_lte_sectors():
    """Grab LTE Download data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/lte_sectors.csv'
    raw_lte_sectors_df = pd.read_csv(DATA_FILENAME)

    # Convert years from string to integers
    raw_lte_sectors_df['year'] = pd.to_numeric(raw_lte_sectors_df['year'])

    return raw_lte_sectors_df

def get_lte_dois():
    """_summary_ Grad the LTS download data per DOI
    """
    DATA_FILENAME = Path(__file__).parent/'data/lte_dois.csv'
    raw_lte_dois_df = pd.read_csv(DATA_FILENAME)
    raw_lte_dois_df['year'] = pd.to_numeric(raw_lte_dois_df['year'])

    return raw_lte_dois_df
    

## get my dataframes

lte_sectors_df = get_lte_sectors()
lte_countries_df = get_lte_countries()
lte_dois_df = get_lte_dois()
# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''

Browse information on the downloads of datasets from the eRA web site. 
This information is dependant on the willingness of the user to fill it in. 


## By Countries
'''

# Add some spacing
''
''

min_value = lte_countries_df['year'].min()
max_value = lte_countries_df['year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

""" countries = lte_countries_df['country'].unique() """
countries = (
    lte_countries_df.loc[
        lte_countries_df['country'].notna()
        & lte_countries_df['country'].str.len().eq(2),
        'country'
    ]
    .unique()
)

dois = (
    lte_dois_df.loc[
        lte_dois_df['DOI'].notna(),
        'DOI'
    ]
    .unique()
)
first_year = lte_countries_df[lte_countries_df['year'] == from_year]
last_year = lte_countries_df[lte_countries_df['year'] == to_year]

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['GB', 'FR', 'US', 'TR', 'CN', 'IN', 'AU'])

''
''
''

# Filter the data
filtered_lte_df = lte_countries_df[
    (lte_countries_df['country'].isin(selected_countries))
    & (lte_countries_df['year'] <= to_year)
    & (from_year <= lte_countries_df['year'])
]

# Filter the data
filtered_lte_sector_df = lte_sectors_df[
    (lte_countries_df['year'] <= to_year)
    & (from_year <= lte_countries_df['year'])
]



st.header('LTE Download Data over time', divider='gray')

''

st.line_chart(
    filtered_lte_df,
    x='year',
    y='dls',
    color='country',
    use_container_width=True
)


''

st.bar_chart(
    filtered_lte_df,
    x='year',
    y='dls',
    color='country',
    use_container_width=True
)

'''
## By sector

Please note 
- capture of sector started in 2025
- data is voluntary.  
'''

st.bar_chart(
    filtered_lte_sector_df,
    x='year',
    y='dls',
    color='sector',
    use_container_width=True
)


'''
## By DOIs
'''
if not len(dois):
    st.warning("Select at least one DOI")

selected_dois = st.multiselect(
    'Which DOI would you like to view?',
    dois,
    ['10.23637/KeyRefOABKyields', '10.23637/rbk1-yld6822-01', '10.23637/rbk1-bksoils-01', 
     '10.23637/rbk1-1796346264-1', '10.23637/rbk1-BKNUTRW-01']) 
# Filter the data
filtered_lte_doi_df = lte_dois_df[
    (lte_dois_df['DOI'].isin(selected_dois))
    &
    (lte_dois_df['year'] <= to_year)
    & (from_year <= lte_dois_df['year'])
]

st.bar_chart(
    filtered_lte_doi_df,
    x='year',
    y='dls',
    color='DOI',
    use_container_width=True
)



