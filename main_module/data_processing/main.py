"""Main orchestration script for data processing pipelines."""

import logging
import time
from datetime import date
from typing import Optional, Callable

from main_module.data_processing.internal_tools.helpers import send_message_tg
from main_module.data_processing.internal_tools.logging_config import setup_logging

logger = logging.getLogger(__name__)


class Pipeline:
    """Base class for data processing pipelines."""

    def __init__(self, name: str):
        self.name = name

    def execute(self) -> None:
        """Execute the pipeline. Override this method in subclasses."""
        raise NotImplementedError


def run_pipeline(pipeline: Pipeline) -> bool:
    """
    Run a data processing pipeline with proper error handling and logging.

    Args:
        pipeline: Pipeline instance to run

    Returns:
        True if pipeline completed successfully, False otherwise
    """
    start_time = time.time()

    try:
        logger.info(f"{pipeline.name} STARTED!")
        send_message_tg(f"{pipeline.name} STARTED!")

        pipeline.execute()

        duration = time.time() - start_time
        success_msg = f"{pipeline.name} COMPLETED! Duration: {duration:.2f}s"
        logger.info(success_msg)
        send_message_tg(success_msg)
        return True

    except Exception as e:
        duration = time.time() - start_time
        error_msg = f"{pipeline.name} FAILED after {duration:.2f}s: {str(e)}"
        logger.error(error_msg, exc_info=True)
        send_message_tg(error_msg)
        return False


def import_pipeline(module_path: str) -> Optional[Pipeline]:
    """
    Import a pipeline module and return its Pipeline instance.

    Args:
        module_path: Import path for the pipeline module

    Returns:
        Pipeline instance or None if import fails
    """
    try:
        module = __import__(
            f"main_module.data_processing.{module_path}", fromlist=["get_pipeline"]
        )
        return module.get_pipeline()
    except Exception as e:
        logger.error(f"Failed to import pipeline {module_path}: {str(e)}")
        return None


def run_conditional(
    condition: Callable[[], bool], pipeline_path: str, pipeline_name: str
) -> None:
    """
    Run a pipeline if a condition is met.

    Args:
        condition: Function that returns True if pipeline should run
        pipeline_path: Import path for the pipeline module
        pipeline_name: Human-readable name for the pipeline
    """
    if condition():
        pipeline = import_pipeline(pipeline_path)
        if pipeline:
            run_pipeline(pipeline)


def main() -> None:
    """Run all data processing pipelines."""
    setup_logging()

    logger.info("START SCHEDULED PARSER")
    send_message_tg("START SCHEDULED PARSER")

    # Daily pipelines
    daily_pipelines = [
        ("pipelines.cc_get_trading_signals", "Get Trading Signals"),
        ("pipelines.cc_get_daily_ohlcv", "Get Daily OHLCV"),
        ("pipelines.calculate_technical_indicators", "Calculate Technical Indicators"),
    ]

    for path, name in daily_pipelines:
        pipeline = import_pipeline(path)
        if pipeline:
            run_pipeline(pipeline)

    # Weekly pipeline (Wednesday)
    run_conditional(
        lambda: date.today().weekday() == 2,
        "pipelines.cc_get_social_data",
        "Get Social Data",
    )

    # API data aggregation pipelines
    aggregation_pipelines = [
        ("api_aggregations.aggregate_for_api_data", "Aggregation for API"),
        ("api_aggregations.aggregate_for_api_summary", "Aggregation for API SUMMARY"),
        ("api_aggregations.aggregate_for_api_signals", "Aggregation for API SIGNALS"),
    ]

    for path, name in aggregation_pipelines:
        pipeline = import_pipeline(path)
        if pipeline:
            run_pipeline(pipeline)

    logger.info("ALL PIPELINES COMPLETED")
    send_message_tg("-------------------------")


if __name__ == "__main__":
    main()
