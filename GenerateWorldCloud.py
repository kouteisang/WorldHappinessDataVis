import wordcloud
import pandas as pd


# generate world cloud
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
worldCloudText = ''

file = pd.read_csv(str(2021) + ".csv")
worldCloudText += " WorldHappinessReportFrom2015-2021"
for index, data in file.iterrows():
    worldCloudText += ' '
    worldCloudText += str(data["Country"] )

w = wordcloud.WordCloud(background_color='white', width=2000, height=150)
w.generate(worldCloudText)
w.to_file('assets/allCountries1.png')