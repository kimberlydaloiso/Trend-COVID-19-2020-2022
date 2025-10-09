import pandas as pd

# ===================== COVID19 =====================
df = pd.read_csv(r"C:\Users\temp2\Downloads\dpc-covid19-ita-regioni.csv")

df = df.drop(columns=[
    "stato", "codice_regione", "lat", "long", "codice_nuts_1",
    "codice_nuts_2", "tamponi_test_molecolare", "tamponi_test_antigenico_rapido",
    "totale_positivi_test_molecolare", "totale_positivi_test_antigenico_rapido",
    "note", "note_casi", "note_test", "ingressi_terapia_intensiva",
    "casi_da_screening", "casi_testati", "casi_da_sospetto_diagnostico"
])

df["data"] = pd.to_datetime(df["data"], errors="coerce")
df_covid = df[(df["data"] >= "2020-03-01") & (df["data"] <= "2022-12-31")].copy()

df_covid.loc[df_covid['denominazione_regione'] == 'P.A. Bolzano', 'denominazione_regione'] = 'Bolzano'
df_covid.loc[df_covid['denominazione_regione'] == 'P.A. Trento', 'denominazione_regione'] = 'Trento'
df_covid.loc[df_covid['denominazione_regione'] == "Valle d'Aosta / Vallée d'Aoste", 'denominazione_regione'] = "Valle d'Aosta"
df_covid.loc[df_covid['denominazione_regione'] == 'Friuli Venezia Giulia', 'denominazione_regione'] = 'Friuli-Venezia Giulia'

print("Database COVID19 pulito:")
print(df_covid)
df_covid.to_csv(r"C:\Users\temp2\Downloads\Covid_pulito.csv", index=False)

# ===================== POPOLAZIONE =====================
df_pop = pd.read_csv(r"C:\Users\temp2\Downloads\popolazione-istat-regione-range.csv")
df_pop = df_pop.drop(columns=[
    "codice_regione", "codice_nuts_1", "descrizione_nuts_1",
    "codice_nuts_2", "sigla_regione", "latitudine_regione",
    "longitudine_regione", "range_eta"
])
df_pop = df_pop.groupby("denominazione_regione")["totale_generale"].sum().reset_index()
df_pop = df_pop.rename(columns={"totale_generale": "popolazione"})

df_pop.loc[df_pop['denominazione_regione'] == 'Provincia Autonoma Bolzano / Bozen', 'denominazione_regione'] = 'Bolzano'
df_pop.loc[df_pop['denominazione_regione'] == 'Provincia Autonoma Trento', 'denominazione_regione'] = 'Trento'
df_pop.loc[df_pop['denominazione_regione'] == "Valle d'Aosta / Vallée d'Aoste", 'denominazione_regione'] = "Valle d'Aosta"
df_pop.loc[df_pop['denominazione_regione'] == 'Friuli Venezia Giulia', 'denominazione_regione'] = 'Friuli-Venezia Giulia'

print("Database popolazione per regione:")
print(df_pop)
df_pop.to_csv(r"C:\Users\temp2\Downloads\Popolazione.csv", index=False)

# ===================== VACCINAZIONI =====================
def raggruppa_vaccinazioni(file_csv, anno):
    df_v = pd.read_csv(file_csv)
    df_v["totale"] = df_v["d1"] + df_v["dpi"]
    df_v = df_v.groupby("reg")["totale"].sum().reset_index()
    df_v.rename(columns={"reg": "denominazione_regione",
                          "totale": f"totale_{anno}"}, inplace=True)
    return df_v

df_2020 = raggruppa_vaccinazioni(r"C:\Users\temp2\Downloads\Vaccinazioni2020.csv", 2020)
df_2021 = raggruppa_vaccinazioni(r"C:\Users\temp2\Downloads\Vaccinazioni2021.csv", 2021)
df_2022 = raggruppa_vaccinazioni(r"C:\Users\temp2\Downloads\Vaccinazioni2022.csv", 2022)

df_2020.loc[df_2020['denominazione_regione'] == 'Provincia Autonoma Bolzano / Bozen', 'denominazione_regione'] = 'Bolzano'
df_2020.loc[df_2020['denominazione_regione'] == 'Provincia Autonoma Trento', 'denominazione_regione'] = 'Trento'
df_2020.loc[df_2020['denominazione_regione'] == "Valle d'Aosta / Vallée d'Aoste", 'denominazione_regione'] = "Valle d'Aosta"
df_2020.loc[df_2020['denominazione_regione'] == 'Friuli Venezia Giulia', 'denominazione_regione'] = 'Friuli-Venezia Giulia'
df_2021.loc[df_2021['denominazione_regione'] == 'Provincia Autonoma Bolzano / Bozen', 'denominazione_regione'] = 'Bolzano'
df_2021.loc[df_2021['denominazione_regione'] == 'Provincia Autonoma Trento', 'denominazione_regione'] = 'Trento'
df_2021.loc[df_2021['denominazione_regione'] == "Valle d'Aosta / Vall├®e d'Aoste", 'denominazione_regione'] = "Valle d'Aosta"
df_2021.loc[df_2021['denominazione_regione'] == 'Friuli Venezia Giulia', 'denominazione_regione'] = 'Friuli-Venezia Giulia'
df_2022.loc[df_2022['denominazione_regione'] == 'Provincia Autonoma Bolzano / Bozen', 'denominazione_regione'] = 'Bolzano'
df_2022.loc[df_2022['denominazione_regione'] == 'Provincia Autonoma Trento', 'denominazione_regione'] = 'Trento'
df_2022.loc[df_2022['denominazione_regione'] == "Valle d'Aosta / Vall├®e d'Aoste", 'denominazione_regione'] = "Valle d'Aosta"
df_2022.loc[df_2022['denominazione_regione'] == 'Friuli Venezia Giulia', 'denominazione_regione'] = 'Friuli-Venezia Giulia'

