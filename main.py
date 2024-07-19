from final_report import FinalReport
from management_report import ManagementReport
from nx_portfolio import NxPortfolio
from pre_transformed_report import PreTransformedReport


if __name__ == "__main__":

    management_report = ManagementReport()
    nx_portfolio = NxPortfolio()

    transformed_report = PreTransformedReport(management_report, nx_portfolio).transform()

    final_report = FinalReport(transformed_report)
    final_report.generate()
    final_report.write_verification()
    final_report.validate()
    final_report.save()
