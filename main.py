#!/usr/bin/python3

# TODO: get query and location as args
# TODO: allow user to queue up multiple titles & locations

from pathlib import Path
from random import choice
from requests_html import HTMLSession
from time import sleep
import csv
import lxml.html
import re

outputFile = ""

def main():
    global outputFile
    # control flow
    session = HTMLSession()
    query = re.sub(" ","+",input("Enter job title to search for:\n")).lower()
    location = re.sub(" ","+",input("Enter location (city, state, zipcode, or \"remote\"):\n")).lower()
    url = f'https://www.indeed.com/jobs?q={query}&l={location}'
    outputFile = f"indeed_results_{query}_{location}.csv"
    prepCSV()
    scrape(session,url)

def scrape(session,url):
    print(f"\nScraping {url} ...")
    html = obtainData(session,url)
    data = parseData(html)
    writeData(data)
    sleep(choice(range(3,15)))
    scrape(session,nextPage(html))

def obtainData(session,url):
    # code to make request and store in session object
    response = session.get(url)
    return response.text

def parseData(html):
    # code to parse html we obtained
    doc = lxml.html.fromstring(html)
    data = []
    rootXpath = './table[contains(@class,"main")]/tbody/tr/td[@class="resultContent"]/'
    postings = doc.xpath('//div[@class="job_seen_beacon"]')
    for p in postings:
        try: title = p.xpath(rootXpath+'div/h2/a/span/@title')[0]
        except: title = "-"

        try: company = p.xpath(rootXpath+'div[contains(@class,"companyInfo")]/span')[0].xpath('./a/text()|./text()')[0]
        except: company = "-"

        try: location = p.xpath(rootXpath+'div[contains(@class,"companyInfo")]/div/text()')[0]
        except: location = "-"

        try: pay = p.xpath(rootXpath+'div/div[contains(@class,"salary")]/div/text()')[0] # purposfully not grabbing "Estimated" data
        except: pay = "-"

        try: jobtype = p.xpath(rootXpath+'div/div/div/svg[@aria-label="Job type"]/../text()')[0]
        except: jobtype = "-"

        try: url = "https://www.indeed.com" + p.xpath(rootXpath+'div/h2/a/@href')[0]
        except: continue
        data.append([title,company,location,pay,jobtype,url])
    return data

def nextPage(html):
    try:
        url =  lxml.html.fromstring(html).xpath('//a[@data-testid="pagination-page-next"]/@href')[0]
    except:
        print("Failed to find next page")
        exit()
    return 'https://www.indeed.com' + url

def writeData(data):
    # code to write parsed data to output file
    global outputFile
    with open(outputFile,'a') as f:
        csvwriter = csv.writer(f,delimiter=",",quoting=csv.QUOTE_ALL)
        for datum in data:
            csvwriter.writerow(datum)

def prepCSV():
    global outputFile
    if (Path("./"+outputFile).is_file() != True):
        with open(outputFile,'w') as f:
            csvwriter = csv.writer(f,delimiter=",",quoting=csv.QUOTE_ALL)
            csvwriter.writerow(["TITLE","COMPANY","LOCATION","PAY","JOBTYPE","URL"])


# execute script
main()
