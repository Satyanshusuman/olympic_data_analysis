import pandas as pd 

def preprocess(df,region_df):
    df=df[df["Season"]=="Summer"]
    df=df.merge(region_df,on="NOC",how="left")
    df.drop_duplicates(inplace=True)
    df=pd.concat([df,pd.get_dummies(df["Medal"])],axis=1)
    return df

def nations_over_time(df):
    nations_over_time= df.drop_duplicates(subset=["Year","region"])["Year"].value_counts().reset_index().sort_values("index")
    nations_over_time.rename(columns={"index":"Editions","Year":"No of countries"},inplace=True)
    return nations_over_time

def events_over_time(df):
    events_over_time= df.drop_duplicates(subset=["Year","Event"])["Year"].value_counts().reset_index().sort_values("index")
    events_over_time.rename(columns={"index":"Editions","Year":"No of events"},inplace=True)
    return events_over_time

def atheletes_over_time(df):
    atheletes_over_time= df.drop_duplicates(subset=["Year","Name"])["Year"].value_counts().reset_index().sort_values("index")
    atheletes_over_time.rename(columns={"index":"Editions","Year":"No of atheletes"},inplace=True)
    return atheletes_over_time

def pivot_table(df):
    x=df.drop_duplicates(subset=["Year","Sport","Event"])
    x=x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0).astype(int).sort_values("Sport")
    return x

def best_athelete(df,sport):
    temp_df=df.dropna(subset=["Medal"])
    if sport!="Overall":
        temp_df=temp_df[temp_df["Sport"]==sport]
    temp_df=temp_df["Name"].value_counts().reset_index()
    temp_df=temp_df.merge(df,left_on="index",right_on="Name").drop_duplicates(subset=["index"]).head(10)
    x=temp_df[["index","Sport","Name_x","region"]]
    return x.rename(columns={"index":"Name","Name_x":"No of medals"})

def Sports_list(df):
    Sports=df["Sport"].unique().tolist()
    Sports.sort()
    Sports.insert(0,"Overall")  
    return Sports

def yearwise_medal(df,country):
    temp_df=df.dropna(subset=["Medal"])
    if country!="Overall":
           temp_df=temp_df[temp_df["region"]==country]
    temp_df=temp_df.drop_duplicates(["Team","Year","Sport","Event","NOC","Games","Medal"])
    return temp_df.groupby("Year")["Medal"].count().reset_index()
    
    
def country_sports_heatmap(df,country):
    temp_df=df.dropna(subset=["Medal"])
    if country!="Overall":
           temp_df=temp_df[temp_df["region"]==country]
    temp_df=temp_df.drop_duplicates(["Team","Year","Sport","Event","NOC","Games","Medal"])
    return temp_df.pivot_table(index="Sport",columns="Year",values="Medal",aggfunc="count").fillna(0)

def best_athelete_countrywise(df,country):
    temp_df=df.dropna(subset=["Medal"])
    if country!="Overall":
        temp_df=temp_df[temp_df["region"]==country]
    temp_df=temp_df["Name"].value_counts().reset_index()
    temp_df=temp_df.merge(df,left_on="index",right_on="Name").drop_duplicates(subset=["index"]).head(10)
    x=temp_df[["index","Name_x","region","Sport"]]
    return x.rename(columns={"index":"Name","Name_x":"No of medals"})

def men_vs_women(df):
    male=df[df["Sex"]=="M"].drop_duplicates(subset=["Name"]).groupby("Year")["Name"].count().reset_index()
    female=df[df["Sex"]=="F"].drop_duplicates(subset=["Name"]).groupby("Year")["Name"].count().reset_index()
    temp_df=male.merge(female,on="Year",how="left").rename(columns={"Name_x":"males","Name_y":"females"})
    temp_df.fillna(0,inplace=True)                                                
    return temp_df
