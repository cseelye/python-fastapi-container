# python-fastapi-container
![Pipeline Status](https://github.com/cseelye/python-fastapi-container/actions/workflows/build.yaml/badge.svg)

Template for python microservice using python and FastAPI

## Features
* Full integration with VS Code
    * Remote development container
    * Intellisense / autocomplete
    * Interactive debugging with breakpoints, watches, etc.
    * Port forwarding so you can test the API from your laptop
* FastAPI
    * Consistent, structured error reporting
    * Strongly versioned API endpoints and schemas
* Python
    * Consistent, configurable logging across FastAPI, uvicorn, and the service itself
    * pytest unit tests
    * pylint linting
    * black code formatting
* Github CI/CD
    * Automatic build, lint, test on every commit https://github.com/cseelye/python-fastapi-container/actions/workflows/build.yaml
    * Automatic publish container image to GHCR https://github.com/cseelye/python-fastapi-container/pkgs/container/python-fastapi-container
    * Automatic generate API docs and publish to github pages https://cseelye.github.io/python-fastapi-container/

## Using This Template
This repo is setup as a template repository, so the easiest way to use it is to click the green button **Use this template** at the top of the page and create a new project.
After creating the new project, there are a few things to customize.

* Set the name and description of your service:
    1. Edit `app/main.py` and change the app initialization, and `test/test_v1_api.py` to update the corresponding test
    1. Edit `app/api/v1/schemas.py` and update service_name
    1. If the local container name is different than the directory name, edit `Makefile` and change PROJECT_NAME
    1. If the published container name is different than the repo name, edit `.github/workflows/build.yaml` and change image_name
* Set the port for your service to listen on:
    1. Edit `Dockerfile` and change the port number in SERVICE_PORT
* Edit this README file, remove all of this and add the information about your project.
* Look through the `api/v1` and `api/v2` to understand how to create and reuse API endpoints, and then delete them and
    start building your own!

For more information about building your service, like setting up VS Code, API versioning, unit tests, etc see [CONTRIBUTING.md](CONTRIBUTING.md)
