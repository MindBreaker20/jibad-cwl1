import pandas as pd
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

# wczytanie plików
power_plant_one_data = pd.read_csv('Plant_1_Generation_Data.csv')  # źródło: Kaggle
power_plant_two_data = pd.read_csv('Plant_2_Generation_Data.csv')

# utworzenie jednego dataframe
power_plant_one_data['DATE_TIME'] = pd.to_datetime(power_plant_one_data['DATE_TIME'], infer_datetime_format=True)
power_plant_two_data['DATE_TIME'] = pd.to_datetime(power_plant_two_data['DATE_TIME'], infer_datetime_format=True)
power_plants_data = pd.concat([power_plant_one_data, power_plant_two_data], ignore_index=True, sort=True)

power_plants_data = power_plants_data.drop(['PLANT_ID', 'DC_POWER', 'DAILY_YIELD', 'TOTAL_YIELD'], axis=1)

# odfiltrowanie brakujących danych
print(power_plants_data.isna().sum(axis=0))
power_plants_data['AC_POWER'] = power_plants_data['AC_POWER'].fillna(power_plants_data['AC_POWER'].mean())

# wykres AC_POWER dla wybranego generatora oraz średnie AC_POWER dla wszystkich generatorów w wybranym tygodniu
power_plants_weekly_data = power_plants_data.loc[(power_plants_data['DATE_TIME'] >= '2020-05-15') &
                                                 (power_plants_data['DATE_TIME'] < '2020-05-22')]

power_plants_weekly_data['AC_POWER_AVERAGE'] = power_plants_weekly_data.groupby('DATE_TIME')['AC_POWER'].transform('mean')

ax = power_plants_weekly_data[power_plants_weekly_data['SOURCE_KEY'] == 'bvBOhCH3iADSZry'].plot(x='DATE_TIME',
y=['AC_POWER', 'AC_POWER_AVERAGE'], kind='line', figsize=(12, 6), title='AC power generated by the inverter compared with average AC power')

ax.legend(['bvBOhCH3iADSZry', 'Average'])
ax.set_xlabel('DATE_TIME')
ax.set_ylabel('AC_POWER')
plt.show()

# szukanie przypadków, kiedy AC_POWER któregoś z generatorów było na poziomie < 80% średniej. Których generatorów najczęściej to dotyczy?
power_plants_weekly_data.loc[power_plants_weekly_data['AC_POWER'] < 0.8 * power_plants_weekly_data['AC_POWER_AVERAGE'], 'LESS_THAN_80_PERCENT'] = 1
power_plants_weekly_data.loc[power_plants_weekly_data['AC_POWER'] >= 0.8 * power_plants_weekly_data['AC_POWER_AVERAGE'], 'LESS_THAN_80_PERCENT'] = 0
power_plants_weekly_data['LESS_THAN_80_PERCENT'] = power_plants_weekly_data['LESS_THAN_80_PERCENT'].astype(int)

print(power_plants_weekly_data.loc[power_plants_weekly_data['LESS_THAN_80_PERCENT'] == 1, ['SOURCE_KEY']].value_counts().nlargest(1))
# najczęściej energię poniżej 80% średniej generowały generatory o identyfikatorze Quc1TzYxW2pYoWX