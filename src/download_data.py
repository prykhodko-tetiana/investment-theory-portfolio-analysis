import os
import logging
import yfinance as yf
import pandas as pd

# -------------------- LOGGING --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -------------------- CONSTANTS --------------------
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


# -------------------- FUNCTIONS --------------------
def download_monthly_prices():
    logger.info("Starting data download from Yahoo Finance...")

    data = yf.download(
        TICKERS,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        progress=False
    )

    close_prices = data["Close"]
    monthly = close_prices.resample("M").last()

    logger.info(f"Downloaded dataset shape: {monthly.shape}")

    # Validation
    if monthly.shape[0] != 289:
        logger.warning("Unexpected number of observations! Expected 289.")

    if monthly.shape[1] != 50:
        logger.warning("Unexpected number of companies! Expected 50.")

    return monthly


def save_raw_data(df: pd.DataFrame):
    os.makedirs("data/raw", exist_ok=True)

    df_reset = df.reset_index()
    df_reset.to_csv(OUTPUT_PATH, index=False)

    logger.info(f"Raw data saved to {OUTPUT_PATH}")


def raw_file_exists():
    return os.path.exists(OUTPUT_PATH)


# -------------------- MAIN --------------------
def main():
    if raw_file_exists():
        logger.info("Raw data file already exists. Skipping download.")
    else:
        logger.info("Raw data file not found. Downloading data...")
        monthly = download_monthly_prices()
        save_raw_data(monthly)


if __name__ == "__main__":
    main()
