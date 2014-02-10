import pandas as pd
import urllib2
from pandasql import sqldf

link = "http://www.besttickets.com/blog/wp-content/uploads/2014/02/NBA-Stats-1980-2014.xls"

socket = urllib2.urlopen(link)

#Import NBA data into dataframe and make column headers lowercase
data = pd.read_excel(socket, "All Teams", index_col=None, na_values=['NA'])
data.columns = [x.lower() for x in data.columns]

#Remove 2014 values from DF because of incomplete season
data=data[data.year != 2014]

#Create data frames based on whether the team made playoffs or not
yes_teams = data[data.playoffs=="Yes"]
no_teams = data[data.playoffs=="No"]

#Average the stats per year for good and bad teams
yes_years = yes_teams.groupby([year for year in yes_teams.year]).mean()
no_years = no_teams.groupby([year for year in no_teams.year]).mean()
all_years = data.groupby([year for year in data.year]).mean()

#Write to an excel file
writer = pd.ExcelWriter('/Users/Pranay/NBA_data/nba_output.xls')
yes_years.to_excel(writer, "Made Playoffs")
no_years.to_excel(writer, "Missed Playoffs")
all_years.to_excel(writer, "All Teams")
writer.save()