print("Vaccinazioni 2020:")
print (df_2020)
print("Vaccinazioni 2021:")
print (df_2021)
print("Vaccinazioni 2022:")
print (df_2022)
df_2020.to_csv(r"C:\Users\temp2\Downloads\Vaccinazioni2020_pulito.csv", index=False)
df_2021.to_csv(r"C:\Users\temp2\Downloads\Vaccinazioni2021_pulito.csv", index=False)
df_2022.to_csv(r"C:\Users\temp2\Downloads\Vaccinazioni2022_pulito.csv", index=False)


# ===================== AGGREGAZIONE COVID PER ANNO =====================
df_covid_copy = df_covid.copy()
df_covid_copy.loc[:, "anno"] = df_covid_copy["data"].dt.year

df_covid_agg = (
    df_covid_copy.sort_values("data")
    .groupby(["denominazione_regione", "anno"])
    .last()
    .reset_index()
)

if "data" in df_covid_agg.columns:
    df_covid_agg = df_covid_agg.drop(columns=["data"])

print("Database covid aggregato:")
print (df_covid_agg)

df_covid_agg.to_csv(r"C:\Users\temp2\Downloads\covid_agg.csv", index=False)


# ===================== INDICATORI =====================

# DECEDUTI

df_deceduti_pivot = df_covid_agg.pivot(
    index="denominazione_regione",
    columns="anno",
    values="deceduti"
).reset_index().rename(columns={2020: "deceduti_2020", 2021: "deceduti_2021", 2022: "deceduti_2022"})
df_deceduti_pivot["deceduti_totale"] = df_deceduti_pivot[["deceduti_2020","deceduti_2021","deceduti_2022"]].fillna(0).max(axis=1).astype(int)

df_deceduti_pivot.loc[df_deceduti_pivot['denominazione_regione'] == 'P.A. Bolzano', 'denominazione_regione'] = 'Bolzano'
df_deceduti_pivot.loc[df_deceduti_pivot['denominazione_regione'] == 'P.A. Trento', 'denominazione_regione'] = 'Trento'
df_deceduti_pivot.loc[df_deceduti_pivot['denominazione_regione'] == 'Friuli Venezia Giulia', 'denominazione_regione'] = 'Friuli-Venezia Giulia'

print("Database deceduti per regione:")
print (df_deceduti_pivot)
df_deceduti_pivot.to_csv(r"C:\Users\temp2\Downloads\deceduti_pivot.csv", index=False)

# GUARITI

df_guariti_pivot = df_covid_agg.pivot(
    index="denominazione_regione",
    columns="anno",
    values="dimessi_guariti"
).reset_index().rename(columns={2020: "guariti_2020", 2021: "guariti_2021", 2022: "guariti_2022"})
df_guariti_pivot["guariti_totale"] = df_guariti_pivot[["guariti_2020","guariti_2021","guariti_2022"]].fillna(0).max(axis=1).astype(int)


df_guariti_pivot.loc[df_guariti_pivot['denominazione_regione'] == 'P.A. Bolzano', 'denominazione_regione'] = 'Bolzano'
df_guariti_pivot.loc[df_guariti_pivot['denominazione_regione'] == 'P.A. Trento', 'denominazione_regione'] = 'Trento'
df_guariti_pivot.loc[df_guariti_pivot['denominazione_regione'] == 'Friuli Venezia Giulia', 'denominazione_regione'] = 'Friuli-Venezia Giulia'

print("Database dimessi guariti per regione:")
print (df_guariti_pivot)
df_guariti_pivot.to_csv(r"C:\Users\temp2\Downloads\guariti_pivot.csv", index=False)

# ===================== TOTALE VACCINATI =====================

df_vaccinazioni = pd.merge(df_2020, df_2021, on='denominazione_regione', how='outer')
df_vaccinazioni = pd.merge(df_vaccinazioni, df_2022, on='denominazione_regione', how='outer')

df_vaccinazioni["vaccinati_totale"] = df_vaccinazioni["totale_2020"] + df_vaccinazioni["totale_2021"] + df_vaccinazioni["totale_2022"]

