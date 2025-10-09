import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- DECEDUTI (Grafico a Barre Raggruppate) ---
print("Generazione Grafico Deceduti...")
file_deceduti = r'C:\Users\temp2\Downloads\deceduti_pivot.csv'
df_deceduti = pd.read_csv(file_deceduti).set_index('denominazione_regione')
df_deceduti = df_deceduti.loc[:, ~df_deceduti.columns.str.contains('^Unnamed')]
df_deceduti.columns = ['2020', '2021', '2022','totale_deceduti']

df_deceduti.plot(kind='bar', figsize=(15, 8), width=0.8)
plt.title('Decessi per Regione (2020-2022)', fontsize=16, fontweight='bold')
plt.xlabel('Regione', fontsize=12)
plt.ylabel('Numero di Deceduti', fontsize=12)
plt.xticks(rotation=90, ha='right', fontsize=10)
plt.legend(title='Anno')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --- GUARITI (Grafico a Barre in Pila) ---
print("Generazione grafico Dimessi Guariti...")
file_guariti = r'C:\Users\temp2\Downloads\guariti_pivot.csv'
df_guariti = pd.read_csv(file_guariti).set_index('denominazione_regione')
df_guariti = df_guariti.loc[:, ~df_guariti.columns.str.contains('^Unnamed')]

df_guariti.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
plt.title('Dimessi Guariti per Regione (2020-2022)', fontsize=16, fontweight='bold')
plt.xlabel('Regioni', fontsize=12)
plt.ylabel('Numero di Dimessi Guariti', fontsize=12)
plt.xticks(rotation=90, ha='right', fontsize=10)
plt.legend(title='Dimessi Guariti', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --- VACCINAZIONI (Grafico a Linee Multiple) ---
print("Generazione Grafico Vaccinazioni...")

df_vaccinazioni = pd.read_csv(r'C:\Users\temp2\Downloads\vaccinazioni tot.csv', index_col='denominazione_regione')
df_vaccinazioni = df_vaccinazioni.drop(columns=['vaccinati_totale'])
df_vaccinazioni.columns = [col.split('_')[1] for col in df_vaccinazioni.columns]
df_vaccinazioni_T = df_vaccinazioni.T

print(df_vaccinazioni_T)

df_vaccinazioni_T.plot(kind='line', figsize=(12, 8))

plt.title('Vaccinazioni COVID-19 per Regione e Anno', fontsize=16)
plt.xlabel('Anno', fontsize=12)
plt.ylabel('Numero di Vaccinazioni', fontsize=12)
plt.xticks(rotation=0)
plt.legend(title='Regione', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

# --- ANDAMENTO POSITIVI (Grafico a Linee Multiple) ---
print("Generazione Grafico Andamento Positivi 7 giorni...")
file_positivi = r'C:\Users\temp2\Downloads\covid_pulito.csv'
df_positivi = pd.read_csv(file_positivi)
df_positivi = df_positivi.loc[:, ~df_positivi.columns.str.contains('^Unnamed')]
df_positivi['data'] = pd.to_datetime(df_positivi['data'], dayfirst=True, errors='coerce')
df_positivi = df_positivi.dropna(subset=['data'])
df_positivi['settimana'] = df_positivi['data'].dt.to_period('W-Mon')
df_aggr_positivi = df_positivi.groupby(['settimana', 'denominazione_regione'])['totale_positivi'].sum().reset_index()
pivot_positivi = df_aggr_positivi.pivot(index='settimana', columns='denominazione_regione', values='totale_positivi')

pivot_positivi.plot(kind='line', figsize=(15, 8))
plt.title('Andamento casi positivi per regione (per settimana)', fontsize=16)
plt.xlabel('Data (settimanale)', fontsize=12)
plt.ylabel('Totale casi positivi', fontsize=12)
plt.legend(title='Regione', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# --- 5. ANDAMENTO VACCINAZIONI (Grafico a Linee Multiple) ---
print("Generazione Grafico Andamento Vaccinazioni 7 giorni...")
file_path = r'C:\Users\temp2\Downloads\IndicatoriVaccinazioniPerData7g.csv'
df_vacc7g = pd.read_csv(file_path)
df_vacc7g['data'] = pd.to_datetime(df_vacc7g['data'], dayfirst=True)
df_vacc7g = df_vacc7g.sort_values(by=['data', 'denominazione_regione'])

pivot_vacc7g = df_vacc7g.pivot(index='data', columns='denominazione_regione', values='Totale Vaccinazioni')

pivot_vacc7g.plot(kind='line', figsize=(15, 8))
plt.title('Andamento delle vaccinazioni per regione (settimanale)', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Totale vaccinazioni', fontsize=12)
plt.legend(title='Regione', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()