import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='LTE Stats dashboard',
    page_icon=':abacus:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab LTE Download data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

gdp_df = get_gdp_data()

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


lte_countries_df = get_lte_countries()
# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :abacus: GDP dashboard

Browse download data from the LTE data. 

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

countries = lte_countries_df['country'].unique()

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

st.header('LTE Download Data over time', divider='gray')

''

st.line_chart(
    filtered_lte_df,
    x='year',
    y='dls',
    color='country',
    use_container_width=True
)


first_year = lte_countries_df[lte_countries_df['year'] == from_year]
last_year = lte_countries_df[lte_countries_df['year'] == to_year]

st.header(f'LTE Downloads in {to_year}', divider='gray')

''

'''
Attempting to add more metrics 
'''


cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_dl = first_year[first_year['country'] == country]['dls'].iat[0]
        last_dl = last_year[last_year['country'] == country]['dls'].iat[0]

        if math.isnan(first_dl):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_dl / first_dl:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} LTE Downloads',
            value=f'{last_dl:,.0f}',
            delta=growth,
            delta_color=delta_color
        )
 