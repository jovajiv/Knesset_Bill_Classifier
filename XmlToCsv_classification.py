import xml.etree.ElementTree as ET
import unicodecsv as csv

xmlp = ET.XMLParser(encoding="utf-8")
tree = ET.parse("KNS_IsraelLawClassificiation.xml",parser=xmlp)
#tree = ET.parse("KNS_IsraelLawClassificiation.xml")
root = tree.getroot()
print(root)
# open a file for writing
for member in root:
	print(member)
Resident_data = open(r'.\classificiation.csv', 'wb')

# create the csv writer object

csvwriter = csv.writer(Resident_data,encoding= "utf-16")
resident_head = []
print("done")
count = 0
for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
    for content in entry.find('{http://www.w3.org/2005/Atom}content'):
        resident = []
        address_list = []
        if count == 0:
            for jojo in content:
                print(jojo)
            #content = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}
            LawClassificiationID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LawClassificiationID').tag
            resident_head.append('LawClassificiationID')
            IsraelLawID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsraelLawID').tag
            resident_head.append('IsraelLawID')
            ClassificiationID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ClassificiationID').tag
            resident_head.append('ClassificiationID')
            ClassificiationDesc = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ClassificiationDesc').tag
            resident_head.append('ClassificiationDesc')
            LastUpdatedDate = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LastUpdatedDate').tag
            resident_head.append('LastUpdatedDate')


            print (resident_head)
            csvwriter.writerow(resident_head)
            count = count + 1
        LawClassificiationID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LawClassificiationID').text
        resident.append(LawClassificiationID)
        IsraelLawID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsraelLawID').text
        resident.append(IsraelLawID)
        ClassificiationID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ClassificiationID').text
        resident.append(ClassificiationID)
        ClassificiationDesc = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}ClassificiationDesc').text
        resident.append(ClassificiationDesc)
        LastUpdatedDate = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LastUpdatedDate').text
        resident.append(LastUpdatedDate)
        csvwriter.writerow(resident)
Resident_data.close()


