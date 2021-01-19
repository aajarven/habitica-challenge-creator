# Habitica Challenge Creator

A simple web app that allows creating challenges in Habitica.


## Running the App for Development Use

## Requirements

Use python 3. I encourage you to use virtualenv:
```
virtualenv .venv -p python3
source .venv/bin/activate
```

Required packages can be installed based on `requirements.txt`:
```
pip install -r requirements.txt
```

## Running the App

To make your site available on `localhost:5000`, you need to run
```
flask run
```
or if you have a virtual machine without ports configured, possibly
```
flask run --host=0.0.0.0
```
instead. After that you should be able to view the page with your browser.
