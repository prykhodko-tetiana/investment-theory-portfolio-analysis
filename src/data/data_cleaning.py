import os
import logging
import pandas as pd

try:
    from download_single import get_one_company_price  # <-- новий файл
except ImportError as e:
    from src.data.download_single import get_one_company_price  # <-- спроба імпорту з іншого місця
# -------------------- LOGGING --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -------------------- CONSTANTS --------------------
INPUT_PATH = "data/raw/prices_2000_2024.csv"
OUTPUT_PATH = "data/processed/clean_prices_2000_2024.csv"
EXPECTED_OBS = 289

REPLACEMENT_TICKERS = ["GIS", "FDX", "NSC", "DOV", "EMN", "CLX"]


# -------------------- FUNCTIONS --------------------

def load_data():
    if not os.path.exists(INPUT_PATH):
        logger.error("Raw data file not found.")
        raise FileNotFoundError("Raw data file not found.")

    df = pd.read_csv(INPUT_PATH, parse_dates=["Date"])
    df.set_index("Date", inplace=True)

    logger.info("Raw data successfully loaded.")
    logger.info(f"Initial dataset shape: {df.shape}")
    print(df.size)

    return df



def recover_company(col, df):
    logger.warning(f"{col} incomplete. Attempting recovery...")

    ticker_used, daily_series = get_one_company_price(
        col,
        replacements=REPLACEMENT_TICKERS
    )
    print(daily_series)

    if daily_series is None:
        logger.error(f"{col} could not be recovered.")
        return None,None

    monthly_series = daily_series.resample("M").last()
    monthly_series = monthly_series.reindex(df.index)
    return ticker_used, monthly_series


def check_and_clean_panel(df):
    print(df.size)

    logger.info("Checking completeness of each company...")

    columns_to_drop = []

    for col in df.columns:
        if df[col].count() == EXPECTED_OBS:
            continue

        columns_to_drop.append(col)
    print(columns_to_drop)
    print(df.shape)
    for col in columns_to_drop:

        logger.warning(f"Dropping column {col}")
        df.drop(columns=[col], inplace=True)

    df_recovery = df.copy()
    print(df.shape)

    for col in columns_to_drop:
    
        ticker_used, recovered_series = recover_company(col, df)

        if recovered_series is not None:
            df[ticker_used] = recovered_series
        print(df.shape)


    logger.info(f"Final dataset shape after cleaning: {df.shape}")
    return df

def save_clean_data(df):
    os.makedirs("data/processed", exist_ok=True)

    df_reset = df.reset_index()
    df_reset.to_csv(OUTPUT_PATH, index=False)

    logger.info(f"Cleaned data saved to {OUTPUT_PATH}")


# -------------------- MAIN --------------------

def main():
    if os.path.exists(OUTPUT_PATH):
        logger.info("Cleaned data file already exists. Skipping cleaning.")
        return
    df = load_data()
    df_clean = check_and_clean_panel(df)
    save_clean_data(df_clean)


if __name__ == "__main__":
    main()