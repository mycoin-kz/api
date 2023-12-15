from internal_tools.helpers import send_message_tg
from datetime import date


if __name__ == '__main__':
    MESSAGE = "START SCHEDULED PARSER"
    send_message_tg(MESSAGE)

    try:
        MESSAGE = "Get Trading Signals STARTED!"
        send_message_tg(MESSAGE)
        import pipelines.cc_get_trading_signals
    except Exception as e:
        MESSAGE = f"Get Trading Signals FAILED: {e}"
        send_message_tg(MESSAGE)

    if date.today().weekday() == 2:
        try:
            MESSAGE = "Get Social Data STARTED!"
            send_message_tg(MESSAGE)
            import pipelines.cc_get_social_data
        except Exception as e:
            MESSAGE = f"Get Social Data FAILED: {e}"
            send_message_tg(MESSAGE)

    try:
        MESSAGE = "Get Daily OHLCV STARTED!"
        send_message_tg(MESSAGE)
        import pipelines.cc_get_daily_ohlcv
    except Exception as e:
        MESSAGE = f"Get Daily OHLCV FAILED: {e}"
        send_message_tg(MESSAGE)

    try:
        MESSAGE = "Calculate Technical Indicators STARTED!"
        send_message_tg(MESSAGE)
        import pipelines.calculate_technical_indicators
    except Exception as e:
        MESSAGE = f"Calculate Technical Indicators FAILED: {e}"
        send_message_tg(MESSAGE)

    try:
        MESSAGE = "Aggregation for API STARTED!"
        send_message_tg(MESSAGE)
        import api_aggregations.aggregate_for_api_data
    except Exception as e:
        MESSAGE = f"Aggregation for API FAILED: {e}"
        send_message_tg(MESSAGE)

    try:
        MESSAGE = "Aggregation for API SUMMARY STARTED!"
        send_message_tg(MESSAGE)
        import api_aggregations.aggregate_for_api_summary
    except Exception as e:
        MESSAGE = f"Aggregation for API SUMMARY FAILED: {e}"
        send_message_tg(MESSAGE)

    try:
        MESSAGE = "Aggregation for API SIGNALS STARTED!"
        send_message_tg(MESSAGE)
        import api_aggregations.aggregate_for_api_signals
    except Exception as e:
        MESSAGE = f"Aggregation for API SIGNALS FAILED: {e}"
        send_message_tg(MESSAGE)

    send_message_tg("-------------------------")
