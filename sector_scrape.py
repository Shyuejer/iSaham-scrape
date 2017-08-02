import csv
import requests
from bs4 import BeautifulSoup

url = 'http://www.isaham.my/all-sectors'
url_2 = 'http://www.isaham.my/sector'

# want to better show that I'm accessing the SUBSECTION.
print "accesing " + url + "..."
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, "html.parser")

# Because there are some annoying numbers within the cell, I'll have to get rid of them. Potentially have to just take [:-1] to remove the ending white space.


list_sectors = []
for cell in soup.findAll("a", class_="list-group-item"):
    # .text is needed or we'll have the stupid tag.
    span_tag = cell.span.extract()
    cell = cell.text
    cell = cell.replace(u'\xa0', u' ')
    list_sectors.append(cell)


# Checking if website links work
def request_count():
    # These are my requests counters. 
    good_counter = 0
    bad_counter = 0  
    for sector in list_sectors:
        sector = sector[:-1].lower()
        sector = sector.split(" ")
        sector = "-".join(sector)
        sector = sector.replace('&','and')
        request = requests.head(url_2 + '/' + sector)
        if request.status_code == 200:
            print('Website exists for %s' %sector)
            good_counter += 1
        else:
            print('Website does not exist for %s' %sector)
            bad_counter += 1


    print "Number of good counters: %i" %good_counter
    print "Number of bad counters: %i" %bad_counter        

# The exciting part: fetching data from 50 pages!
# First I will make a list of websites to visit
list_of_sites = []

for sector in list_sectors:
    sector = sector[:-1].lower()
    sector = sector.split(" ")
    sector = "-".join(sector)
    sector = sector.replace('&','and')
    list_of_sites.append(url_2+'/'+sector)

def fetch():
    for url in list_of_sites:
        print "accesing " + url
        response = requests.get(url)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            data_rows = []    
            header_cells = []
            for cell in soup.findAll('th'):
                # .text is needed or we'll have the stupid tag.
                header_cells.append(cell.text)
            
            for row in soup.findAll('tr')[1:]:
                data_cells = []
                for cell in row.findAll('td'):
                    text = cell.text.replace('&nbsp;', '')
                    data_cells.append(text)
                data_rows.append(data_cells)
            
            outfile = open("C:\\Users\\sj\\Dropbox\\Investing\\isaham.data\\%s.csv" % url[27:], "wb")
            writer = csv.writer(outfile)
            writer.writerow(header_cells)
            writer.writerows(data_rows)