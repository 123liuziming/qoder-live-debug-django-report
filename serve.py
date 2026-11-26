import os
from wsgiref.simple_server import make_server, WSGIRequestHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.core.wsgi import get_wsgi_application
from django.db import connection

application = get_wsgi_application()
from ledger.models import Branch, Loan, Repayment


def prepare_demo():
    existing = connection.introspection.table_names()
    with connection.schema_editor() as schema:
        for model in (Branch, Loan, Repayment):
            if model._meta.db_table not in existing:
                schema.create_model(model)
    branch, _ = Branch.objects.get_or_create(code="demo-east")
    if not Loan.objects.filter(branch=branch).exists():
        loan = Loan.objects.create(branch=branch, borrower="小李", issued_on="2026-11-01", principal=1000)
        Repayment.objects.bulk_create([Repayment(loan=loan, principal=100), Repayment(loan=loan, principal=200)])


class QuietRequests(WSGIRequestHandler):
    def log_message(self, *args):
        pass


if __name__ == "__main__":
    prepare_demo()
    with make_server("127.0.0.1", int(os.getenv("REPORT_PORT", "8080")), application, handler_class=QuietRequests) as httpd:
        print(f"报表地址：http://127.0.0.1:{httpd.server_port}/", flush=True)
        httpd.serve_forever()
