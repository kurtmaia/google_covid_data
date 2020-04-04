import numpy as np
import pandas as pd
from tqdm import tqdm

from utils import *
    


countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
       'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
       'Bahamas', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium',
       'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil',
       'Brunei', 'Bulgaria', 'Burkina Faso', 'Burma', 'Cabo Verde',
       'Cameroon', 'Canada', 'Chile', 'China', 'Colombia',
       'Congo', 'Costa Rica',
       "Cote d'Ivoire", 'Croatia', 'Cyprus', 'Czechia', 'Denmark',
       'Diamond Princess', 'Dominican Republic', 'Ecuador', 'Egypt',
       'El Salvador', 'Estonia', 'Finland', 'France', 'Gabon', 'Gambia',
       'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guyana', 'Honduras',
       'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq',
       'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan',
       'Kazakhstan', 'Kenya', 'Korea, South', 'Kosovo', 'Lebanon',
       'Libya', 'Lithuania', 'Luxembourg', 'MS Zaandam', 'Malaysia',
       'Mali', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco',
       'Montenegro', 'Morocco', 'Netherlands', 'New Zealand', 'Nicaragua',
       'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman',
       'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland',
       'Portugal', 'Qatar', 'Romania', 'Russia', 'San Marino',
       'Saudi Arabia', 'Senegal', 'Serbia', 'Singapore', 'Slovakia',
       'Slovenia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan',
       'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tanzania',
       'Thailand', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
       'US', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
       'Uruguay', 'Uzbekistan', 'Venezuela', 'West Bank and Gaza',
       'Zambia', 'Zimbabwe']


if __name__ == '__main__':
    dates = []
    for month in range(3,4):
        for d in tqdm(range(1,32)):
            fullday = "2020-{:02d}-{:02d}".format(month,d)
            if havedata(fullday):
                print(fullday)
                dates.append(fullday)

    countryLevel, regionLevel = get_google_data(countries,dates)
    countryLevel.to_csv("countryLevel.csv")
    regionLevel.to_csv("regionLevel.csv")






