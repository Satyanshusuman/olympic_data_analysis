def country_year_list(df):
    years=df["Year"].unique().tolist()
    years.sort()
    years.insert(0,"Overall")

    countries=df["region"].dropna().unique().tolist()
    countries.sort()
    countries.insert(0,"Overall")
    return years,countries