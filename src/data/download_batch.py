import os
import logging
import yfinance as yf
import pandas as pd

START_DATE = "2000-12-01"
END_DATE = "2024-12-31"
OUTPUT_PATH = "data/raw/prices_2000_2024.csv"

TICKERS = [
    "AAPL", "AMZN", "ADI", "MCHP", "HPQ", "GLW", "WDC", "SWKS",
    "DE", "CAT", "LUV", "EXPD", "TXT", "FAST", "RHI",
    "K", "CSX", "TAP", "BBWI", "LEG", "HAS",
    "RF", "MTB", "FITB", "KEY",
    "CINF", "WRB", "BEN", "IVZ",
    "MDT", "BAX", "XRAY",
    "VLO", "OKE",
    "NUE", "PKG", "MOS",
    "IPG", "OMC",
    "EIX", "AEE", "NEE",
    "FRT", "VTR", "O",
    "JNJ", "PG", "KO", "PEP",
    "MMM"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def download_monthly_prices():

    logger.info("Downloading batch data from Yahoo Finance...")

    data = yf.download(
        TICKERS,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        progress=False,
        threads=False
    )

    close_prices = data["Close"]
    monthly = close_prices.resample("M").last()

    logger.info(f"Dataset shape: {monthly.shape}")

    return monthly


def save_raw_data(df):
    os.makedirs("data/raw", exist_ok=True)
    df.reset_index().to_csv(OUTPUT_PATH, index=False)
    logger.info("Raw batch data saved.")


def main():
    if os.path.exists(OUTPUT_PATH):
        logger.info("Raw file already exists. Skipping download.")
        return

    monthly = download_monthly_prices()
    save_raw_data(monthly)


if __name__ == "__main__":
    main()