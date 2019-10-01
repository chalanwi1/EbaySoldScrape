from bs4 import BeautifulSoup
import lxml
import pandas as pd
import requests
import time

# Create Dictionary for scraped data
data = {
  'Title': [],
  'Sold Date': [],
  'Sold Price': [],
}

# Sets how many pages to scrape
pages = range(1)

# Loop through each page
for i in pages:

    # base url
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=gym+equipment&_sacat=0&LH_TitleDesc=0&_oac=1&_' \
          'ipg=200&rt=nc&LH_Complete=1&rt=nc&rt=nc&_pgn={}'.format(i)

    # Send get request for http
    page = requests.get(url)

    # if response is good(200), render page
    if page.status_code == requests.codes.ok:
        bs = BeautifulSoup(page.text, 'lxml')

        # Create list of all items in container
        gym_list = bs.find_all(class_='s-item')[1:]

        # Loop through each item in container and store our defined data
        for gym_item in gym_list:

            title = gym_item.find(class_='s-item__title--tag').next_element.next_element.text
            if title:
                data['Title'].append(title)
            else:
                data['Title'].append('NA')

            sold_date = gym_item.find(class_='s-item__title--tag').text
            if sold_date:
                data['Sold Date'].append(sold_date)
            else:
                data['Sold Date'].append('NA')

            sold_price = gym_item.find(class_='s-item__price').text
            if sold_price:
                data['Sold Price'].append(sold_price)
            else:
                data['Sold Price'].append('NA')

            # Sleep .1 secs for each data set scraped
            time.sleep(.1)

# Convert data dictionary to pandas data frame
final = pd.DataFrame(data, columns=['Title', 'Sold Date', 'Sold Price'])

# Starts our list number at 1 instead of 0
final.index += 1

# Write result to csv file
final.to_csv('gym_file.csv', index=False, sep=',', encoding='utf-8')

print(final)
