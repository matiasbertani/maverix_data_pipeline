import pandas as pd


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
            'cartera.xlsx',  # FIXME the data must be read from "input" folder
            usecols=self.columns_to_work_with,
            dtype=str,
        )
        self.data.rename(columns=self.columns_to_work_with, inplace=True)
        self.data.drop_duplicates(subset=['dni'], inplace=True)
