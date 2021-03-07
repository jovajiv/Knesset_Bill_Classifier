import xml.etree.ElementTree as ET
import unicodecsv as csv

xmlp = ET.XMLParser(encoding="utf-8")
tree = ET.parse("KNS_Person.xml",parser=xmlp)
#tree = ET.parse("KNS_IsraelLawClassificiation.xml")
root = tree.getroot()
print(root)
# open a file for writing
for member in root:
	print(member)
Resident_data = open(r'.\person.csv', 'wb')

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
            PersonID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}PersonID').tag
            resident_head.append('PersonID')
            LastName = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LastName').tag
            resident_head.append('LastName')
            FirstName = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}FirstName').tag
            resident_head.append('FirstName')
            GenderDesc = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}GenderDesc').tag
            resident_head.append('GenderDesc')
            IsCurrent = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsCurrent').tag
            resident_head.append('IsCurrent')


            print (resident_head)
            csvwriter.writerow(resident_head)
            count = count + 1
        PersonID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}PersonID').text
        resident.append(PersonID)
        LastName = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LastName').text
        resident.append(LastName)
        FirstName = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}FirstName').text
        resident.append(FirstName)
        GenderDesc = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}GenderDesc').text
        resident.append(GenderDesc)
        IsCurrent = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsCurrent').text
        resident.append(IsCurrent)
        csvwriter.writerow(resident)
Resident_data.close()


