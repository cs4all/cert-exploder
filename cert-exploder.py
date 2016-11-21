# coding: utf-8

# In[7]:

import csv
import errno
import os
import pandas as pd


def explode(filepath):
    '''
    Takes an Excel report of teachers with CS licenses, de-aggragates by
    endorsement and by certification for easier analysis.

    Inputs: filename of Excel file

    Returns: Dataframe 'endorsements', dataframe 'certifications',
            dataframe 'teachers'
    '''
    teachers = pd.read_excel(filepath)
    # add unique ID for each teacher
    teachers['teacherID'] = 0
    for row in range(len(teachers)):
        teachers.set_value(row, 'teacherID', row)  # teacherID = row in og dataframe
    #create dataframe that records endorsements
    endorsements = pd.DataFrame(columns=['teacherID', 'endorsement'])
    index = 0
    for row in range(len(teachers)):
        ID = teachers['teacherID'][row]
        endor = str(teachers['ENDORSMENT'][row])  # "endorsement" is mispelled in the dataset
        endor = endor.split('|')
        for e in endor:
            endorsements.loc[index] = [ID, e]
            index += 1
    # create dataframe that records certifications
    certifications = pd.DataFrame(columns=['teacherID', 'certification'])
    index = 0
    for row in range(len(teachers)):
        ID = teachers['teacherID'][row]
        cert = str(teachers['CERTIFICATION'][row])
        cert = cert.split('|')
        for c in cert:
            certifications.loc[index] = [ID, c]
            index += 1
    # remove 'ENDORSMENT' and 'CERTIFICATION' from teachers dataframe
    del teachers['ENDORSMENT']
    del teachers['CERTIFICATION']

    # return dataframes
    return endorsements, certifications, teachers


def mkdir_p(path):
    '''
    http://stackoverflow.com/questions/600268
    '''
    try:
        os.makedirs(path)
    except OSError as exc:  # python > 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def main(filepath):
    '''
    Takes an Excel report of teachers with CS Licenses and makes a report of
    the number of teachers with each type of certifications and reports for each
    individual certification of the teachers that have that certification.
    '''
    # make a .csv with columns for each certification and number of
    #    teachers with that certification

    # make report dirs if they don't exist

    mkdir_p('reports/certifications')
    mkdir_p('reports/endorsements')

    endorsements, certifications, teachers = explode(filepath)
    ct_certifications = {}
    for row in range(len(certifications)):
        c = certifications['certification'][row]
        ct_certifications[c] = ct_certifications.get(c, 0) + 1
    with open('reports/certification_counts.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['Certification', 'Count'])
        for key in ct_certifications:
            w.writerow([key, ct_certifications[key]])
    # make a file for each certification of teachers with that certification
    for key in ct_certifications:
        certs = certifications[certifications['certification'] == key]
        IDs = list(certs.pop('teacherID'))
        twc = teachers[teachers['teacherID'].isin(IDs)]  # teachers w certification in question
        del twc['teacherID']
        twc.to_csv('reports/certifications/' + key + ".csv")
    # make ct_endorsements analogous to ct_certifications
    ct_endorsements = {}
    for row in range(len(endorsements)):
        e = endorsements['endorsement'][row]
        ct_endorsements[e] = ct_endorsements.get(e, 0) + 1
    with open('reports/endorsement_counts.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['Endorsement', 'Count'])
        for key in ct_endorsements:
            w.writerow([key, ct_endorsements[key]])
    # make a file for each endorsement of teachers with that endorsement
    for key in ct_endorsements:
        endor = endorsements[endorsements['endorsement'] == key]
        IDs = list(endor.pop('teacherID'))
        twe = teachers[teachers['teacherID'].isin(IDs)]  # teachers w certification in question
        del twe['teacherID']
        k = key.replace("/", "|") #so as not to be confused with a new filepath
        twe.to_csv('reports/endorsements/' + k + ".csv")

if __name__ == '__main__':
    main("Comp Sci Licenses.xlsx")
