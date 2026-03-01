import logging
import yfinance as yf

START_DATE = "2000-12-01"
END_DATE = "2024-12-31"

logger = logging.getLogger(__name__)


def download_ticker(ticker):
    try:
        data = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=False,
            progress=False,
            threads=False
        )

        if data.empty or "Close" not in data.columns:
            raise ValueError("Empty or invalid data")

        close_prices = data["Close"]
        monthly = close_prices.resample("M").last()
        return monthly

    except Exception as e:
        logger.warning(f"Download failed for {ticker}: {e}")
        return None


def download_with_retry(ticker, max_retries=2):
    for attempt in range(max_retries):
        logger.info(f"Attempt {attempt+1} for {ticker}")
        result = download_ticker(ticker)
        if result is not None:
            return result

    logger.error(f"All retry attempts failed for {ticker}")
    return None


def try_replacements(original_ticker, replacements):

    while replacements:
        new_ticker = replacements.pop(0)
        logger.warning(f"Trying replacement {new_ticker} for {original_ticker}")
        result = download_ticker(new_ticker)
        if result is not None:
            logger.info(f"Replacement successful: {new_ticker} used instead of {original_ticker}")
            return new_ticker, result

    logger.error(f"No replacement worked for {original_ticker}")
    return None, None


def get_one_company_price(ticker, replacements=None, max_retries=2):

    result = download_with_retry(ticker, max_retries)

    if result is not None:
        return ticker, result

    new_ticker, replacement_result = try_replacements(ticker, replacements)

    if replacement_result is not None:
        return new_ticker, replacement_result

    return None, None