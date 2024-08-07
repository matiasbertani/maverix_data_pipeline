import pandas as pd

from .constants import DATABASE_PATH


class UsersMap:

    filename = 'usuarios.csv'
    data_delimiter = ';'
    data_encoding = 'latin1'

    def __init__(self) -> None:
        self.users_map = pd.read_csv(
            DATABASE_PATH / self.filename,
            sep=self.data_delimiter,
            encoding=self.data_encoding,
            dtype=str
        )

    def get_map(self) -> dict:
        return {osiris_user: nx_user for osiris_user, nx_user in self.users_map.values}
