# radaris-reverseapi
### Project Description

The Radaris.com Reverse API project is designed to interact with Radaris.com, enabling users to search for individuals and retrieve detailed profile information. It provides a Flask-based web service that exposes several endpoints to perform these operations. Users can search for people by name, retrieve profile URLs from a given name, and get detailed data from an individual's profile.

### Get started

#### 1. Search for a person

**Endpoint:**
```
GET /search
```

**Description:**
This endpoint allows you to search for people based on a provided name. It returns a list of possible matches with their names and profile URLs.

**Parameters:**
- `name` (required): The name of the person to search for.

**Example Request:**
```bash
curl -G http://localhost:5000/search --data-urlencode "name=Kazimierczuk"
```

**Example Response:**
```json
[
  {
    "href": "/p/Adam/Kazimierczuk/",
    "name": "Adam Kazimierczuk"
  },
  {
    "href": "/p/Alicia/Kazimierczuk/",
    "name": "Alicia Kazimierczuk"
  },
  {
    "href": "/p/Alicja/Kazimierczuk/",
    "name": "Alicja Kazimierczuk"
  }
]
```

#### 2. Get profile URLs

**Endpoint:**
```
GET /urls
```

**Description:**
This endpoint retrieves profile URLs for a person based on a provided URL fragment.

**Parameters:**
- `href` (required): The URL fragment of the person's profile.

**Example Request:**
```bash
curl -G http://localhost:5000/urls --data-urlencode "href=/p/Adam/Kazimierczuk/"
```

**Example Response:**
```json
[
  "https://radaris.com/~Adam-Kazimierczuk/1515830380",
  "https://radaris.com/~Anna-Kazimierczuk/1130543411",
  "https://radaris.com/~Adam-Kazimierczuk/1817946293"
]
```

#### 3. Get detailed data

**Endpoint:**
```
GET /data
```

**Description:**
This endpoint retrieves detailed information about a person based on their profile URL.

**Parameters:**
- `url` (required): The URL of the person's profile.

**Example Request:**
```bash
curl -G http://localhost:5000/data --data-urlencode "url=https://radaris.com/~Adam-Kazimierczuk/1817946293"
```

**Example Response:**
```json
{
  "Addresses": "725 Parkwood Ave, Park Ridge, IL 60068",
  "Full Name": "Adam Kazimierczuk",
  "Occupation": "Supervisor",
  "Phones": [
    "(847) 388-8916",
    "(847) 384-8916"
  ]
}
```

### Running the Project

To run the project, make sure you have Flask and other dependencies installed. Then, you can start the Flask application with:

```bash
python main.py
```

The API will be available at `http://localhost:5000` by default.

This project facilitates easy interaction with Radaris.com for searching and retrieving detailed profile information about individuals. By exposing these endpoints, users can programmatically access and utilize the data provided by Radaris.com.

### Credits
- https://github.com/pb0xxx (Piotr Bednarski)

