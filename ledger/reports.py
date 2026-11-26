from django.db.models import Sum

from .models import Loan


def branch_totals(branch_code, issued_on, include_repaid):
    loans = Loan.objects.filter(branch__code=branch_code, issued_on=issued_on)
    columns = {"principal_total": Sum("principal")}
    if include_repaid:
        columns["principal_repaid"] = Sum("payments__principal")
    query = loans.values("branch__code").annotate(**columns)
    row = query.get()
    principal_total = row["principal_total"]
    principal_repaid = row.get("principal_repaid")
    return {"principal_total": principal_total, "principal_repaid": principal_repaid}
