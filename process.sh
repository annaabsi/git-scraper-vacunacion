filename="vacunas_covid.csv"

sed -i "s/FEMENINO/0/;s/MASCULINO/1/;s/\((.*)\)//" $filename 
