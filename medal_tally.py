import streamlit as st

def fetch_medal_tally(df,year,country):
    temp_df=df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"])
    flag=0
    if year=="Overall"and country =="Overall":
        st.header("**Overall Medal Tally**")
        temp_df=temp_df
    elif year=="Overall"and country != "Overall":
        flag=1
        st.header("**Medal Tally of** "+ country)
        temp_df=temp_df[temp_df["region"]==country]
    elif year!="Overall"and country == "Overall":
        st.header("**Medal Tally in** "+str(year)+" Olympics") 
        temp_df= temp_df[temp_df["Year"]==year]
    elif year!="Overall"and country != "Overall":
        st.header(country+" **Overall Performance in** "+str(year))
        temp_df= temp_df[(temp_df["region"]==country) & (temp_df["Year"]==year)]
    if flag==1:
         x=temp_df.groupby("Year")[["Gold","Silver","Bronze"]].sum().sort_values("Year").reset_index()
    else:     
        x=temp_df.groupby("region")[["Gold","Silver","Bronze"]].sum().sort_values("Gold",ascending=False).reset_index()
    x["Total"]=x["Gold"]+x["Silver"]+x["Bronze"]
    return x
