import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import scipy.stats

def remove_all_nulls(WWC):
    WWC.drop(['iso_code', 'continent', 'total_cases', 'total_deaths', 'new_deaths_smoothed',
              'new_cases_smoothed_per_million', 'new_deaths_smoothed_per_million', 'icu_patients',
              'icu_patients_per_million', 'hosp_patients', 'hosp_patients_per_million', 'hosp_patients',
              'hosp_patients_per_million', 'weekly_icu_admissions', 'weekly_icu_admissions_per_million',
              'weekly_hosp_admissions', 'weekly_hosp_admissions_per_million', 'new_tests', 'total_tests',
              'new_tests_smoothed', 'new_tests_smoothed_per_thousand', 'tests_units', 'total_vaccinations',
              'total_vaccinations_per_hundred', 'aged_65_older', 'aged_70_older',
              'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers', 'male_smokers',
              'handwashing_facilities'], axis=1, inplace=True)

    return (WWC.dropna())

def series_30_relativity(WWC):
    for i in range(1, 31):
        s_death = 'new_death_' + str(i) + '_day_ago'
        s_cases = 'new_cases_' + str(i) + '_day_ago'
        WWC[s_death] = WWC[s_death] / WWC['Death_STATS_avg']
        WWC[s_cases] = WWC[s_cases] / WWC['Cases_STATS_avg']

def arrange_30_statistic(WWC):
    WWC['Cases_STATS_min'] = WWC['Cases_STATS_min']/ 1000000
    WWC['Cases_STATS_max'] = WWC['Cases_STATS_max'] / 1000000
    WWC['Cases_STATS_avg'] = WWC['Cases_STATS_avg'] / 1000000
    WWC['Cases_STATS_percentile_25'] = WWC['Cases_STATS_percentile_25'] / 1000000
    WWC['Cases_STATS_percentile_50'] = WWC['Cases_STATS_percentile_50'] / 1000000
    WWC['Cases_STATS_percentile_75'] = WWC['Cases_STATS_percentile_75'] / 1000000

    WWC['Death_STATS_min'] = WWC['Death_STATS_min'] / 1000000
    WWC['Death_STATS_max'] = WWC['Death_STATS_max'] / 1000000
    WWC['Death_STATS_avg'] = WWC['Death_STATS_avg'] / 1000000
    WWC['Death_STATS_percentile_25'] = WWC['Death_STATS_percentile_25'] / 1000000
    WWC['Death_STATS_percentile_50'] = WWC['Death_STATS_percentile_50'] / 1000000
    WWC['Death_STATS_percentile_75'] = WWC['Death_STATS_percentile_75'] / 1000000

def classify_columns_by_percintles(WWC, num_of_classes):
    col = ['col_name']
    for i in range(num_of_classes):
        col.append(str(i)+'_min')
        col.append(str(i) + '_max')
    df = pd.DataFrame(columns=col)


    part = (100/num_of_classes)/100
    for col in WWC.columns:
        if (col in ['location', 'date', 'more_new_cases']):
            continue
        # DELETE this------------------
        WWC[col][WWC[col] < 0] = 0
        # ------------------------------
        series = pd.Series(WWC[col])
        percentile_val = []
        for i in range(num_of_classes+1):
            percentile_val.append(series.quantile(i*part))

        new_row = [col]

        #print("Column name: " + col)
        for i in range(num_of_classes):
            #print("   Class number: " + str(i))
            #print("   Range: " +str(percentile_val[i]) + " - " + str(percentile_val[i+1]))
            new_row.append(str(percentile_val[i]))
            new_row.append(str(percentile_val[i+1]))
            WWC.loc[(WWC[col] >= percentile_val[i]) & (WWC[col] <= percentile_val[i+1]), col] = i -20

        df.loc[len(df)] = new_row

        WWC[col] += 20

    return df

def drop_irelevant_cols(WWC):
    WWC.drop(['Unnamed: 0', 'Unnamed: 0.1', 'new_cases', 'new_cases_smoothed', 'new_deaths',
                 'population', 'more_death'], axis=1, inplace=True)




if __name__ == '__main__':

    # WWC = pd.read_csv('WWC_data.csv')
    # WWC = remove_all_nulls(WWC)
    # series_30_relativity(WWC)
    # arrange_30_statistic(WWC)
    # # print(WWC.total_deaths.describe())
    # print('ARRANGE DATA DONE!')

    #------------------------------NO NULLS---------------------------------

    WWC_no_nulls = pd.read_csv('WWC_all_data_clean_09_01_2021_no_nulls.csv')
    drop_irelevant_cols(WWC_no_nulls)
    series_30_relativity(WWC_no_nulls)
    arrange_30_statistic(WWC_no_nulls)

    # ----------------- 4 classes -----------------
    WWC_no_nulls_4_classes = WWC_no_nulls.copy()
    df_4 = classify_columns_by_percintles(WWC_no_nulls_4_classes, 4)

    WWC_no_nulls_4_classes.to_csv('WWC_09_01_2021_no_nulls_4_classes.csv')
    df_4.to_csv('WWC_09_01_2021_no_nulls_4_classes_METADATA.csv')
    # ---------------------------------------------------

    # ----------------- 16 classes -----------------
    WWC_no_nulls_16_classes = WWC_no_nulls.copy()
    df_16 = classify_columns_by_percintles(WWC_no_nulls_16_classes, 16)

    WWC_no_nulls_16_classes.to_csv('WWC_09_01_2021_no_nulls_16_classes.csv')
    df_16.to_csv('WWC_09_01_2021_no_nulls_16_classes_METADATA.csv')
    # ---------------------------------------------------

    # ------------------------------FIX NULLS WITH AVERAGE ---------------------------------

    WWC_no_nulls_avg = pd.read_csv('WWC_all_data_clean_09_01_2021_replace_nulls_with_average.csv')
    drop_irelevant_cols(WWC_no_nulls_avg)
    series_30_relativity(WWC_no_nulls_avg)
    arrange_30_statistic(WWC_no_nulls_avg)

    # ----------------- 4 classes -----------------
    WWC_no_nulls_avg_4_classes = WWC_no_nulls_avg.copy()
    df_avg_4 = classify_columns_by_percintles(WWC_no_nulls_avg_4_classes, 4)

    WWC_no_nulls_avg_4_classes.to_csv('WWC_09_01_2021_no_nulls_AVG_4_classes.csv')
    df_avg_4.to_csv('WWC_09_01_2021_no_nulls_AVG_4_classes_METADATA.csv')
    # ---------------------------------------------------

    # ----------------- 8 classes -----------------
    WWC_no_nulls_avg_8_classes = WWC_no_nulls_avg.copy()
    df_avg_8 = classify_columns_by_percintles(WWC_no_nulls_avg_8_classes, 8)

    WWC_no_nulls_avg_8_classes.to_csv('WWC_09_01_2021_no_nulls_AVG_8_classes.csv')
    df_avg_8.to_csv('WWC_09_01_2021_no_nulls_AVG_8_classes_METADATA.csv')
    # ---------------------------------------------------

    # ----------------- 16 classes -----------------
    WWC_no_nulls_avg_16_classes = WWC_no_nulls_avg.copy()
    df_avg_16 = classify_columns_by_percintles(WWC_no_nulls_avg_16_classes, 16)

    WWC_no_nulls_avg_16_classes.to_csv('WWC_09_01_2021_no_nulls_16_classes.csv')
    df_avg_16.to_csv('WWC_09_01_2021_no_nulls_AVG_16_classes_METADATA.csv')
    # ---------------------------------------------------

    print('ARRANGE DATA DONE!')

