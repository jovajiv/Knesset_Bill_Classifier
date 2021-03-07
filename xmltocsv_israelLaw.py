import xml.etree.ElementTree as ET
import unicodecsv as csv

tree = ET.parse("KNS_israelLaw.xml")
root = tree.getroot()
print(root)
# open a file for writing
for member in root:
	print(member)
Resident_data = open(r'.\israeli_laws.csv', 'wb')

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
			BillID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsraelLawID').tag
			resident_head.append('IsraelLawID')
			KnessetNum = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}KnessetNum').tag
			resident_head.append('KnessetNum')
			name = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Name').tag
			resident_head.append('Name')
			IsBasicLaw = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsBasicLaw').tag
			resident_head.append('IsBasicLaw')
			IsFavoriteLaw = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsFavoriteLaw').tag
			resident_head.append('IsFavoriteLaw')
			PublicationDate = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}PublicationDate').tag
			resident_head.append('PublicationDate')
			LatestPublicationDate = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LatestPublicationDate').tag
			resident_head.append('LatestPublicationDate')
			IsBudgetLaw = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsBudgetLaw').tag
			resident_head.append('IsBudgetLaw')
			LawValidityID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LawValidityID').tag
			resident_head.append('LawValidityID')
			LawValidityDesc = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LawValidityDesc').tag
			resident_head.append('LawValidityDesc')
			LastUpdatedDate = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LastUpdatedDate').tag
			resident_head.append('LastUpdatedDate')

			print (resident_head)
			csvwriter.writerow(resident_head)
			count = count + 1
		BillID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsraelLawID').text
		resident.append(BillID)
		KnessetNum = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}KnessetNum').text
		resident.append(KnessetNum)
		name = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Name').text
		resident.append(name)
		IsBasicLaw = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsBasicLaw').text
		resident.append(IsBasicLaw)
		IsFavoriteLaw = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsFavoriteLaw').text
		resident.append(IsFavoriteLaw)
		PublicationDate = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}PublicationDate').text
		resident.append(PublicationDate)
		LatestPublicationDate = content.find(
			'{http://schemas.microsoft.com/ado/2007/08/dataservices}LatestPublicationDate').text
		resident.append(LatestPublicationDate)
		IsBudgetLaw = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}IsBudgetLaw').text
		resident.append(IsBudgetLaw)
		LawValidityID = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LawValidityID').text
		resident.append(LawValidityID)
		LawValidityDesc = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LawValidityDesc').text
		resident.append(LawValidityDesc)
		LastUpdatedDate = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}LastUpdatedDate').text
		resident.append(LastUpdatedDate)
		csvwriter.writerow(resident)
Resident_data.close()


