from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse
from pyecharts.charts import Line
from pyecharts.options import RenderOpts
from datetime import datetime, timedelta

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates/dashboard"))

from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
from django.apps import apps
import random
from calendar import monthrange


def index(request):
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题")
        )
    )
    return HttpResponse(c.render_embed(template_name="simple_chart.html"))


def all_accounts(request):
    """使用accounts app下的models，查询所有Account数量并返回"""
    try:
        # Dynamically load the Account model from the accounts app
        Account = apps.get_model("accounts", "Account")

        # Query the count of all Account instances
        account_count = Account.objects.count()

        # Return the count in the HttpResponse
        return HttpResponse(f"Total Accounts: {account_count}")
    except LookupError:
        # Handle the case where the Account model is not found
        return HttpResponse("Account model not found in the accounts app", status=404)


def main(request, start_date_str, end_date_str):
    # generate some dates for the x axis from the date string in request
    # Default to today's date if not provided
    # start_date_str = request.GET.get("start_date", datetime.now().strftime("%Y-%m-%d"))

    # end_date_str = request.GET.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    tl = Timeline()
    tl.options.get("baseOption").get("timeline").update({"currentIndex": 1})
    for n in range(1, 13):

        # start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        # end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        start_date = datetime.strptime(start_date_str[:8] + "01", "%Y-%m-%d")
        # (start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(
            start_date_str[:8] + str(monthrange(int(end_date_str[:4]), month=n)[1]),
            "%Y-%m-%d",
        )
        x = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end_date - start_date).days)
        ]
        # generate some float number for the y axis
        y = [round(random.random(), 2) for _ in range((end_date - start_date).days)]
        c = Line().add_xaxis(x).add_yaxis("custom", y, is_smooth=True).set_global_opts()
        tl.add(c, f"{n}月")
    return HttpResponse(tl.render_embed(template_name="_base.html"))


def yearview(request):
    tl = Timeline()
    year = datetime.now().year
    month = datetime.now().month
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    months_cap = months[:month]
    tl.options.get("baseOption").get("timeline").update(
        {"currentIndex": month, "autoPlay": False}
    )
    for n in months_cap:
        start_date = datetime.strptime(str(year) + n + "01", "%Y%m%d")
        end_date = datetime.strptime(
            str(year) + n + str(monthrange(year, month=int(n))[1]),
            "%Y%m%d",
        )
        x = [
            (start_date + timedelta(days=i)).strftime("%Y%m%d")
            for i in range((end_date - start_date).days)
        ]
        # generate some float number for the y axis
        y = [round(random.random(), 2) for _ in range((end_date - start_date).days)]
        c = Line().add_xaxis(x).add_yaxis("custom", y, is_smooth=True).set_global_opts()
        tl.add(c, f"{n}月")
    return HttpResponse(tl.render_embed(template_name="_base.html"))
