import pandas as pd

from .users_map import UsersMap

from .constants import INPUT_PATH


class ManagementReport:

    filename = 'gestiones.csv'
    columns_to_work_with = {
        'Mat. Unica': 'dni',
        'Razon Social': 'full_name',
        'Prox. Pago': 'next_payment_date',
        '$ Prox. Pago': 'next_payment_amount',
        'Fecha': 'operation_date',
        'Hora': 'operation_time',
        'Accion': 'action',
        'SubEstado': 'substatus',
        'Resultado': 'result',
        'Usuario': 'user',
        'Ejecutivo': 'executive',
    }
    data_delimiter = ';'
    data_encoding = 'latin1'

    osiris_nx_users_map = UsersMap().get_map()

    def __init__(self) -> None:
        self.data = pd.read_csv(
            INPUT_PATH / self.filename,
            sep=self.data_delimiter,
            encoding=self.data_encoding,
            usecols=self.columns_to_work_with.keys(),
            dtype=str
        )
        self.data.rename(columns=self.columns_to_work_with, inplace=True)
        self.data = self._format_management_report(self.data)

    def _format_management_report(self, df: pd.DataFrame) -> pd.DataFrame:

        df = self._set_operation_datetime(df)
        df = self._set_next_payment_datetime(df)
        df = self._set_next_payment_amount_as_int(df)
        df = self._replace_special_characters(df)
        df = self._set_nx_users(df)
        df = self._delete_unnecessary_columns(df)

        return df

    def _set_operation_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        df['operation_datetime'] = pd.to_datetime(df['operation_date'] + df['operation_time'], format='%Y-%m-%d%H:%M')
        df['operation_datetime'] = df['operation_datetime'].dt.strftime("%Y%m%d%H%M%S")
        return df

    def _set_next_payment_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        operations_with_next_payments = df['next_payment_date'] != '0000-00-00'
        df.loc[operations_with_next_payments, 'next_payment_datetime'] = pd.to_datetime(
            df.loc[operations_with_next_payments, 'next_payment_date'], format='%Y-%m-%d'
        )
        df['next_payment_datetime'] = df['next_payment_datetime'].dt.strftime("%Y%m%d%H%M%S")
        return df

    def _set_next_payment_amount_as_int(self, df: pd.DataFrame) -> pd.DataFrame:
        df.loc[df["next_payment_datetime"].isna(), "next_payment_amount"] = pd.NA
        df.loc[df["next_payment_amount"].notna(), "next_payment_amount"] = (
            df.loc[df["next_payment_amount"].notna(), "next_payment_amount"].astype(float).astype(int).astype(str)
        )
        return df

    def _replace_special_characters(self, df: pd.DataFrame) -> pd.DataFrame:
        df["action"] = self._replace_special_chars_in_column(df["action"])
        df["result"] = self._replace_special_chars_in_column(df["result"])
        df["substatus"] = self._replace_special_chars_in_column(df["substatus"])
        return df

    def _replace_special_chars_in_column(self, columns: pd.Series) -> pd.Series:
        return columns.apply(
            lambda result:
                result
                .replace("Ã\x81", "Á")
                .replace("Ã\x89", "É")
                .replace("Ã\x8d", "Í")
                .replace("Ã\x93", "Ó")
                .replace("Ã\x9a", "Ú")
                .replace("Ã\x91", "Ñ")
        )

    def _set_nx_users(self, df: pd.DataFrame) -> pd.DataFrame:
        df['nx_users'] = df['executive'].map(self.osiris_nx_users_map)
        return df

    def _delete_unnecessary_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=['operation_date', 'operation_time', 'next_payment_date'])
