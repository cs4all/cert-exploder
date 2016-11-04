# cert-exploder
Takes an Excel report of teachers with CS Licenses, de-aggregates by endorsement for easier analysis

# Data source
HR (main contact) can provide a report of teachers in the district with a CS endorsement and/or degree.

# Initial processing flow
1. Read in .xlsx file, convert to pandas dataframe ('teachers')
1. Add 'TeacherID' column to data frame for later joining
1. Create new dataframe ('endorsements')
  - For each teacher, create an entry with teacherID and endorsement for each pipe-separated entry in the 'ENDORSMENT' column [sic].
1. Create new dataframe ('certifications')
  - For each teacher, create an entry with teacherID and endorsement for each pipe-separated entry in the 'CERTIFICATION' column.
1. [Maybe] remove 'ENDORSMENT' and 'CERTIFICATION' columns from 'teachers' table.

# Reports to make (.csv for each)
1. Number of teachers with each kind of certification.
1. For each type of CS certification, report each teacher with that certification + their school.

# Data tables and fields
All-caps fields come straight from dataset
## Teachers
- teacherID
- LAST_NAME
- FIRST_NAME
- HIRE_DT
- JOBCODE
- JOB_TITLE
- DEPTID
- DEPARTMENT

## Endorsements
- teacherID
- endorsement

## Certification
- teacherID
- certification
