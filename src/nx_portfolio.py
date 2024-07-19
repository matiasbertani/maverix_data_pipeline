import pandas as pd

from .constants import INPUT_PATH


class NxPortfolio:
    columns_to_work_with = {
        "DU": "du",
        "DNI": "dni",
        "NXDIGITAL": "nx_digital",
        "PRODUCTO": "product",
        "PREFIJO": "prefix",
        "NUMERO": "number",
    }

    def __init__(self) -> None:
        self.data = pd.read_excel(
            INPUT_PATH / 'cartera.xlsx',
            usecols=self.columns_to_work_with,
            dtype=str,
        )
        self.data.rename(columns=self.columns_to_work_with, inplace=True)
        self.data.drop_duplicates(subset=['dni'], inplace=True)
