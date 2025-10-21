# Hospitality Insights SaaS

This repository contains a lightweight SaaS reference implementation that unifies
point-of-sale (POS) and reservation system data for hospitality groups. The
service exposes REST APIs for retrieving raw integrations and analytics built on
sample datasets.

## Features

- FastAPI application with typed responses
- Automated aggregation of revenue and occupancy metrics across vendors
- Ready-to-use sample datasets for POS and reservation providers
- Comprehensive test coverage using `pytest`

## Getting Started

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the API locally:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Access the interactive API docs at `http://127.0.0.1:8000/docs`.

## Running Tests

Execute the automated test suite with:

```bash
pytest
```

## Project Structure

- `app/`: FastAPI application source code
- `docs/`: Vendor research and integration notes
- `samples/`: Example CSV exports used by the service
- `tests/`: Automated tests for the API
- `requirements.txt`: Runtime and test dependencies
