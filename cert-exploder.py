import pandas as pd 
import csv


def explode(filepath):
	'''
	Takes an Excel report of teachers with CS licenses, de-aggragates by
	endorsement and by certification for easier analysis.

	Inputs: filename of Excel file 

	Returns: Dataframe 'endorsements', dataframe 'certifications', 
			dataframe 'teachers'
	'''
	teachers = pd.read_excel(filepath)
	#add unique ID for each teacher
	teachers['teacherID'] = 0
	for row in range(len(teachers)):
		teachers['teacherID'][row] = row #id is equivalent to row in og dataframe
	#create dataframe that records endorsements
	endorsements = pd.DataFrame(columns = ['teacherID', 'endorsement'])
	for row in range(len(teachers)):
		ID = teachers['teacherID'][row]
		endor = teachers['ENDORSMENT'] # "endorsement" is mispelled in the dataset
		endor = endor.split('|')
		for e in endor:
			df = pd.DataFrame([ID, e], columns = ['teacherID', 'endorsement'])
			endorsements = endorsements.append(df)
	#create dataframe that records certifications
	certifications = pd.DataFrame(columns = ['teacherID', 'certification'])
	for row in range(len(teachers)):
		ID = teachers['teacherID'][row]
		cert = teachers['CERTIFICATION']
		cert = endor.split('|')
		for c in cert:
			df = pd.DataFrame([ID, c], columns = ['teacherID', 'certification'])
			certifications = certifications.append(df)
	#remove 'ENDORSMENT' and 'CERTIFICATION' from teachers dataframe
	del teachers['ENDORSMENT']
	del teachers['CERTIFICATION']
	#return dataframes
	return endorsements, certifications, teachers

def main(filepath):
	'''
	Makes two csv files from the given Excel report with fields 'ENDORSMENT' and 
	'CERTIFICATION', one for endorsements and one for ceritifcations
	'''
	#make a .csv with columns for each certification and number of
	#	teachers with that certification
	endorsements, certifications, teachers = explode(filepath)
	ct_certifications = {}
	for row in range(len(certifications)):
		c = certifications['certification'][row]
		ct_certifications[c] = ct_certifications.get(c, 0) + 1
	with open('reports/certification_counts.csv', 'wb') as f: 
        w = csv.DictWriter(f, ['certification', 'count'])
        w.writeheader()
        for key in ct_certifications:
            w.writerow([key, ct_certifications[key]])
    #make a .csv for each type of certifcation
    for key in ct_certifications:
    	certs = certifications[certifications['certification'] == key]
    	IDs = list(certs.pop('teacherID'))
    	twc = teachers[teachers['teacherID'] in IDs] #teachers w certification in question
    	del twc['teacherID']
    	twc.to_csv('reports/certifications/' + key + ".csv")
