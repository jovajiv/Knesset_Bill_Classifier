import xml.etree.ElementTree as ET
import unicodecsv as csv


xmlp = ET.XMLParser(encoding="utf-8")
tree = ET.parse("KNS_BillInitiator.xml",parser=xmlp)
#tree = ET.parse("KNS_IsraelLawClassificiation.xml")
root = tree.getroot()
print(root)
# open a file for writing
for member in root:
	print(member)
Resident_data = open(r'.\Bill_initiatior.csv', 'wb')

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
                BillInitiatorID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}BillInitiatorID').tag
            resident_head.append('BillInitiatorID')
            BillID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}BillID').tag
            resident_head.append('BillID')
            PersonID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}PersonID').tag
            resident_head.append('PersonID')
            IsInitiator = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsInitiator').tag
            resident_head.append('IsInitiator')
            Ordinal = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Ordinal').tag
            resident_head.append('Ordinal')


            print (resident_head)
            csvwriter.writerow(resident_head)
            count = count + 1
        BillInitiatorID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}BillInitiatorID').text
        resident.append(BillInitiatorID)
        BillID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}BillID').text
        resident.append(BillID)
        PersonID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}PersonID').text
        resident.append(PersonID)
        IsInitiator = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsInitiator').text
        resident.append(IsInitiator)
        Ordinal = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Ordinal').text
        resident.append(Ordinal)
        csvwriter.writerow(resident)
Resident_data.close()


