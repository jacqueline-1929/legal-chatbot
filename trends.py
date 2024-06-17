import time
from pytrends.request import TrendReq

# Create a TrendReq object
pytrends = TrendReq(hl='en-US', tz=360)

# Specify the keywords
keywords = ['Python', 'Java', 'C++', 'JavaScript', 'Ruby']

# Build the payload
pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='', gprop='')

# Retrieve the interest over time data
interest_over_time_df = None
while interest_over_time_df is None:
    try:
        interest_over_time_df = pytrends.interest_over_time()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Waiting for 60 seconds before retrying...")
        time.sleep(60)

# Print the interest over time data
print("Interest over time:")
print(interest_over_time_df)