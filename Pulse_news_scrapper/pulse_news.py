import requests
import schedule
from flask import Flask
import subprocess
import gspread
from datetime import date
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
import time
key = '195zvdsCxHeStpGnb3zlSaPEDaRBLh9phhJ0jTNfROT0'
app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome to my automated projects"

@app.route('/news_scraping_automated')
def news_scraping_automated():
    # Make a request to the webpage
    url = 'https://pulse.zerodha.com/'
    webpage = requests.get(url).text

    # Parse the HTML content of the webpage using Beautiful Soup
    soup = BeautifulSoup(webpage, 'html.parser')
    headline_all = []
    description_all = []
    date_time_all = []
    
    # Find all the list items with class "box item"
    list_items = soup.find_all('li', class_='box item')
    list_sides = soup.find_all('ul', class_='similar')
    
    # Extract the data from each list item
    for item in list_items:
        # Extract the headline
        headline = item.find('h2', class_='title').text.strip()
        headline_all.append(headline)
        
        # Extract the description
        description = item.find('div', class_='desc').text.strip()
        description_all.append(description)
        
        # Extract the date and time
        date_time = item.find('span', class_='date')['title']
        date_time_all.append(date_time)
    
    for item in list_sides:
        # Extract the headline
        headline = item.find('a', class_='title2').text.strip()
        headline_all.append(headline)
        
        # Extract the description
        description_all.append(headline)
        
        # Extract the date and time
        date_time = item.find('span', class_='date')['title']
        date_time_all.append(date_time)
    
    df = pd.DataFrame()
    df['headline'] = headline_all
    df['description'] = description_all
    df['date_time'] = date_time_all
    
    gc = gspread.service_account(filename='D:\\Automated projects\\news-data-api-d22f2d663df8.json')
    sheet = gc.open_by_key(key)
    current_date = date.today()
    worksheet = sheet.add_worksheet(title=str(current_date), rows="1000", cols="3")
    
    # Get the number of rows and columns in the DataFrame
    num_rows, num_cols = df.shape
    
    # Get the range where the data will be written
    cell_range = f'A1:{chr(ord("A") + num_cols - 1)}{num_rows}'
    
    # Convert DataFrame to a list of lists
    data = df.values.tolist()
    
    # Update the worksheet with the data
    worksheet.update(cell_range, data)
    return f"Scraping completed successfully of {current_date}"

# Schedule the script to run every 24 hours at 12:01 AM
schedule.every(24).hours.at("00:01").do(news_scraping_automated)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