df_vaccinazioni = df_vaccinazioni.rename(columns={
    "totale_2020": "vaccinati_2020",
    "totale_2021": "vaccinati_2021",
    "totale_2022": "vaccinati_2022"
})

print("\nTotale vaccinati per regione:")
print(df_vaccinazioni)

df_vaccinazioni.to_csv(r"C:\Users\temp2\Downloads\vaccinazioni tot.csv", index=False)


# ===================== MERGE COMPLETO =====================
df_completo = df_pop.merge(df_deceduti_pivot, on="denominazione_regione", how="left") \
                     .merge(df_guariti_pivot, on="denominazione_regione", how="left") \
                     .merge(df_vaccinazioni, on="denominazione_regione", how="left") \

cols_int = df_completo.select_dtypes(include=["float", "int"]).columns
df_completo[cols_int] = df_completo[cols_int].fillna(0).astype(int)

df_completo = df_completo.rename(columns={
    "totale_2020": "vaccinati_2020",
    "totale_2021": "vaccinati_2021",
    "totale_2022": "vaccinati_2022"
})

print("Dataset completo per regione:")
print(df_completo)

df_completo.to_csv(r"C:\Users\temp2\Downloads\dataset_completo.csv", index=False)

# ===================== ANDAMENTO VACCINATI =====================

file_path = "C:\\Users\\temp2\\.ipython\\covid_pulito.csv"
df = pd.read_csv(file_path)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

df['data'] = pd.to_datetime(df['data'], errors='coerce')  # forza NaT se formato non valido
df = df.dropna(subset=['data'])

df_aggr = (
    df.groupby(['data', 'denominazione_regione'], as_index=False)['totale_positivi']
    .sum()
    .sort_values('data')
)

# Creazione intervallo settimanale
date7g = pd.date_range(df_aggr['data'].min(), df_aggr['data'].max(), freq='7D')
df_aggr_filt = df_aggr[df_aggr['data'].isin(date7g)]

df_aggr_filt.to_csv('IndicatorePositivi7giorni.csv', index=False)

# ===================== ANDAMENTO VACCINAZIONI =====================

vaccinazioni2020 = pd.read_csv(r'C:\Users\temp2\Downloads\Vaccinazioni2020.csv')
vaccinazioni2021 = pd.read_csv(r'C:\Users\temp2\Downloads\Vaccinazioni2021.csv')
vaccinazioni2022 = pd.read_csv(r'C:\Users\temp2\Downloads\Vaccinazioni2022.csv')

vaccinazioni2020['Totale Vaccinazioni'] = vaccinazioni2020['d1'] + vaccinazioni2020['dpi']
vaccinazioni2021['Totale Vaccinazioni'] = vaccinazioni2021['d1'] + vaccinazioni2021['dpi']
vaccinazioni2022['Totale Vaccinazioni'] = vaccinazioni2022['d1'] + vaccinazioni2022['dpi']

df_vaccperdata = pd.concat([vaccinazioni2020, vaccinazioni2021, vaccinazioni2022])

df_vaccperdata.rename(columns={'reg': 'denominazione_regione'}, inplace=True)

df_vaccperdata.loc[df_vaccperdata['denominazione_regione'] == 'Provincia Autonoma Bolzano / Bozen', 'denominazione_regione'] = 'P.A. Bolzano'
df_vaccperdata.loc[df_vaccperdata['denominazione_regione'] == "Provincia Autonoma Trento" , 'denominazione_regione']= "P.A. Trento"
df_vaccperdata.loc[df_vaccperdata['denominazione_regione'] == "Valle d'Aosta / Vallée d'Aoste" , 'denominazione_regione']= "Valle d'Aosta"
df_vaccperdata.loc[df_vaccperdata['denominazione_regione'] == "Friuli-Venezia Giulia", 'denominazione_regione'] = "Friuli Venezia Giulia"


df_vaccperdata.to_csv(r'C:\Users\temp2\Downloads\IndicatoriVaccinazioniPerData.csv')
print("Indicatori vaccinazioni per data:")
print (df_vaccperdata)

df = pd.read_csv(r'C:\Users\temp2\Downloads\IndicatoriVaccinazioniPerData.csv')

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
df['data'] = pd.to_datetime(df['data'], dayfirst=True)

df = df.groupby(['data','denominazione_regione'])['Totale Vaccinazioni'].sum().reset_index()
df = df.sort_values(by='data')


prima_data = df['data'].min() #'27/12/2020'
ultima_data = df['data'].max() #'31/12/2022'

# Creo una lista di date suddivise in 7 giorni
date7g = pd.date_range(start=prima_data, end=ultima_data, freq='7D')

df_aggr_filt = df[df['data'].isin(date7g)]

df_aggr_filt.to_csv(r'C:\Users\temp2\Downloads\IndicatoriVaccinazioniPerData7g.csv')
print ('Indicatori vaccinazioni per settimana:')
print (df_aggr_filt)

