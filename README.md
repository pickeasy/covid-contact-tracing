# COVID Contact Tracing API
Description to be filled

## How is your information protected?
To be filled.

## Deployment
`Dockerfile` is ready for deployment.
It is recommended to reverse proxy through nginx.

## Development
### Setup

Note: This project *requires* Python 3.7+ installed. For Mac users, ensure you are using the correct version of Python because the OS preinstalls Python 2.7 and default `pip` and `python` commands execute in v2.7 rather than v3.x.

1. Clone this repo or create a new one with this as a template.

1. Create a virtual environment for the project and activate it. Run `pip3 install virtualenv` if virtualenv is not installed on Python3.7+
    ```
    $ cd covid-contact-tracing
    $ virtualenv venv --python=python
    $ source venv/bin/activate
    ```

4. Install the required dependencies, and setup automatic code quality checking with `black`.
    ```
    (venv) $ pip install -r requirements.txt
    (venv) $ pip install -r requirements-dev.txt
    (venv) $ pre-commit install
    ```

5. Edit `config.py.bak` with the proper credentials and move it to `config.py`.

### Run Locally
Remember to fill any necessary fields in `config.py`.
1. Make sure you are in your virtualenv that you setup
    ```
    $ source venv/bin/activate
    ```
2. Start server
    ```
    (venv) $ flask run
    ```
   