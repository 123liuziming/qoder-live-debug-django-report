from django.db import models


class Branch(models.Model):
    code = models.CharField(max_length=32, unique=True)


class Loan(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    borrower = models.CharField(max_length=32)
    issued_on = models.DateField()
    principal = models.IntegerField()


class Repayment(models.Model):
    loan = models.ForeignKey(Loan, related_name="payments", on_delete=models.CASCADE)
    principal = models.IntegerField()
