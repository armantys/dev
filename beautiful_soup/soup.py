from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    city = request.form['city']
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    
    url = f'https://www.booking.com/searchresults.fr.html?ss={city}&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0'
    headers = { 
        'User-Agent' : 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, comme Gecko) Chrome/51.0.2704.64 Safari/537.36', 
        'Accept-Language' : 'en-US, en;q=0.5'
    } 

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    hotels = soup.findAll('div', {'data-testid': 'property-card'})

    hotels_data = []
    for hotel in hotels:
        name_element = hotel.find('div', {'data-testid': 'title'})
        name = name_element.text.strip() if name_element else 'N/A'

        location_element = hotel.find('span', {'data-testid': 'address'})
        location = location_element.text.strip() if location_element else 'N/A'

        price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
        price = price_element.text.strip() if price_element else 'N/A'

        rating_element = None
        for possible_class in ['a3b8729ab1 d86cee9b25']:
            rating_el = hotel.find('div', {'class': possible_class})
            if rating_el:
                rating_text = rating_el.text.strip()
                rating_match = re.search(r"\d+(\.\d+)?", rating_text)
                rating_element = rating_match.group(0) if rating_match else 'N/A'
                break

        hotels_data.append({
            'name': name,
            'location': location,
            'price': price,
            'rating': rating_element
        })

    return render_template('index.html', hotels=hotels_data)

if __name__ == '__main__':
    app.run(debug=True)