# Radaris.com Reverse API
# This project is for interacting with Radaris.com, enabling person searches
# and retrieving detailed profile information.
# https://github.com/pb0xxx

import json
import requests
from flask import Flask, jsonify, request, render_template
from bs4 import BeautifulSoup

from classes.ApiResponse import ApiResponse
from classes.Result import Result

app = Flask(__name__)

def search(name):
    """
    Function to search for people based on a name.

    Parameters:
    - name: name of the person to search for

    Returns:
    - ApiResponse: API response with search results or error message
    """
    results = []  # List to store search results
    
    url = f"https://radaris.com/ng/search?fl={name}"  # Creating the search URL

    # If the search parameter is empty
    if not name:
        return ApiResponse("not_empty", 20)
    
    response = requests.get(url, timeout=60)
    
    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Find all search result elements
        elements = soup.find_all("span", class_="col-sm-8")
        
        # Iterate through all found results
        for html_element in elements:
            hyperlink = html_element.find("a")
            if hyperlink:
                name = hyperlink.text
                href = hyperlink.get("href")
                results.append(Result(name, href))
        
        return ApiResponse(results, 0)  # Return the search results
    elif response.status_code == 301:
        return ApiResponse("no_results", 5)
    else:
        return ApiResponse("not_success_external", 10)

def get_person_urls(href):
    """
    Function to retrieve profile URLs for people.

    Parameters:
    - href: fragment of the person's profile URL

    Returns:
    - ApiResponse: API response with the list of URLs or error message
    """
    person_urls = []  # List to store profile URLs

    url = f"https://radaris.com{href}"

    # If the search parameter is empty
    if not href:
        return ApiResponse("not_empty", 20)
    
    response = requests.get(url, timeout=60)
    
    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Parse JSON-LD containing profile URLs
        profiles_list = soup.find("div", class_="profiles-list", id="tbl_ps")
        item_list = profiles_list.find_all("script", type="application/ld+json")[1]
        
        items = json.loads(item_list.text)
        for item in items["itemListElement"]:
            cleared_url = item["@id"].split("?", 1)[0]
            person_urls.append(cleared_url)
        
        return ApiResponse(person_urls, 0)
    elif response.status_code == 301:
        return ApiResponse("no_results", 5)
    else:
        return ApiResponse("not_success_external", 10)

def parse_bullets(td):
    """
    Function to parse the values of table cells where data is separated by bullet points.

    Parameters:
    - td: table cell (HTML element)

    Returns:
    - items: list of values from the cell
    """
    items = []
    for content in td.contents:
        if isinstance(content, str):
            parts = content.split('•')
            for part in parts:
                clean_part = part.strip()
                if clean_part:
                    items.append(clean_part)
        elif content.name:
            items.append(content.text.strip())
    return items

def get_person(url):
    """
    Function to retrieve detailed information about a person based on their profile URL.

    Parameters:
    - url: URL of the person's profile

    Returns:
    - ApiResponse: API response with the person's data or error message
    """
    if not url:
        return ApiResponse("not_empty", 20)
    
    response = requests.get(url, timeout=60)
    
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        tbody = soup.find('tbody')

        data = {}

        try:
            for row in tbody.find_all("tr"):
                key = row.find("td", class_="td-title").text.strip()
                value_td = row.find_all("td")[1]
                value = parse_bullets(value_td)
                data[key] = value if len(value) > 1 else value[0]
        except AttributeError:
            return ApiResponse("no_summary", 5)

        return ApiResponse(data, 0)
    else:
        return ApiResponse("not_success_external", 10)

@app.route('/')
def index():
    return render_template('index.html')

# Search for a person and return a list of possible names
@app.route('/search', methods=['GET'])
def api_search():
    name = request.args.get('name', type=str)
    if not name:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    if " " in name:
        return jsonify({"error": "Parameter 'name' contains whitespace"}), 400
    items = search(name).response
    objects = []
    if isinstance(items, str):
        response_message = items
        return jsonify({"error": response_message}), 400
    else:
        for result in items:
            objects.append({"name": result.name, "href": result.href})
        return jsonify(objects)

# Get profile URLs from a given name
@app.route('/urls', methods=['GET'])
def api_urls():
    href = request.args.get('href')
    if not href:
        return jsonify({"error": "Missing 'href' parameter"}), 400
    items = get_person_urls(href)
    if isinstance(items, str):
        response_message = items
        return jsonify({"error": response_message}), 400
    else:
        return jsonify(items.response)

# Get detailed data from an individual's profile
@app.route('/data', methods=['GET'])
def api_data():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    data = get_person(url)
    if isinstance(data.response, str):
        response_message = data.response
        return jsonify({"error": response_message}), 400
    else:
        return jsonify(data.response)

if __name__ == '__main__':
    app.run(debug=True)