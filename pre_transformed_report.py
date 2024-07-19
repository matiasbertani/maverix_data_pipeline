import pandas as pd

from management_report import ManagementReport
from nx_portfolio import NxPortfolio

from constants import DATABASE_PATH


class PreTransformedReport:

    action_map_source = pd.read_csv(DATABASE_PATH / "actions_map_osiris_naranjax.csv", sep=";", dtype=str).values
    response_map_source = pd.read_csv(DATABASE_PATH / "response_ids_map_osiris_naranjax.csv", sep=";", dtype=str).values
    whatsapp_results = pd.read_csv(
        DATABASE_PATH / "whatsapp_results.csv", sep=";", dtype=str)["osiris_results"].values.tolist()

    actions_with_common_transformation = [
        'LLAMADA SALIENTE',
        'LLAMADA ENTRANTE',
        'MAIL',
        'SMS',
    ]

    def __init__(self, management_report: ManagementReport, nx_portfolio: NxPortfolio) -> None:

        self.data = pd.merge(management_report.data, nx_portfolio.data, on="dni", how='inner')

        self.actions_id_map = {
            osiris_action_id: nx_action_id
            for osiris_action_id, nx_action_id in self.action_map_source
        }
        self.response_id_map = {
            osiris_result_id: nx_response_id
            for osiris_result_id, nx_response_id, _ in self.response_map_source
        }
        self.contact_id_map = {
            osiris_response_id: nx_contact_id
            for osiris_response_id, _, nx_contact_id in self.response_map_source
        }

    def transform(self) -> pd.DataFrame:
        self.data = self._do_common_transformation_for_action(self.data, self.actions_with_common_transformation)
        self.data = self._transform_whatsapp_actions(self.data)
        return self.data

    def _do_common_transformation_for_action(self, df: pd.DataFrame, actions_to_transform: list[str]) -> pd.DataFrame:

        rows_to_transform = df["action"].isin(actions_to_transform)

        df.loc[rows_to_transform, "nx_action_id"] = (
            df.loc[rows_to_transform, "action"].apply(lambda action: self.actions_id_map.get(action, pd.NA))
        )

        df.loc[rows_to_transform, "nx_response_id"] = (
            df.loc[rows_to_transform, "result"].apply(lambda result: self.response_id_map.get(result, pd.NA))
        )

        df.loc[rows_to_transform, "nx_contact_id"] = (
            df.loc[rows_to_transform, "result"].apply(lambda result: self.contact_id_map.get(result, pd.NA))
        )

        df.loc[rows_to_transform, "transformed"] = True

        return df

    def _transform_whatsapp_actions(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.transform_whatsapp_actions_for_direct_contact_substatus(df)
        df = self.transform_whatsapp_actions_for_the_right_substatus(df)
        df = self.trasnform_whatsapp_actions_for_wrong_osiris_resulst(df)
        return df

    def _transform_whatsapp_actions_for_direct_contact_substatus(self, df: pd.DataFrame) -> pd.DataFrame:
        rows_to_transform = (df["action"] == "WHATSAPP") & (df["substatus"] == "CONTACTO DIRECTO")
        df.loc[rows_to_transform, "nx_action_id"] = "ENVIAR WHATSAPP"
        df.loc[rows_to_transform, "nx_response_id"] = "WHATSAPP"
        df.loc[rows_to_transform, "nx_contact_id"] = "DEBTOR"
        df.loc[rows_to_transform, "transformed"] = True
        return df

    def _transform_whatsapp_actions_for_the_right_substatus(self, df: pd.DataFrame) -> pd.DataFrame:

        rows_to_transform = (df["action"] == "WHATSAPP") & (df["result"].isin(self.whatsapp_results))

        df.loc[rows_to_transform, "nx_action_id"] = (
            df.loc[rows_to_transform, "action"].apply(lambda action: self.actions_id_map.get(action, pd.NA))
        )

        df.loc[rows_to_transform, "nx_response_id"] = (
            df.loc[rows_to_transform, "result"].apply(lambda result: self.response_id_map.get(result, pd.NA))
        )

        df.loc[rows_to_transform, "nx_contact_id"] = (
            df.loc[rows_to_transform, "result"].apply(lambda result: self.contact_id_map.get(result, pd.NA))
        )

        df.loc[rows_to_transform, "transformed"] = True

        return df

    def _trasnform_whatsapp_actions_for_wrong_osiris_resulst(self, df: pd.DataFrame) -> pd.DataFrame:

        rows_to_transform = df["action"] == "WHATSAPP"

        df.loc[rows_to_transform, "nx_action_id"] = "MAKE CALL"
        df.loc[rows_to_transform, "nx_response_id"] = (
            df.loc[rows_to_transform, "result"].apply(lambda result: self.response_id_map.get(result, pd.NA))
        )
        df.loc[rows_to_transform, "nx_contact_id"] = (
            df.loc[rows_to_transform, "result"].apply(lambda result: self.contact_id_map.get(result, pd.NA))
        )
        df.loc[rows_to_transform, "transformed"] = True

        return df
