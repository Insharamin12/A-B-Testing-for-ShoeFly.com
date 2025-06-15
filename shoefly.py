import pandas as pd

# Load data
ad_clicks = pd.read_csv('ad_clicks.csv')
print(ad_clicks.head())

# Count users by utm_source
utm_counts = ad_clicks.groupby('utm_source')\
    .user_id.count()\
    .reset_index()
print(utm_counts)

# Add a new column to indicate if ad was clicked
ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()

# Group by utm_source and is_click
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click'])\
    .user_id.count()\
    .reset_index()
print(clicks_by_source)

# Pivot to compare clicks vs non-clicks by source
clicks_pivot = clicks_by_source.pivot(
    index='utm_source',
    columns='is_click',
    values='user_id'
).reset_index()

# Calculate percent clicked
clicks_pivot['percent_clicked'] = clicks_pivot[True] / (
    clicks_pivot[True] + clicks_pivot[False]
)
print(clicks_pivot)

# Count users by experimental group
print(ad_clicks.groupby('experimental_group')\
    .user_id.count()\
    .reset_index())

# Clicks by experimental group
exp_group_clicks = ad_clicks.groupby(['experimental_group', 'is_click'])\
    .user_id.count()\
    .reset_index()\
    .pivot(
        index='experimental_group',
        columns='is_click',
        values='user_id'
    ).reset_index()
print(exp_group_clicks)

# Split into A and B groups
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

# Pivot A group by day
a_clicks_pivot = a_clicks.groupby(['is_click', 'day'])\
    .user_id.count()\
    .reset_index()\
    .pivot(
        index='day',
        columns='is_click',
        values='user_id'
    ).reset_index()
a_clicks_pivot['percent_clicked'] = a_clicks_pivot[True] / (
    a_clicks_pivot[True] + a_clicks_pivot[False]
)
print(a_clicks_pivot)

# Pivot B group by day
b_clicks_pivot = b_clicks.groupby(['is_click', 'day'])\
    .user_id.count()\
    .reset_index()\
    .pivot(
        index='day',
        columns='is_click',
        values='user_id'
    ).reset_index()
b_clicks_pivot['percent_clicked'] = b_clicks_pivot[True] / (
    b_clicks_pivot[True] + b_clicks_pivot[False]
)
print(b_clicks_pivot)
