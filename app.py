import pandas as pd
import sqlite3
connexion = sqlite3.connect("kbo_database.db")
cursor = connexion.cursor()
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table';
""")
df_tables = pd.DataFrame(cursor.fetchall(), columns=["Tables Name"],index=[1,2,3,4,5,6,7,8,9])
print("Name of tables in database:")
print(df_tables)
print("____________________________________________________________")
print("TOP 10 NACE CODE WITH MAXIMUM NO OF COMPANIES")
cursor.execute("""
    SELECT NaceCode , COUNT(enterprise.EnterpriseNumber) AS Count_enterprise, ROUND(AVG(strftime('%Y', 'now') - strftime('%Y', enterprise.StartDate)),2) AS AvgAge
    FROM activity
    INNER JOIN enterprise
    ON enterprise.EnterpriseNumber= activity.EntityNumber
    GROUP BY NaceCode
    ORDER BY COUNT(enterprise.EnterpriseNumber) DESC
    LIMIT 10;
""")
top10nacecode= pd.DataFrame(cursor.fetchall(), columns=["nacecode","noofcompanies","avgage"])
print(top10nacecode)
Nacecodes=top10nacecode["nacecode"].tolist()
print(Nacecodes)

print("____________________________________________________________")
print("Compare geographical distribution of companies")
cursor.execute("""
    SELECT MunicipalityNL, COUNT(EntityNumber)
    FROM address
    GROUP BY MunicipalityNL
    ORDER BY COUNT(EntityNumber) DESC
    LIMIT 10;
""")
regionwise= pd.DataFrame(cursor.fetchall(), columns=["MunicipalityNL","noofcompanies"])
print(regionwise)

nacecodedesc=["Support","Consulting","PR","Training","Carpentry","Electrical","Landscaping","Hospital","Advertising","IT"]
nace_dict = dict(zip(Nacecodes, nacecodedesc))
companies_dict={}
for i,j in nace_dict.items():
    print("____________________________________________________________")
    print(f"REGIONAL PRESENCE OF COMPANIES WITH NACE CODE {i} :{j}")
    
    cursor.execute("""
        SELECT MunicipalityNL, Zipcode, COUNT(address.EntityNumber) AS CompanyCount
        FROM address
        INNER JOIN activity
        ON activity.EntityNumber = address.EntityNumber
        WHERE activity.NaceCode = ?
        GROUP BY MunicipalityNL, Zipcode
        ORDER BY CompanyCount DESC
        LIMIT 10;
    """, (i,))
    
    df = pd.DataFrame(cursor.fetchall(), columns=["MunicipalityNL", "Zipcode", "noofcompanies"])
    companies_dict[j]=df
    print(companies_dict[j])
print("____________________________________________________________")  
   