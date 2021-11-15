import pandas as pd

data = pd.read_csv("olddata/2021.csv")

code = dict()
typo = dict()

print(data.shape[0])
for i in range(data.shape[0]):
    code[data["Country"][i]] = data["Region"][i]


# for year in range(2015, 2021):
#     filename = str(2021) + ".csv"
    file = str(2019) + "_new3.csv"
    frame = pd.read_csv("2019.csv")
    frame["Region"] = ""
for i in range(frame.shape[0]):
    if frame["Country"][i] == "Oman":
        frame["Region"][i] = ''
    elif frame["Country"][i] == "Qatar":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Taiwan":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Suriname":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Trinidad and Tobago":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Hong Kong":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Bhutan":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Macedonia":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Sudan":
        frame["Region"][i] = ''
    elif frame["Country"][i] == "Congo (Kinshasa)":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Djibouti":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Angola":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Central African Republic":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Afghanistan":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Puerto Rico":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Belize":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Somalia":
        frame["Region"][i] = ''
    elif frame["Country"][i] == "Somaliland Region":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "South Sudan":
        frame["Region"][i] =  ''
    elif frame["Country"][i] == "Syria":
        frame["Region"][i] =  ''
    else:
        frame["Region"][i] = code[frame["Country"][i]]
    frame.to_csv(file)
