import requests, bs4, csv, os
from pprint import pprint

INFOCASAS_URL = 'https://www.infocasas.com.bo/venta/inmuebles/santa-cruz/pagina1?&ordenListado=3'

def write_to_csv(propertyData):
  filename = 'infocasas.csv'
  append_write = None

  if os.path.exists(filename):
    append_write = 'a'
  else:
    append_write = 'w'
  
  csv_file = open(filename, append_write, newline='', encoding='utf-8')
  csv_writer = csv.writer(csv_file)
  
  csv_writer.writerow(propertyData)
  
  csv_file.close()

def get_infocasas_properties():
  hasMorePages = True
  page = 1
  while hasMorePages == True:
    # try:
      res = requests.get(f'https://www.infocasas.com.bo/venta/inmuebles/santa-cruz/pagina{page}?&ordenListado=3')
      res.raise_for_status()

      infocasas_soup = bs4.BeautifulSoup(res.text, 'lxml')
      properties = infocasas_soup.select('.propiedades-slider')

      if len(properties) > 0:
        for property in properties:
          property_link = property.find('a', {'class': 'holder-link'})['href']
          property_price = property.find('div', {'class': 'precio'}).get_text(strip=True)
          property_address = property.find('div', {'class': 'inDescription'}).select('h3')[0].get_text(strip=True)
          property_description = property.find('div', {'class': 'inDescription'}).select('p')[0].get_text(strip=True)
          property_quick_info = property.find('div', {'class': 'contentIcons'}).get_text(strip=True)

          propertyDataList = [property_price, property_link, property_quick_info, property_address, property_description]
          
          write_to_csv(propertyDataList)

        print(f'{len(properties)} properties scraped in page {page}')

        page += 1

      else:
        hasMorePages = False
    
get_infocasas_properties()
print('Infocasas successfully scraped')
