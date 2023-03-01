#!/usr/bin/python3

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
    postings = doc.xpath('//div[@class="job_seen_beacon"]')
    for p in postings:
        try: title = p.xpath('./table[contains(@class,"main")]/tbody/tr/td[@class="resultContent"]/div/h2/a/span/@title')[0]
        except: title = "-"

        try: company = p.xpath('./table[contains(@class,"main")]/tbody/tr/td[@class="resultContent"]/div[contains(@class,"companyInfo")]/span/text()')[0]
        except: company = "-"

        try: location = p.xpath('./table[contains(@class,"main")]/tbody/tr/td[@class="resultContent"]/div[contains(@class,"companyInfo")]/div[@class="companyLocation"]/span[not(@class)]/text()')[0]
        except: location = "-"

        try: pay = p.xpath('./table[contains(@class,"main")]/tbody/tr/td[@class="resultContent"]/div/div[contains(@class,"salary")]/div/text()')[0]
        except: pay = "-"

        try: jobtype = p.xpath('./table[contains(@class,"main")]/tbody/tr/td[@class="resultContent"]/div/div/div/svg[@aria-label="Job type"]/../text()')[0]
        except: jobtype = "-"

        try: url = "https://www.indeed.com" + p.xpath('./table[contains(@class,"main")]/tbody/tr/td[@class="resultContent"]/div/h2/a/@href')[0]
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
        csvwriter = csv.writer(f,delimiter=",",quoting=csv.QUOTE_MINIMAL)
        for datum in data:
            csvwriter.writerow(datum)

def prepCSV():
    global outputFile
    if (Path("./"+outputFile).is_file() != True):
        with open(outputFile,'w') as f:
            csvwriter = csv.writer(f,delimiter=",",quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(["TITLE","COMPANY","LOCATION","PAY","JOBTYPE","URL"])


# execute script
main()
