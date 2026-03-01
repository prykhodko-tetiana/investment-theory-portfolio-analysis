from src.data.download_batch import main as download_data
from src.data.data_cleaning import main as data_cleaning


if __name__ == "__main__":
    download_data()
    data_cleaning()