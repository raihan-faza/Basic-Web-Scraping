# web to scrape:https://www.scrapethissite.com/
from bs4 import BeautifulSoup as bs
import urllib3 as ul
import polars as pl

url = 'https://www.scrapethissite.com/pages/simple/'
http = ul.PoolManager()
resp = http.request('GET', url)
data = {
    'CountryName': [],
    'Capital': [],
    'Population': [],
    'Area': [],
}
soup = bs(resp.data.decode('utf-8'), 'html.parser')
countryList = soup.find_all('div', class_='col-md-4 country')

# preparing dataframe input
for country in countryList:
    country.find('i').decompose()
    data['CountryName'].append(country.find('h3',class_='country-name').text.strip())
    data['Capital'].append(country.find('span',class_='country-capital').text.strip())
    data['Population'].append(country.find('span',class_='country-population').text.strip())
    data['Area'].append(country.find('span',class_='country-area').text.strip())

# move content to csv file
df = pl.DataFrame(data)
df.write_csv('test.csv',separator=',')

#check the csv file
test = pl.read_csv('test.csv')
print(test.head())