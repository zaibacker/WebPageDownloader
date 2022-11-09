#!/usr/bin/env python3
# fetch.py

# fetch web site and all the pictures
# store in medadata file information about the website 

import sys, csv, os, re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import validators
from validators import ValidationFailure
from urllib.parse import urljoin
 
images = 'img'
links = 'a'
metadataFile = ".metadata.csv"
header = ['site','num_links','images','last_fetch']

#Function to find all images , css  etc... and then save them
def soupfindAllnSave(pagefolder, url, soup, tag2find='img', inner='src'):
    if not os.path.exists(pagefolder):
        os.mkdir(pagefolder)
    for res in soup.findAll(tag2find): 
        try:
            filename = os.path.basename(res[inner])  
            fileurl = urljoin(url, res.get(inner))
            filepath = os.path.join(pagefolder, filename)
            res[inner] = os.path.join(os.path.basename(pagefolder), filename)
            if not os.path.isfile(filepath):
                with open(filepath, 'wb') as file:
                    filebin = session.get(fileurl)
                    file.write(filebin.content)
        except Exception as exc:
            i = 1	
    return soup

#Function to save the web site and all its component
def savePage(response, pagefilename='page'):    
   url = response.url
   soup = BeautifulSoup(response.text,"html.parser")
   pagefolder = pagefilename+'_files' # page contents 
   soup = soupfindAllnSave(pagefolder, url, soup, 'img', inner='src')
   soup = soupfindAllnSave(pagefolder, url, soup, 'link', inner='href')    
   with open(pagefilename+'.html', 'w') as file:
      file.write(soup.prettify())
   return soup

#get the time formated
def getTime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

#count number of links and images
def cnt_links(url, type):
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    return len(soup.find_all(type))

#check if url is valid
def is_string_an_url(url_string: str) -> bool:
    result = validators.url(url_string.strip())
    if isinstance(result, ValidationFailure):
        return False
    return result

#check if we have http or https 
def ishttp(url):
    matches = re.search(r'^(((?!https).)+)$', url)
    if matches:
        return True
    else: 
        return False

saveWebPage = True
elementLength = len(sys.argv)

#We must have at least 2 arguments
if elementLength < 2:
	print("arguments missing")
	sys.exit()
	
#We have to choose between saving a webpage or requesting the metadata information
if sys.argv[1] == "--metadata" :
	saveWebPage = False


#Function to save web page , its components and store metadata information
if saveWebPage == True :

	#We store the header of the csv metadata file
    if not os.path.exists(metadataFile):
        with open(metadataFile,'w+') as meta :
            csv_writer = csv.writer(meta)
            csv_writer.writerow(header)
	
	#We loop all the pages we want to store from command line
    for x in range(1,elementLength):
        url = sys.argv[x]

        protocol = "https://"		
        if ishttp(url) == True:
            protocol = "http://"
		
        if is_string_an_url(url.strip()) == False :
            print('incorrect url:', url)
            break

        try:
            url.index(protocol)
        except ValueError:
            print("Could not find " + url)
        else:
			#In this else we have all the logic to save the pages and its components
			
             print(url + " Found!")
             try:         
                 urlName = url.replace(protocol,"")			 
                 session = requests.Session()
                 response = session.get(url)
                 savePage(response, urlName)
				 
             except urllib.error.HTTPError as e:
                 print("Unable to download page: "+str(e.reason))
                 break
             
			 #We prepare the information to be stored into the csv metadata file
             time = getTime()		
             link_count = cnt_links(url,links)
             image_count = cnt_links(url,images)
             data = [urlName, link_count, image_count, time + " JST"]
		 
			#We store the information into the csv metadata file
             with open(metadataFile,'a+') as meta :
                 csv_writer = csv.writer(meta)
                 csv_writer.writerow(data)

#From here we are going to read and display the information from the csv metadata file				 
else:

    site = ""
    link = ""
    image = ""
    date = ""
	
    with open(metadataFile, mode='r') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
	    
			#We must introduce the website to search with the http or https protocol
            urlFile = row[0]
            urlInput = sys.argv[2]
            protocol = "https://"		
            if ishttp(urlInput) == True:
                protocol = "http://"
            urlNoHTTP = urlInput.replace(protocol,"")

            if urlNoHTTP == urlFile :

                site = row[0]
                link = row[1]
                image = row[2]
                date = row[3]

	# We display the information				
    if site == "" :
        print("no data found!")
    else :
        print("site : " + site)
        print("num_links : " + link)
        print("images : " + image)
        print("last_fetch : " + date) 