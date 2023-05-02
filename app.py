import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px


from helper import preprocess,nations_over_time
from helper import events_over_time,atheletes_over_time,pivot_table,best_athelete
from helper import Sports_list,yearwise_medal,country_sports_heatmap,best_athelete_countrywise, men_vs_women
from sidebar import country_year_list
from medal_tally import fetch_medal_tally


df= pd.read_csv("athlete_events.csv")
region_df= pd.read_csv("noc_regions.csv")

st.sidebar.title("**Olympic Analysis**")
st.sidebar.image("download.jpg")
user_menu=st.sidebar.radio("**select an option**",["Medals Tally","Overall Analysis","Country-wise Analysis","Athelete wise Analysis"])

df=preprocess(df,region_df)

if user_menu=="Medals Tally":
    st.image("dataset-cover.jpg")
    st.sidebar.header("**Medals Tally**")
    years,countries=country_year_list(df)
  
    selected_year= st.sidebar.selectbox("Select Year",years)
    selected_country= st.sidebar.selectbox("Select country",countries)
    
    medal_tally=fetch_medal_tally(df,selected_year,selected_country)
    st.dataframe(medal_tally,use_container_width=True)

if user_menu=="Overall Analysis":
    Editions=df["Year"].unique().shape[0]-1
    cities=df["City"].unique().shape[0]
    sports=df["Sport"].unique().shape[0]
    events=df["Event"].unique().shape[0]
    nations=df["region"].unique().shape[0]
    athelets=df["Name"].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3= st.columns(3)
    with col1:
        st.subheader("Editions")
        st.title(Editions)
    with col2:
        st.subheader("Cities")
        st.title(cities)
    with col3:
        st.subheader("Sports")
        st.title(sports)
    with col1:
        st.subheader("Events")
        st.title(events)
    with col2:
        st.subheader("Nations")
        st.title(nations)
    with col3:
        st.subheader("Atheletes")
        st.title(athelets)
    st.title("Participating Nations Over the Years ")
    fig=sns.relplot(nations_over_time(df),kind="line",x="Editions",y="No of countries",aspect=1.5)
    st.pyplot(fig)

    st.title("Event Over the Years ")
    fig1=sns.relplot(events_over_time(df),kind="line", x="Editions",y="No of events",aspect=1.5)
    st.pyplot(fig1)

    st.title("Athelete Over the Years ")
    fig2=sns.relplot(atheletes_over_time(df),kind="line",x="Editions",y="No of atheletes",aspect=1.5)
    st.pyplot(fig2)

    st.title("Event Over the Years(Every sport)")
    fig,ax=plt.subplots(figsize=(15,15))
    ax=sns.heatmap(pivot_table(df),annot=True)
    st.pyplot(fig)

    st.title("Most Succesfull Atheletes")
    selected_sport=st.selectbox("**Select sports category**",Sports_list(df))
    st.table(best_athelete(df,selected_sport))

if user_menu=="Country-wise Analysis":
    st.sidebar.header("Country-wise Analysis")
    years,countries=country_year_list(df)
    selected_country= st.sidebar.selectbox("Select country",countries)
    
    st.title(selected_country+" Medal Tally Over the Years")
    fig,ax=plt.subplots(figsize=(8,5))
    ax=sns.lineplot(yearwise_medal(df,selected_country),x="Year",y="Medal")
    st.pyplot(fig)

    st.title(selected_country+" excellence in following sports")
    fig,ax=plt.subplots(figsize=(20,25))
    ax=sns.heatmap(country_sports_heatmap(df,selected_country),annot=True)
    st.pyplot(fig)

    st.title("Top 10 atheletes of "+selected_country)
    st.table(best_athelete_countrywise(df,selected_country))

if user_menu=="Athelete wise Analysis":
    st.title("Distribution of Age wrt Medals ")
    athelete_df= df.drop_duplicates(subset=["Name","region"]).dropna(subset=["Medal","Age"])
    fig=sns.displot(athelete_df,kind="kde",x="Age",hue="Medal",aspect=1.5)
    st.pyplot(fig)

    st.title("Height vs Weight")
    athelete_df=df.drop_duplicates(subset=["Name","region"]).dropna(subset=["Age","Height","Weight"])
    athelete_df["Medal"].fillna("No medal",inplace=True)
    selected_sport=st.selectbox("**Select sports category**",Sports_list(df))
    if selected_sport!="Overall":
        athelete_df=athelete_df[athelete_df["Sport"]==selected_sport]
    fig,ax=plt.subplots(figsize=(10,10))
    ax=sns.scatterplot(athelete_df,x="Weight",y="Height",hue="Medal",style="Sex",s=100)
    st.pyplot(fig)

    st.title("Men vs Women Participation Over the Years")
    final=men_vs_women(df)
    fig=px.line(final,x="Year",y=["males","females"],width=1000,height=800)
    st.plotly_chart(fig)
    