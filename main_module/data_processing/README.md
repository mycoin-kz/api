# Data Processing Module

This module handles all data collection, processing, and aggregation tasks for cryptocurrency data.

## Structure

```
data_processing/
├── api_aggregations/     # Aggregates data for API endpoints
├── internal_tools/       # Shared utilities and helper functions
├── pipelines/           # Data processing pipelines
├── oneshots/           # One-time scripts
└── main.py            # Main orchestration script
```

## Components

### API Aggregations

- Processes and formats data for API consumption
- Generates summary, signals, and detailed data views

### Internal Tools

- Helper functions for data processing
- Database utilities
- Telegram notifications

### Pipelines

- Trading signals collection
- Social data processing
- OHLCV data collection
- Technical indicators calculation

## Usage

The main script (`main.py`) orchestrates various data processing tasks:

1. Collects trading signals
2. Gathers social media data (weekly)
3. Updates OHLCV data
4. Calculates technical indicators
5. Aggregates data for API endpoints

To run all pipelines:

```bash
python main.py
```

## Development

When adding new pipelines:

1. Add the pipeline module in the appropriate directory
2. Update main.py to include the new pipeline
3. Add error handling and logging
4. Update tests if necessary
