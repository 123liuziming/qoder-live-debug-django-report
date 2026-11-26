from django.http import JsonResponse

from .reports import branch_totals


def report(request):
    branch_code = request.GET["branch"]
    issued_on = request.GET["issued_on"]
    include_repaid = request.GET.get("include_repaid") == "1"
    result = branch_totals(branch_code, issued_on, include_repaid)
    return JsonResponse(result)


def report_page(request):
    from django.http import HttpResponse
    return HttpResponse("""<!doctype html><html lang="zh"><meta charset="utf-8">
<title>分支机构放款报表</title><main><h1>分支机构放款报表</h1>
<p>机构　东区演示分行　　放款日期　2026-11-01</p>
<label><input id="toggle" type="checkbox"> 显示已还本金</label>
<table><thead><tr><th>放款总额（元）</th><th id="rhead">已还本金（元）</th></tr></thead>
<tbody><tr><td id="total"></td><td id="repaid"></td></tr></tbody></table></main>
<style>body{font:18px system-ui,sans-serif;color:#1f3448;background:#f5f7f8}main{max-width:650px;margin:8vh auto;padding:42px;background:white}label{cursor:pointer}table{width:100%;margin:24px 0;border-collapse:collapse}th,td{text-align:left;padding:13px;border-bottom:1px solid #ccd5d9}td{font-size:26px}</style>
<script>
const toggle = document.getElementById('toggle');
async function refresh() {
  const show = toggle.checked;
  const response = await fetch('/reports/branch?branch=demo-east&issued_on=2026-11-01&include_repaid=' + Number(show));
  const data = await response.json();
  if (toggle.checked !== show) return;
  document.getElementById('total').textContent = data.principal_total;
  document.getElementById('repaid').textContent = data.principal_repaid;
  document.getElementById('repaid').hidden = !show;
  document.getElementById('rhead').hidden = !show;
}
toggle.addEventListener('change', refresh); refresh();
</script></html>""")
