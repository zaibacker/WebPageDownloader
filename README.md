# WebPageDownloader
Implement a command line program that can fetch web pages , saves them to disk and store metadata information in python3.

FUNCTIONALITIES

This program should support the following functions :

- Fetch the web site and store it with all its elements ( css, pictures etc.) in disk. 
- Create a CSV metadatada file which store basic data and allow the user to check it



RUNNING

**** Run the program to fetch the web sites with the following command. You can add multiple websites in the same command line.

python3 fetch.py https://website1.com https://website2.com https://website2.com

<Important : the protocol http or https must be written>


**** Run the program to display the metadata information from a fetched website

python3 fetch.py --metadata  https://website1.com

<Important : the protocol http or https must be written>

for example :
$ python3 fetch.py --metadata  https://www.google.com
site : www.google.com
num_links : 17
images : 1
last_fetch : 09/11/2022 18:25:34 JST



DEPENDENCIES

*Dependdencies must be installed using command "pip3 install <Library_name>" or "sudo pip3 install <Library_name>" 

- requests           2.27.1     -> pip3 install requests
- validators         0.20.0     -> pip3 install validators
- bs4                0.0.1      -> pip3 install bs4
- beautifulsoup4     4.11.1     -> pip3 install beautifulsoup4  (this one is probbaly optional because bs4 should already have it)

Tested with python 3.9.10 under Cygwin (Windows)



NEXT FEATURES

* Delete from metadata csv file the old information when same website is fetched. 
* Fetch from websites also their scripts
