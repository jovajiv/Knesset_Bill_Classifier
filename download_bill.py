import xml.etree.ElementTree as ET
import urllib.request
import time
import socket    # to force timeout if filedownload is stuck
import threading
from concurrent.futures import ThreadPoolExecutor




## this file downloads the last doc file related to a bill,
## KNS_Bill.xml includes all bills submitted and uploaded to the knesset. (around 42k bills).
## for each bill , we download a single word file.
#after download is complete , open cmd , go to the path where the files are saved
# and run in cmd :
#                   rename *.doc *.docx

## this way we will have docx files which enables us to read their content in python using "docx2txt" module



xmlp = ET.XMLParser(encoding="utf-8")
tree = ET.parse("KNS_Bill.xml", parser=xmlp)
# tree = ET.parse("KNS_IsraelLawClassificiation.xml")
root = tree.getroot()
print(root)
# open a file for writing
for member in root:
    print(member)

# create the csv writer object


#def retry_for_doc(url,PATH):
  #  remaining_download_tries = 15


   # while remaining_download_tries > 0:
    #    try:
            #urllib.request.urlretrieve(url, PATH)
     #       img = urllib.request.urlopen(url).read()
     #       fhand = open(PATH, 'wb')
      #      fhand.write(img)
       #     fhand.close()
       #     print("successfully downloaded: " + url)
            #time.sleep(0.1)
      #  except:
       #     print("error downloading " + url + " on trial no: " + str(16 - remaining_download_tries))
        #    remaining_download_tries = remaining_download_tries - 1
         #   time.sleep(2)
          #  continue
        #else:
        #    break

def retry(url,PATH):
    global mutex
    remaining_download_tries = 15


    while remaining_download_tries > 0:
        try:
            socket.setdefaulttimeout(15)
            urllib.request.urlretrieve(url, PATH)
            print("successfully downloaded: " + url)
            #time.sleep(0.1)
        except:
            print("error downloading " + url + " on trial no: " + str(16 - remaining_download_tries))
            remaining_download_tries = remaining_download_tries - 1
            time.sleep(16)
            continue
        else:
            break

def download_bill_xml(billID):
    url = "http://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_DocumentBill()?$filter=BillID%20eq%20{}".format(billID)
    print("start download_xml")
    PATH="Bill_document_xml\\bill_xml_{}.xml".format(billID)
    retry(url,PATH)
    #urllib.request.urlretrieve(url,PATH)
    return PATH

def download_bill_doc(billID,url):
    #url = "http://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_DocumentBill()?$filter=BillID%20eq%20{}".format(billID)
    print("start download_word_doc")
    PATH="Bill_document\\bill_doc_{}.doc".format(billID)
    retry(url,PATH)
    #urllib.request.urlretrieve(url,PATH)
    print("path is {}".format(PATH))
    return PATH

class myThread(threading.Thread):


    def __init__(self, billID,url  ):
        threading.Thread.__init__(self)
        self.billID = billID
        self.url = url


    def run(self):
        download_bill_doc(self.billID,self.url)
        # print("Thread id {} prints: \n {}".format(self.threadID,data))




def task(BillID):
    xmlp = ET.XMLParser(encoding="utf-8")
    Path_to_bill_xml = download_bill_xml(BillID)
    tree = ET.parse(Path_to_bill_xml, parser=xmlp)
    root = tree.getroot()
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        for content in entry.find('{http://www.w3.org/2005/Atom}content'):
            FileURL = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}FilePath').text
            FileURL = FileURL.replace(" ",
                                      "%20")  # remove whitespaces to ascii code , as otherwise , the download will fail.
            fileType = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ApplicationDesc').text
            if fileType == "DOC":
                print(FileURL)
                #thr = myThread(BillID, FileURL)
                #thr.start()
                download_bill_doc(BillID,FileURL)






print("done")
count = 0
executor = ThreadPoolExecutor(3)

for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
    for content in entry.find('{http://www.w3.org/2005/Atom}content'):
        xmlp = ET.XMLParser(encoding="utf-8")

        resident = []
        address_list = []
        BillID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}BillID').text
        #resident.append(BillID)
        executor.submit(task,BillID)


time.sleep(10)      # to allow the last thread enough time to finish




#----------------------------------------------------- main thread downloads xml, then subthreads run the doc downloads
#for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
#    for content in entry.find('{http://www.w3.org/2005/Atom}content'):
#        xmlp = ET.XMLParser(encoding="utf-8")
#
#        resident = []
#        address_list = []
#        BillID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}BillID').text
#        #resident.append(BillID)
#        Path_to_bill_xml = download_bill_xml(BillID)
#        tree = ET.parse(Path_to_bill_xml, parser=xmlp)
#        root = tree.getroot()
#        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
#            for content in entry.find('{http://www.w3.org/2005/Atom}content'):
#                FileURL = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}FilePath').text
#                FileURL = FileURL.replace(" ", "%20")  # remove whitespaces to ascii code , as otherwise , the download will fail.
#                fileType = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ApplicationDesc').text
#                if fileType == "DOC" :
#                    print(FileURL)
#                    thr = myThread(BillID,FileURL)
#                    thr.start()
#                    #download_bill_doc(BillID,FileURL)
#
#time.sleep(10)      # to allow the last thread enough time to finish
