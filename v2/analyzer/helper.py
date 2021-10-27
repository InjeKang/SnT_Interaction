def create_breakpoints(start_year, end_year, max_month):
    years = list(range(start_year, end_year+1))
    months = ["0{}".format(i) if i < 10 else "{}".format(i) for i in range(1, 13)]
    year_month = ["{}{}".format(year, month)
                    for year in years for month in months
                    if int("{}{}".format(year, month)) <= max_month]
    year_month = pd.Series(year_month)
    year_month = year_month.map(lambda x: dt.datetime.strptime(x, "%Y%m"))
    return year_month