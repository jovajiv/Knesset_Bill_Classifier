# Knesset_Bill_Classifier




<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)



<!-- ABOUT THE PROJECT -->
## About The Project

this project handles the task of classifying the Bills in the Kneset,
As of current time , only Israel_Law DB was manually classified (approx 1400 entries), into approx 48 categories
using those entries , i've trained a NaiveBayes ML classifier to identify those categories of 



### Built With
* [Python](https://www.python.org/)
* [Scikit-learn](https://scikit-learn.org/)
* [XML](https://docs.python.org/3/library/xml.etree.elementtree.html)


## Getting Started
 (1) download XML files from the Knesset Odata repository using MergeXML.py , which downloads by increments of 100 entries per xml file , then merges them to one big xml
 (2) given the big XML , run the appropriate XMLtoCSV_{}.py   to convert the xml into CSV with the relevant data
    (a)  person(i.e knesset member)
    (b)  Bill_Initiator
    (c)  Israeli_laws
    (d)  Classification
 (3) for Knesset_Bills :
    (a) run bill_download.py , which downloads the bill doc from odata service in .doc format
    (b) run from cmd "rename *.doc *.docx" to convert to docx format
    (c) run docx_to_txt.py to convert the docx files to txt files.
 (4) for israel_laws:
    (a) run download_law, which:
        (*) creates dictionary including only law_ids who have classification
        (*) manipulate the dicitonary so each key (i.e law_id) has an array of classifications (52 possible classifications)
        (*) creates csv called attempt_to_manipuate_law with 52 possible classifications
        (*) attempt to download classified law context from open knesset wiki as those are not available in odata service.
        (*) create csv called file.csv with 52 possible classifications , only for laws who has classification and were sucessfully downloaded from the open knesset wiki
    (b) run parse_law.py which removes metadata info added by the open knesset website when downloading from there.
 (5) for laws downloaded in 
    
 





