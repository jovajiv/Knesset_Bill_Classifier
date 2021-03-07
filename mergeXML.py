import os, os.path, sys
import glob
import urllib.request
from xml.etree import ElementTree
import time






#specify the max skiptoken used in odata kneset gov for this query , as odata returns info in increments of 100 ,
# going higher then the max is ok , going lower is not
#also need to specify the query table for odata.
def download_by_count(query ,upto):
    print("start download")
    PATH="XML\\"
    index=0
    while(upto > index):

        urllib.request.urlretrieve("http://knesset.gov.il/Odata/ParliamentInfo.svc/{}()?$skip={}&top=100".format(query,index),PATH+"xml_{}.xml".format(index))
        index +=100

def init_download(query):
    global index
    print("start download")
    PATH="XML\\xml_{}.xml".format(0)
    url = "http://knesset.gov.il/Odata/ParliamentInfo.svc/{}()".format(query)
    urllib.request.urlretrieve(url,PATH)
    index +=100
    return PATH

def download(url):
    global index
    print("start download")
    PATH="XML\\xml_{}.xml".format(index)
    retry(url,PATH)
    #urllib.request.urlretrieve(url,PATH)
    index +=100
    return PATH


def retry(url,PATH):
    remaining_download_tries = 15


    while remaining_download_tries > 0:
        try:
            urllib.request.urlretrieve(url, PATH)
            print("successfully downloaded: " + url)
            #time.sleep(0.1)
        except:
            print("error downloading " + url + " on trial no: " + str(16 - remaining_download_tries))
            remaining_download_tries = remaining_download_tries - 1
            time.sleep(2)
            continue
        else:
            break



def run(query):
    ElementTree.register_namespace('', "http://www.w3.org/2005/Atom")
    ElementTree.register_namespace('d',"http://schemas.microsoft.com/ado/2007/08/dataservices")
    ElementTree.register_namespace('m',"http://schemas.microsoft.com/ado/2007/08/dataservices/metadata")
    ElementTree.register_namespace('base',"http://knesset.gov.il/Odata/ParliamentInfo.svc")


    xml_element_tree = None
    file=init_download(query)
    while 1:
        root = ElementTree.parse(file).getroot()

        if xml_element_tree is None:
            xml_element_tree = root
            to_remove=root.findall(".")[0][-1]                      # remove the next label from the final result
            next = root.findall(".")[0][-1].attrib['href']
            file = download(next)
            xml_element_tree.remove(to_remove)
            continue
        else:
            for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):
                temp = ElementTree.Element('entry')
                temp.append(entry)
                xml_element_tree.extend(temp)
        try:
            next = root.findall(".")[0][-1].attrib['href']
            print(next)
        except:
            break
        file = download(next)




    if xml_element_tree is not None:
        #print(ElementTree.tostring(xml_element_tree))
        f = open("myfile.xml", "wb")
        f.write(ElementTree.tostring(xml_element_tree, encoding='utf8'))
        f.close()


 ############################################################################################### this is main ###############################################################################
index=0

#download_by_count("KNS_Bill",100)
run("KNS_IsraelLaw")
# need to manually delete the next..





def old_run():
    files = "./XML"
    ElementTree.register_namespace('', "http://www.w3.org/2005/Atom")
    ElementTree.register_namespace('d',"http://schemas.microsoft.com/ado/2007/08/dataservices")
    ElementTree.register_namespace('m',"http://schemas.microsoft.com/ado/2007/08/dataservices/metadata")
    ElementTree.register_namespace('base',"http://knesset.gov.il/Odata/ParliamentInfo.svc")

    xml_files = glob.glob(files +"/*.xml")
    xml_element_tree = None
    #init_download("KNS_IsraelLawClassificiation")
    for xml_file in xml_files:
        root = ElementTree.parse(xml_file).getroot()

        if xml_element_tree is None:
            xml_element_tree = root
            temp= root.findall(".")[0][-1]
            print(root.findall(".")[0][-1].attrib['href'])      #next

            #for link in xml_element_tree.findall('{http://www.w3.org/2005/Atom}link'):
            #    print(link.attrib)

            continue
        for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):

            temp = ElementTree.Element('entry')
            temp.append(entry)
            xml_element_tree.extend(temp)
            #print(ElementTree.tostring(xml_element_tree,encoding='utf8'))

    if xml_element_tree is not None:
        toto=xml_element_tree.find('link')
        print(ElementTree.tostring(xml_element_tree))
        f = open("myfile.xml", "wb")
        f.write(ElementTree.tostring(xml_element_tree,encoding='utf8'))
        f.close()
