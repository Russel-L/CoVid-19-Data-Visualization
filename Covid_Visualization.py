import csv
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

open('covid.db', 'w').close()
db = sqlite3.connect('covid.db')
cursor = db.cursor()
# Create table
cursor.execute(
    '''CREATE TABLE CovidCases (
		CaseCode TEXT, Age INT, AgeGroup TEXT, Sex TEXT, DateSpecimen DATE, DateResultRelease DATE, 
		DateRepConf DATE, DateDied DATE, DateRecover DATE, RemovalType TEXT, Admitted TEXT, 
		RegionRes TEXT, ProvRes TEXT, CityMunRes TEXT, CityMuniPSGC TEXT, BarangayRes TEXT, 
		BarangayPSGC TEXT, HealthStatus TEXT, Quarantined TEXT, DateOnset DATE, Pregnanttab TEXT,
		ValidationStatus TEXT)''')

csvfile = input("Input csv file: ")
with open(csvfile) as file:
    # Create DictReader
    reader = csv.DictReader(file)

    # Iterate over the CSV file
    for row in reader:
        # Insert case record
        sql = '''INSERT INTO CovidCases (CaseCode, Age, AgeGroup, Sex, DateSpecimen, DateResultRelease, 
		DateRepConf, DateDied, DateRecover, RemovalType, Admitted, RegionRes, ProvRes, CityMunRes,
		CityMuniPSGC, BarangayRes, BarangayPSGC, HealthStatus, Quarantined, DateOnset, Pregnanttab,
		ValidationStatus) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        caseData = (row['CaseCode'], row['Age'], row['AgeGroup'], row['Sex'], row['DateSpecimen'],
                    row['DateResultRelease'], row['DateRepConf'], row['DateDied'], row['DateRecover'],
                    row['RemovalType'], row['Admitted'], row['RegionRes'], row['ProvRes'], row['CityMunRes'],
                    row['CityMuniPSGC'], row['BarangayRes'], row['BarangayPSGC'], row['HealthStatus'],
                    row['Quarantined'], row['DateOnset'], row['Pregnanttab'], row['ValidationStatus'])
        cursor.execute(sql, caseData)
db.commit()
region = input("Input region: ")
print("Input 1 for number of positive cases")
print("Input 2 for number of active cases")
print("Input 3 for number of positive cases by sex")
print("Input 4 for number of positive cases by each age group")
print("Input 5 for number of positive cases by the health status")
print("Input 6 for number of deaths by sex")
print("Input 7 for number of deaths by each age group")
print("Input 8 for number of asymptomatic cases")
graph = input("Input number of data to be visualized: ")
if graph == '1':
    if region == 'NCR':
        # Total NCR cases each city
        ncrsql = '''SELECT CityMunRes, COUNT(CaseCode) FROM CovidCases 
			    WHERE RegionRes = 'NCR' GROUP BY CityMunRes'''
        data1 = cursor.execute(ncrsql).fetchall()
        title = f"Number of Positive Cases for Each City and Pateros in NCR"
        sns.set_style('whitegrid')
        cit = []
        freq = []
        for cities, poscases2 in data1:
            cit.append(cities)
            freq.append(poscases2)
        if cit[0] == '':
            cit[0] = 'UNKNOWN'
        sns.set(font_scale=0.8)
        axes = sns.barplot(x=freq, y=cit, palette='pastel', orient='h')
        axes.set_title(title, size=20)
        axes.set_xlim(right=max(freq) * 1.10)
        for bar, frequency in zip(axes.patches, freq):
            text_y = bar.get_y() + bar.get_height() / 2.0
            text_x = bar.get_width()
            text = f'{frequency:,}'
            axes.text(text_x, text_y, text,
                      fontsize=11, ha='right', va='center')
    else:
        # Total Region cases each province
        provsql = f'''SELECT ProvRes, COUNT(CaseCode) FROM CovidCases 
			WHERE RegionRes = '{region}' GROUP BY ProvRes'''
        data2 = cursor.execute(provsql).fetchall()
        title = f"Number of Positive Cases for Each Province in {region}"
        sns.set_style('whitegrid')
        prov = []
        freq = []
        for provi, poscase in data2:
            prov.append(provi)
            freq.append(poscase)
        if prov[0] == '':
            prov[0] = 'UNKNOWN'
        sns.set(font_scale=1)
        axes = sns.barplot(x=prov, y=freq, palette='bright')
        axes.set_title(title, size=18)
        axes.set(xlabel='Provinces')
        axes.set_ylim(top=max(freq) * 1.10)
        for bar, frequency in zip(axes.patches, freq):
            text_x = bar.get_x() + bar.get_width() / 2.0
            text_y = bar.get_height()
            text = f'{frequency:,}'
            axes.text(text_x, text_y, text,
                      fontsize=11, ha='center', va='bottom')
if graph == '2':
    if region == 'NCR':
        # Total active ncr cases each city
        ncrsql1 = '''SELECT DISTINCT CityMunRes, RemovalType, COUNT(RemovalType) FROM CovidCases 
			WHERE RegionRes = 'NCR' GROUP BY RemovalType, CityMunRes'''
        data3 = cursor.execute(ncrsql1).fetchall()
        title = f"Number of Active Cases for Each City and Pateros in NCR"
        sns.set_style('whitegrid')
        cit = []
        freq = []
        for cities, rem, count1 in data3:
            if not rem:
                cit.append(cities)
                freq.append(count1)
            if cit[0] == '':
                cit[0] = 'UNKNOWN'
        sns.set(font_scale=0.8)
        axes = sns.barplot(x=freq, y=cit, palette='pastel', orient='h')
        axes.set_title(title, size=20)
        axes.set_xlim(right=max(freq) * 1.10)
        for bar, frequency in zip(axes.patches, freq):
            text_y = bar.get_y() + bar.get_height() / 2.0
            text_x = bar.get_width()
            text = f'{frequency:,}'
            axes.text(text_x, text_y, text,
                      fontsize=11, ha='right', va='center')
    else:
        # Total region cases each province
        provsql1 = f'''SELECT DISTINCT ProvRes, RemovalType, COUNT(RemovalType) FROM CovidCases 
			WHERE RegionRes = '{region}' GROUP BY RemovalType, ProvRes'''
        data4 = cursor.execute(provsql1).fetchall()
        title = f"Number of Active Cases for Each Province in {region}"
        sns.set_style('whitegrid')
        prov = []
        freq = []
        for provi, rem, count2 in data4:
            if not rem:
                prov.append(provi)
                freq.append(count2)
        if prov[0] == '':
            prov[0] = 'UNKNOWN'
        axes = sns.barplot(x=prov, y=freq, palette='bright')
        axes.set_title(title, size=18)
        axes.set(xlabel='Provinces')
        axes.set_ylim(top=max(freq) * 1.10)
        for bar, frequency in zip(axes.patches, freq):
            text_x = bar.get_x() + bar.get_width() / 2.0
            text_y = bar.get_height()
            text = f'{frequency:,}'
            axes.text(text_x, text_y, text,
                      fontsize=11, ha='center', va='bottom')
if graph == '3':
    # Cases each sex
    sexsql = f'''SELECT DISTINCT Sex, COUNT(Sex) FROM CovidCases WHERE RegionRes = '{region}' 
	    	GROUP BY Sex, RegionRes'''
    data5 = cursor.execute(sexsql).fetchall()
    label = []
    freq = []
    for sex3, count5 in data5:
        freq.append(count5)
        freq1 = str(count5)
        label.append(f'{sex3} : {freq1}')
    fig1, ax1 = plt.subplots()
    wedges, texts, autotexts = ax1.pie(freq, autopct='%1.2f%%',
                                       textprops=dict(color="w"))
    title = f'Number of Positive Cases by Sex in {region}'
    ax1.set_title(title, size=18)
    ax1.legend(wedges, label,
               title="Sex",
               loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=11, weight="bold")
if graph == '4':
    # Cases each age group
    agegrpsql = f'''SELECT DISTINCT AgeGroup, COUNT(AgeGroup) FROM CovidCases 
		WHERE RegionRes = '{region}' GROUP BY AgeGroup, RegionRes 
		ORDER BY length(AgeGroup), AgeGroup ASC'''
    data6 = cursor.execute(agegrpsql).fetchall()
    title = f"Number of Positive Cases by Each Age Group in {region}"
    sns.set_style('whitegrid')
    label = []
    freq = []
    for agegrop, posc2 in data6:
        label.append(agegrop)
        freq.append(posc2)
    if label[0] == '':
        label[0] = "UNKNOWN"
    axes = sns.barplot(x=label, y=freq, palette='bright')
    axes.set_title(title, size=17)
    axes.set(xlabel='Age Group')
    axes.set_ylim(top=max(freq) * 1.10)
    for bar, frequency in zip(axes.patches, freq):
        text_x = bar.get_x() + bar.get_width() / 2.0
        text_y = bar.get_height()
        text = f'{frequency:,}'
        axes.text(text_x, text_y, text,
                  fontsize=11, ha='center', va='bottom')
if graph == '5':
    # cases each health status
    statussql = f'''SELECT DISTINCT HealthStatus, COUNT(HealthStatus) FROM CovidCases 
		WHERE RegionRes = '{region}' GROUP BY HealthStatus, RegionRes'''
    data7 = cursor.execute(statussql).fetchall()
    title = f"Number of Positive Cases by the Health Status in {region}"
    sns.set_style('whitegrid')
    label = []
    freq = []
    for hstat, posc1 in data7:
        label.append(hstat)
        freq.append(posc1)
    if label[0] is None:
        label[0] = 'UNKNOWN'
    axes = sns.barplot(x=label, y=freq, palette='bright')
    axes.set_title(title, size=16)
    axes.set(xlabel='Health Status')
    axes.set_ylim(top=max(freq) * 1.10)
    for bar, frequency in zip(axes.patches, freq):
        text_x = bar.get_x() + bar.get_width() / 2.0
        text_y = bar.get_height()
        text = f'{frequency:,}'
        axes.text(text_x, text_y, text,
                  fontsize=11, ha='center', va='bottom')
if graph == '6':
    # deaths per sex
    dsexsql = f'''SELECT DISTINCT Sex, COUNT(Sex) FROM CovidCases 
    WHERE RegionRes = '{region}' AND HealthStatus = 'DIED' GROUP BY HealthStatus, Sex, RegionRes'''
    data8 = cursor.execute(dsexsql).fetchall()
    label = []
    freq = []
    for sex2, count4 in data8:
        freq.append(count4)
        freq1 = str(count4)
        label.append(f'{sex2} : {freq1}')
    fig1, ax1 = plt.subplots()

    wedges, texts, autotexts = ax1.pie(freq, autopct='%1.2f%%',
                                       textprops=dict(color="w"))
    title = f'Number of Deaths by Sex in {region}'
    ax1.set_title(title, size=20)
    ax1.legend(wedges, label,
               title="Sex",
               loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=11, weight="bold")
if graph == '7':
    # deaths per age group
    dagesql = f'''SELECT DISTINCT AgeGroup, COUNT(AgeGroup), HealthStatus 
		FROM CovidCases WHERE RegionRes = '{region}' GROUP BY HealthStatus, AgeGroup, RegionRes 
		ORDER BY length(AgeGroup), AgeGroup ASC'''
    data9 = cursor.execute(dagesql).fetchall()
    title = f"Number of Deaths by Each Age Group in {region}"
    sns.set_style('whitegrid')
    label = []
    freq = []
    for agegrop1, posc3, hstat1 in data9:
        if hstat1 == 'DIED':
            label.append(agegrop1)
            freq.append(posc3)
    if label[0] == '':
        label[0] = "UNKNOWN"
    axes = sns.barplot(x=label, y=freq, palette='bright')
    axes.set_title(title, size=17)
    axes.set(xlabel='Age Group')
    axes.set_ylim(top=max(freq) * 1.10)
    for bar, frequency in zip(axes.patches, freq):
        text_x = bar.get_x() + bar.get_width() / 2.0
        text_y = bar.get_height()
        text = f'{frequency:,}'
        axes.text(text_x, text_y, text,
                  fontsize=11, ha='center', va='bottom')
if graph == '8':
    if region == 'NCR':
        # asymptomatic cases per city
        asympsql2 = f'''SELECT DISTINCT CityMunRes, COUNT(HealthStatus) FROM CovidCases
    	    WHERE RegionRes = 'NCR' AND HealthStatus = 'ASYMPTOMATIC' GROUP BY HealthStatus, CityMunRes'''
        data11 = cursor.execute(asympsql2).fetchall()
        title = f"Number of Asymptomatic Cases for Each City and Pateros in NCR"
        sns.set_style('whitegrid')
        cit = []
        freq = []
        for cities1, posc6 in data11:
            cit.append(cities1)
            freq.append(posc6)
        if cit[0] == '':
            cit[0] = 'UNKNOWN'
        sns.set(font_scale=0.8)
        axes = sns.barplot(x=freq, y=cit, palette='pastel', orient='h')
        axes.set_title(title, size=16)
        axes.set_xlim(right=max(freq) * 1.10)
        for bar, frequency in zip(axes.patches, freq):
            text_y = bar.get_y() + bar.get_height() / 2.0
            text_x = bar.get_width()
            text = f'{frequency:,}'
            axes.text(text_x, text_y, text,
                      fontsize=11, ha='right', va='center')
    else:
        # asymptomatic cases per province
        asympsql1 = f'''SELECT DISTINCT ProvRes, COUNT(HealthStatus) FROM CovidCases 
            WHERE RegionRes = '{region}' and HealthStatus = 'ASYMPTOMATIC' 
            GROUP BY HealthStatus, ProvRes'''
        data10 = cursor.execute(asympsql1).fetchall()
        title = f"Number of Asymptomatic Cases for Each Province in {region}"
        sns.set_style('whitegrid')
        prov = []
        freq = []
        for provi, posc4 in data10:
            prov.append(provi)
            freq.append(posc4)
        if prov[0] == '':
            prov[0] = 'UNKNOWN'
        axes = sns.barplot(x=prov, y=freq, palette='bright')
        axes.set_title(title, size=16)
        axes.set(xlabel='Provinces')
        axes.set_ylim(top=max(freq) * 1.10)
        for bar, frequency in zip(axes.patches, freq):
            text_x = bar.get_x() + bar.get_width() / 2.0
            text_y = bar.get_height()
            text = f'{frequency:,}'
            axes.text(text_x, text_y, text,
                      fontsize=11, ha='center', va='bottom')

plt.show()
cursor.close()
