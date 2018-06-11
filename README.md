# pyramid_test

# Clone from github AKA Microsoft :P
$ git clone git@github.com:OHR7/pyramid_test.git

# Create a Virtual environment 
$ cd pyramid_test
$ pip install virtualenv
$ virtualenv test_env
$ source test_env/bin/activate

# Create a new environment variable for the root of the project virtual environment
$ export VENV=<path of venv>/test_env/ 

# Install the dependencies
$ pip install -e .

# Initialize the DB
$ $VENV/bin/initialize_test_db development.ini

# Start the server
$ $VENV/bin/pserve development.ini --reload

# Project URL's
http://localhost:6543/invoice
GET request returns a Form to create a new invoice
POST request handles the input data in the form to create the new invoice
can be send it by the HTML Form or directly with a JSON POST

http://localhost:6543/invoice.json
GET request returns a JSON with the list of invoices and the list of available items like this:

{
    "results": [
        {
            "id": 1,
            "date": "2018-06-10"
        },
        {
            "id": 2,
            "date": "2018-06-10"
        },
    ],
    "items": [
        {
            "id": 1,
            "amount": 2.0,
            "units": 1,
            "description": "car"
        },
        {
            "id": 2,
            "amount": 3.0,
            "units": 4,
            "description": "boat"
        }
    ]
}

http://localhost:6543/invoice-item
GET request returns a Form to create a new invoice item
POST request handles the input data in the form to create the new item
can be send it by the HTML Form or directly with a JSON POST

http://localhost:6543/invoice-item.json?invoice_id=<id of invoice>
GET request returns a JSON with the list of items in the given invoice id
like this:
{
    "results": [
        {
            "id": 1,
            "amount": 2.0,
            "units": 1,
            "description": "car"
        },
        {
            "id": 2,
            "amount": 3.0,
            "units": 4,
            "description": "boat"
        }
    ]
}





