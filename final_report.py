import pandas as pd

from constants import (
    DATABASE_PATH,
    RESULTS_PATH,
    VERIFICATION_PATH,
)


class FinalReport:

    report_model = pd.read_csv(DATABASE_PATH / "report_model.csv", sep=";", dtype=str, nrows=0)

    def __init__(self, transformed_report: pd.DataFrame) -> None:
        self.transformed_report = transformed_report.copy()

    def generate(self) -> pd.DataFrame:

        final_report = self.report_model.copy()

        final_report["operation_datetime_01"] = self.transformed_report["operation_datetime"]
        final_report["operation_datetime_02"] = self.transformed_report["operation_datetime"]
        final_report["du"] = self.transformed_report["du"]
        final_report["nx_col_01"] = self.transformed_report["nx_digital"]
        final_report["product"] = self.transformed_report["product"]
        final_report["nx_col_02"] = self.transformed_report["nx_digital"]
        final_report["data_col_01"] = "PRESTAMO P"
        final_report["index"] = self.transformed_report.index
        final_report["user_nx"] = self.transformed_report["nx_users"]  # FIXME name inconsistence between dfs
        final_report["data_col_02"] = "N"
        final_report["action_id_nx"] = self.transformed_report["nx_action_id"]
        final_report["result_id_nx"] = self.transformed_report["nx_response_id"]
        final_report["contact_id_nx"] = self.transformed_report["nx_contact_id"]
        final_report["number"] = self.transformed_report["number"]
        final_report["prefix"] = self.transformed_report["prefix"]
        final_report["type"] = "CEL"
        final_report["next_payment_amount"] = self.transformed_report["next_payment_amount"]
        final_report["next_payment_datetime"] = self.transformed_report["next_payment_datetime"]
        final_report["data_col_03"] = "N"
        final_report["agency"] = "CUERVO"
        final_report["data_col_04"] = "1"
        final_report["status"] = "PENDING"

        self.verification_df = self._create_verification_df(final_report)
        self.final_report = final_report

        return self.final_report

    def _create_verification_df(self, final_report: pd.DataFrame) -> pd.DataFrame:
        verification_df = final_report.copy()
        idx = final_report.columns.get_loc("data_col_02")
        verification_df.insert(idx + 1, "osiris_action", self.transformed_report["action"])
        verification_df.insert(idx + 2, "osiris_result", self.transformed_report["result"])
        verification_df.insert(idx + 3, "osiris_substatus", self.transformed_report["substatus"])
        return verification_df

    def validate(self) -> None:
        self._validate_the_final_report_transformation("action_id_nx")
        self._validate_the_final_report_transformation("result_id_nx")

    def _validate_the_final_report_transformation(self, id_column: str) -> None:
        na_rows = self.final_report[id_column].isna().sum()
        if na_rows > 0:
            raise ValueError(f"Existen {na_rows} filas en la columna {id_column} vacias")

    def save(self, filename: str = "final_report.csv") -> None:
        self.final_report.to_csv(RESULTS_PATH / filename, sep=";", index=False)
