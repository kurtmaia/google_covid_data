import textract
import pdfplumber
import sys
from urllib.request import urlopen, urlretrieve
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import pycountry



def getRegion(subtext,var_str = ["Retail & recreation","Grocery & pharmacy","Parks","Transit stations","Workplaces","Residential"]):
    percs = (subtext[2]+subtext[10]).split("compared to baseline")
    percs = [p2f(f) for f in percs if len(f)>0]
    ans_dict =  dict(zip(var_str,percs))
    return ans_dict

def getRegionPerPage(text1):
    result = {}
    for i in range(int(len(text1)/17)):
        j = i*17
        result[text1[j]] = getRegion(text1[j:(j+17)])
    return result

def getRegionResults(pdfpath):
    pdf = pdfplumber.open(pdfpath)
    if len(pdf.pages) >3:
        finalResult = {}
        for p in tqdm(range(2,len(pdf.pages)-1)):
            page = pdf.pages[p]
            text = page.extract_text()
            if (text.find("compared to baseline")):
                finalResult.update(getRegionPerPage(text.split("\n")))
    else:
        finalResult = None
    pdf.close()
    return finalResult

def p2f(x):
    try:
        ans = float(x.strip('[% ]'))/100
    except Exception as e:
        print(e)
        ans = float('nan')
    return ans

def pdf2dict(pdfpath, var_str = ["Retail & recreation","Grocery & pharmacy","Parks","Transit stations","Workplaces","Residential"] ):
    text = textract.process(pdfpath).decode()
    pointerStr = "About this data"
    subtext = text[(text.find(pointerStr)+len(pointerStr)):]

    bStr = "compared to baseline"
    arr_dict = {}

    for _ in var_str:
        subtext_tmp = subtext[(subtext.find(_)+len(_)):]
        percNum = p2f(subtext_tmp[:(subtext_tmp.find(bStr)+len(bStr))].split("\n")[-2])
        arr_dict[_] = percNum
    
    return arr_dict
    
def gpdfparser(countryCode, date, region = False):
    url_pdf = "https://www.gstatic.com/covid19/mobility/"+date+"_"+countryCode+"_Mobility_Report_en.pdf"
    urlretrieve(url_pdf,"Googledata.pdf")
    ans_country = {countryCode : pdf2dict("Googledata.pdf")}
    cdt = pd.DataFrame(ans_country).T
    cdt.index.names = ["country"]
    cdt = cdt.reset_index()
    cdt["date"] = date
    ans = cdt
    if region:
        ans_region = getRegionResults("Googledata.pdf")
        if ans_region is not None:
            ans_region = pd.DataFrame(ans_region).T
            ans_region.index.names = ["region"]
            ans_region = ans_region.reset_index()
            ans_region["country"] = countryCode
            ans_region["date"] = date
        ans = [cdt,ans_region]
    os.remove("Googledata.pdf")  
    return ans

def havedata(date):
    url_pdf = "https://www.gstatic.com/covid19/mobility/"+date+"_US_Mobility_Report_en.pdf"
    try:
        urlopen(url_pdf)
        ans = True
    except:
        ans = False
    return ans

def countryname2acronym(c):
    try:
        ans = pycountry.countries.search_fuzzy(str(c))[0].alpha_2
    except Exception as e:
        print(e)
        ans = None
    return ans

def get_data_from_date(countrylist,date, useAcronym=False):
    countryLevel = pd.DataFrame()
    regionLevel = pd.DataFrame()    
    for c in countrylist:
        print("Parsing {} results...".format(c))
        if useAcronym:
            cc = c
        else:
            cc = countryname2acronym(c)
        if cc is not None:
            try:
                a1,a2 = gpdfparser(cc,date,region = True)
                a1["countryName"] = c
                countryLevel = countryLevel.append(a1,ignore_index=True)
                if a2 is not None:
                    a2["countryName"] = c
                    regionLevel = regionLevel.append(a2,ignore_index=True)
            except Exception as e:
                print(e)
    return countryLevel, regionLevel

def get_google_data(countrylist,datelist = None, start=1,end=31, month = "03"):
    countryLevel = pd.DataFrame()
    regionLevel = pd.DataFrame()
    if datelist is None:
        datelist = ["2020-{}-{:02d}".format(month,day) for day in range(start,end+1)]
    for fullday in datelist:
        try:
            a1, a2 = get_data_from_date(countrylist,fullday)
            countryLevel = countryLevel.append(a1,ignore_index=True)
            regionLevel = regionLevel.append(a2,ignore_index=True)
        except Exception as e:
            print("No data on {}".format(fullday))
    return countryLevel, regionLevel
    