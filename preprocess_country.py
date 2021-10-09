#########################################################################################################
# Covnerting country names
## WIPS has already used The two-letter alphabetic codes in this Recommended Standard are aligned with the universally recognized ISO
# Alpha-2 Codes listed in International Standard ISO 3166-1
# https://www.wipson.com/service/sch/ctryCodePopup.wips >> https://www.wipo.int/export/sites/www/standards/en/pdf/03-03-01.pdf

# To convert the names into two-letter codes
# https://stackoverflow.com/questions/16253060/how-to-convert-country-names-to-iso-3166-1-alpha-2-values-using-python
# https://stackoverflow.com/questions/53923433/how-to-get-country-name-from-country-abbreviation-in-python-with-mix-of-alpha-2
# #########################################################################################################

import os
import pandas as pd
import pycountry #if "PackagesNotFoundError" >> conda install -c conda-forge package_name
import re
import numpy as np
import copy

# setting working directory
# os.chdir("C:/Users/Administrator/Dropbox/Inje-Jiseong/00.Collab/S&T Interaction/Analysis/data/cleansing") # in server
os.chdir("D:/Dropbox/Inje-Jiseong/00.Collab/S&T Interaction/Analysis/data/cleansing") # in local pc

# load data
data = pd.read_excel("data_final2_country.xlsx", sheet_name="Sheet1") # removed rows that do not have values of nation

def string_to_list(string):
    tolist = list(string.split(" | "))
    return tolist

def contain_numeric(value):
    for character in value:
        if character.isdigit():
            return True
    return False

def contain_zipcode(value):
    if bool(re.search(r"(\w\w) (USA)", value)) == True:
        return True
    return False


def remove_zipcode(nation):
    """
    to convert countries' name with zipecode to United States
    such as CA 94270 USA >> US
    """
    nation = re.sub(r"(\w\w) (\d\d\d\d\d) (USA)", "US", nation)
    nation = re.sub(r"(\w\w) (USA)", "US", nation) #such as GA USA
    return nation



# change keys in dictionary
countries={}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2

countries["South Korea"] = countries["Korea, Republic of"]
del countries["Korea, Republic of"]

countries["Czech Republic"] = countries["Czechia"]
del countries["Czechia"]

countries["Vietnam"] = countries["Viet Nam"]
del countries["Viet Nam"]

countries["Peoples R China"] = countries["China"]
del countries["China"]

countries["Taiwan"] = countries["Taiwan, Province of China"]
del countries["Taiwan, Province of China"]

countries["England"] = countries["United Kingdom"]
del countries["United Kingdom"]

countries["Russia"] = countries["Russian Federation"]
del countries["Russian Federation"]

countries["Iran"] = countries["Iran, Islamic Republic of"]
del countries["Iran, Islamic Republic of"]

countries["Moldova"] = countries["Moldova, Republic of"]
del countries["Moldova, Republic of"]

countries["U Arab Emirates"] = countries["United Arab Emirates"]
del countries["United Arab Emirates"]

countries["BELARUS"] = countries["Belarus"]
del countries["Belarus"]

countries["Brunei"] = countries["Brunei Darussalam"]
del countries["Brunei Darussalam"]

countries["Venezuela"] = countries["Venezuela, Bolivarian Republic of"]
del countries["Venezuela, Bolivarian Republic of"]

countries["North Korea"] = countries["Korea, Democratic People's Republic of"]
del countries["Korea, Democratic People's Republic of"]

countries["Syria"] = countries["Syrian Arab Republic"]
del countries["Syrian Arab Republic"]

countries["Palestine"] = countries["Palestine, State of"]
del countries["Palestine, State of"]

countries["Rep Congo"] = countries["Congo"]
del countries["Congo"]

countries["Tanzania"] = countries["Tanzania, United Republic of"]
del countries["Tanzania, United Republic of"]

countries["Trinidad Tobago"] = countries["Trinidad and Tobago"]
del countries["Trinidad and Tobago"]

countries["Cote Ivoire"] = countries["Côte d'Ivoire"]
del countries["Côte d'Ivoire"]

# countries["Serbia Monteneg"] = countries["Serbia"] # 다 serbai로 통일
# del countries["Serbia"]

# countries["Macedonia"] = countries["North Macedonia"] # 다 north macedonia로 통일
# del countries["North Macedonia"]

def country_2digit(data):
    """
    국가명 >> 2 digit 코드로 전환
    """        
    country_name = data.copy()
    for i in range(len(country_name)):
        if country_name["type"][i] == "S": # T는 이미 정리되어 있기 때문에, S만 변환
            country_name["nation"][i] = string_to_list(country_name["nation"][i])
            for j in range(len(country_name["nation"][i])):
                if (contain_numeric(country_name["nation"][i][j]) == True) or (contain_zipcode(country_name["nation"][i][j]) == True):
                    country_name["nation"][i][j] = remove_zipcode(country_name["nation"][i][j])
                elif (country_name["nation"][i][j] == "Wales") or (country_name["nation"][i][j] == "Scotland") or (country_name["nation"][i][j] == "North Ireland"): #united kingdom으로 분류되어 있기 때문에
                    country_name["nation"][i][j] = "GB"                
                else:
                    country_name["nation"][i][j] = countries.get(country_name["nation"][i][j], "invalid code")
        print("Processing element # of row {}".format(i+1))
    return country_name

data2 = country_2digit(data)

#Save in excel
writer = pd.ExcelWriter('data_final2_country_cleansed.xlsx', engine='xlsxwriter')
data2.to_excel(writer, sheet_name="Sheet1")
writer.save()


