# Telecom Automation Lab (IMS / API / CI-CD)

This project demonstrates backend API validation for telecom-style asynchronous workflows using Flask, SQLite, Robot Framework, and Jenkins.

## Architecture
- Flask backend simulating IMS registration
- SQLite for persistent registration state
- Robot Framework for API automation
- Jenkins pipeline for CI/CD execution

## APIs
- GET /health
- POST /ims/register
- GET /ims/status/{subscriberId}

## Automation
- Health checks
- Negative validation
- Async workflow validation using polling

## CI/CD
- Jenkins pipeline pulls code from GitHub
- Installs dependencies
- Executes Robot Framework tests
- Archives test artifacts

## Tech Stack
- Python, Flask
- SQLite
- Robot Framework
- Jenkins
