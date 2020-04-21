import pandas as pd
import random as r
import altair as alt
import numpy as np
import math
from sklearn import linear_model, preprocessing, model_selection
from CountersForDnR import deathCounter, recoverCounter
import datetime


def expoIncrease(predict_df, forecast_set):
    # Prediction function focusing on expected exponential growth
    last_date = "2020-04-17"
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    index = 87
    diff = (predict_df.loc[index - 1][1] - forecast_set[0]) * 1.05
    mult = 1.0

    for i in forecast_set:
        if (i <= 0):
            i = 0
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        mult *= 1.03
        val = mult * (i + diff)
        if (val <= 0):
            val = 0
        predict_df.loc[index] = [str(next_date)] + [val]
        index += 1

    return predict_df


def continueTrend(predict_df, forecast_set):
    # Prediction function focusing on maintaining current rate
    last_date = "2020-04-17"
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    index = 87
    diff = (predict_df.loc[index - 1][1] - forecast_set[0]) * 1.05
    mult = 1.0

    for i in forecast_set:
        if (i <= 0):
            i = 0
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        mult *= 1
        val = mult * (i + diff)
        if (val <= 0):
            val = 0
        predict_df.loc[index] = [str(next_date)] + [val]
        index += 1

    return predict_df


def levelOff(predict_df, forecast_set):
    # prediction function focusing on levelling off growth rate slowly
    last_date = "2020-04-17"
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    index = 87
    diff = (predict_df.loc[index - 1][1] - forecast_set[0]) * 1.05
    mult = 1.0

    for i in forecast_set:
        if (i <= 0):
            i = 0
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        mult *= 0.988
        val = mult * (i + diff)
        if (val <= 0):
            val = 0
        predict_df.loc[index] = [str(next_date)] + [val]
        index += 1

    return predict_df


def chart_canada(worst_df, norm_df, best_df):
    # charts data using altair with the input predict_df
    trimmed_worst = worst_df.loc[50:]
    trimmed_worst.columns = ['Date', 'Worst']
    trimmed_norm = norm_df.loc[50:]
    trimmed_norm.columns = ['Date', 'Norm']
    trimmed_best = best_df.loc[50:]
    trimmed_best.columns = ['Date', 'Best']

    trimmed_total = trimmed_worst.merge(trimmed_norm, on='Date')
    trimmed_total = trimmed_total.merge(trimmed_best, on='Date')
    # print(trimmed_total.tail(31))

    # chart entire prediction
    chart_full = alt.Chart(trimmed_total).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y='Active Cases:Q',
        color='Curve:N'
    ).properties(
        title='Canada - Predicted Amount of Active Cases for the Next Month'
    ).interactive()

    chart_full.show()
    chart_full.save("JSON_charts/CAN/CAN_Full_Chart.json")

    # trim dataframes for individual predicted weeks
    trimmed_week_1 = trimmed_total.loc[37:43]
    trimmed_week_2 = trimmed_total.loc[44:50]
    trimmed_week_3 = trimmed_total.loc[51:57]
    trimmed_week_4 = trimmed_total.loc[58:64]

    chart_1 = alt.Chart(trimmed_week_1).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Canada - Predicted Amount of Active Cases for Week 1 of Next Month'
    ).interactive()

    chart_1.show()
    chart_1.save("JSON_charts/CAN/CAN_Week_1_Chart.json")

    chart_2 = alt.Chart(trimmed_week_2).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Canada - Predicted Amount of Active Cases for Week 2 of Next Month'
    ).interactive()

    chart_2.show()
    chart_2.save("JSON_charts/CAN/CAN_Week_2_Chart.json")

    chart_3 = alt.Chart(trimmed_week_3).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Canada - Predicted Amount of Active Cases for Week 3 of Next Month'
    ).interactive()

    chart_3.show()
    chart_3.save("JSON_charts/CAN/CAN_Week_3_Chart.json")

    chart_4 = alt.Chart(trimmed_week_4).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Canada - Predicted Amount of Active Cases for Week 4 of Next Month'
    ).interactive()

    chart_4.show()
    chart_4.save("JSON_charts/CAN/CAN_Week_4_Chart.json")


def chart_korea(worst_df, norm_df, best_df):
    # charts data using altair with the input predict_df
    trimmed_worst = worst_df.loc[50:]
    trimmed_worst.columns = ['Date', 'Worst']
    trimmed_norm = norm_df.loc[50:]
    trimmed_norm.columns = ['Date', 'Norm']
    trimmed_best = best_df.loc[50:]
    trimmed_best.columns = ['Date', 'Best']

    trimmed_total = trimmed_worst.merge(trimmed_norm, on='Date')
    trimmed_total = trimmed_total.merge(trimmed_best, on='Date')
    # print(trimmed_total.tail(31))

    # chart entire prediction
    chart_full = alt.Chart(trimmed_total).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y='Active Cases:Q',
        color='Curve:N'
    ).properties(
        title='Korea - Predicted Amount of Active Cases for the Next Month'
    ).interactive()

    chart_full.show()
    chart_full.save("JSON_charts/KOR/KOR_Full_Chart.json")

    # trim dataframes for individual predicted weeks
    trimmed_week_1 = trimmed_total.loc[37:43]
    trimmed_week_2 = trimmed_total.loc[44:50]
    trimmed_week_3 = trimmed_total.loc[51:57]
    trimmed_week_4 = trimmed_total.loc[58:64]

    chart_1 = alt.Chart(trimmed_week_1).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Korea - Predicted Amount of Active Cases for Week 1 of Next Month'
    ).interactive()

    chart_1.show()
    chart_1.save("JSON_charts/KOR/KOR_Week_1_Chart.json")

    chart_2 = alt.Chart(trimmed_week_2).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Korea - Predicted Amount of Active Cases for Week 2 of Next Month'
    ).interactive()

    chart_2.show()
    chart_2.save("JSON_charts/KOR/KOR_Week_2_Chart.json")

    chart_3 = alt.Chart(trimmed_week_3).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Korea - Predicted Amount of Active Cases for Week 3 of Next Month'
    ).interactive()

    chart_3.show()
    chart_3.save("JSON_charts/KOR/KOR_Week_3_Chart.json")

    chart_4 = alt.Chart(trimmed_week_4).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Korea - Predicted Amount of Active Cases for Week 4 of Next Month'
    ).interactive()

    chart_4.show()
    chart_4.save("JSON_charts/KOR/KOR_Week_4_Chart.json")


def chart_america(worst_df, norm_df, best_df):
    # charts data using altair with the input predict_df
    trimmed_worst = worst_df.loc[50:]
    trimmed_worst.columns = ['Date', 'Worst']
    trimmed_norm = norm_df.loc[50:]
    trimmed_norm.columns = ['Date', 'Norm']
    trimmed_best = best_df.loc[50:]
    trimmed_best.columns = ['Date', 'Best']

    trimmed_total = trimmed_worst.merge(trimmed_norm, on='Date')
    trimmed_total = trimmed_total.merge(trimmed_best, on='Date')
    # print(trimmed_total.tail(31))

    # chart entire prediction
    chart_full = alt.Chart(trimmed_total).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y='Active Cases:Q',
        color='Curve:N'
    ).properties(
        title='USA - Predicted Amount of Active Cases for the Next Month'
    ).interactive()

    chart_full.show()
    chart_full.save("JSON_charts/USA/USA_Full_Chart.json")

    # trim dataframes for individual predicted weeks
    trimmed_week_1 = trimmed_total.loc[37:43]
    trimmed_week_2 = trimmed_total.loc[44:50]
    trimmed_week_3 = trimmed_total.loc[51:57]
    trimmed_week_4 = trimmed_total.loc[58:64]

    chart_1 = alt.Chart(trimmed_week_1).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='USA - Predicted Amount of Active Cases for Week 1 of Next Month'
    ).interactive()

    chart_1.show()
    chart_1.save("JSON_charts/USA/USA_Week_1_Chart.json")

    chart_2 = alt.Chart(trimmed_week_2).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='USA - Predicted Amount of Active Cases for Week 2 of Next Month'
    ).interactive()

    chart_2.show()
    chart_2.save("JSON_charts/USA/USA_Week_2_Chart.json")

    chart_3 = alt.Chart(trimmed_week_3).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='USA - Predicted Amount of Active Cases for Week 3 of Next Month'
    ).interactive()

    chart_3.show()
    chart_3.save("JSON_charts/USA/USA_Week_3_Chart.json")

    chart_4 = alt.Chart(trimmed_week_4).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='USA - Predicted Amount of Active Cases for Week 4 of Next Month'
    ).interactive()

    chart_4.show()
    chart_4.save("JSON_charts/USA/USA_Week_4_Chart.json")


def trainData(listDF):
    # organize data and perform training
    covidCanadaTotal_df = listDF[0]
    covidCanadaTotalDeaths_df = listDF[1]
    covidCanadaTotalRecovered_df = listDF[2]
    covidAB_df = listDF[3]
    covidABDeath_df = listDF[4]
    covidBC_df = listDF[5]
    covidBCDeath_df = listDF[6]
    covidMN_df = listDF[7]
    covidMNDeath_df = listDF[8]
    covidNB_df = listDF[9]
    covidNBDeath_df = listDF[10]
    covidNL_df = listDF[11]
    covidNLDeath_df = listDF[12]
    covidNS_df = listDF[13]
    covidNSDeath_df = listDF[14]
    covidON_df = listDF[15]
    covidONDeath_df = listDF[16]
    covidPE_df = listDF[17]
    covidPEDeath_df = listDF[18]
    covidQC_df = listDF[19]
    covidQCDeath_df = listDF[20]
    covidSA_df = listDF[21]
    covidSADeath_df = listDF[22]
    covidAmericaTotal_df = listDF[23]
    covidAmericaTotalDeaths_df = listDF[24]
    covidAmericaTotalRecovered_df = listDF[25]
    covidKoreaTotal_df = listDF[26]
    covidKoreaTotalDeaths_df = listDF[27]
    covidKoreaTotalRecovered_df = listDF[28]

    # create dataframe to input as active cases trainer
    canada_df = covidCanadaTotal_df
    canada_df = canada_df.merge(covidCanadaTotalDeaths_df, on='Date')
    canada_df = canada_df.merge(covidCanadaTotalRecovered_df, on='Date')
    canada_df = canada_df.merge(covidAB_df, on='Date')
    canada_df = canada_df.merge(covidBC_df, on='Date')
    canada_df = canada_df.merge(covidMN_df, on='Date')
    canada_df = canada_df.merge(covidNB_df, on='Date')
    canada_df = canada_df.merge(covidNL_df, on='Date')
    canada_df = canada_df.merge(covidNS_df, on='Date')
    canada_df = canada_df.merge(covidON_df, on='Date')
    canada_df = canada_df.merge(covidPE_df, on='Date')
    canada_df = canada_df.merge(covidQC_df, on='Date')
    canada_df = canada_df.merge(covidSA_df, on='Date')

    america_df = covidAmericaTotal_df
    america_df = america_df.merge(covidAmericaTotalDeaths_df, on='Date')
    america_df = america_df.merge(covidAmericaTotalRecovered_df, on='Date')

    korea_df = covidKoreaTotal_df
    korea_df = korea_df.merge(covidKoreaTotalDeaths_df, on='Date')
    korea_df = korea_df.merge(covidKoreaTotalRecovered_df, on='Date')

    # create input arrays for training model
    X_canada = np.array(canada_df.drop(['Active_Cases', 'Date'], axis=1))
    y_canada = np.array(canada_df['Active_Cases'])
    X_canada = preprocessing.scale(X_canada)

    X_america = np.array(america_df.drop(['Active_Cases', 'Date'], axis=1))
    y_america = np.array(america_df['Active_Cases'])
    X_america = preprocessing.scale(X_america)

    X_korea = np.array(korea_df.drop(['Active_Cases', 'Date'], axis=1))
    y_korea = np.array(korea_df['Active_Cases'])
    X_korea = preprocessing.scale(X_korea)

    # split data into training and test data
    X_train_canada, X_test_canada, y_train_canada, y_test_canada = model_selection.train_test_split(
        X_canada, y_canada, test_size=0.1)

    X_train_america, X_test_america, y_train_america, y_test_america = model_selection.train_test_split(
        X_america, y_america, test_size=0.1)

    X_train_korea, X_test_korea, y_train_korea, y_test_korea = model_selection.train_test_split(
        X_korea, y_korea, test_size=0.1)

    # train using SGDRegressor
    clf_canada = linear_model.SGDRegressor()
    clf_canada.fit(X_train_canada, y_train_canada)
    accuracy_canada = clf_canada.score(X_test_canada, y_test_canada)

    clf_america = linear_model.SGDRegressor()
    clf_america.fit(X_train_america, y_train_america)
    accuracy_america = clf_america.score(X_test_america, y_test_america)

    clf_korea = linear_model.SGDRegressor()
    clf_korea.fit(X_train_korea, y_train_korea)
    accuracy = clf_korea.score(X_test_korea, y_test_korea)

    # create size of forecast and perform prediction
    forecast_out = 30
    X_predict_canada = X_canada[-forecast_out:]
    forecast_set_canada = clf_canada.predict(X_predict_canada)

    X_predict_america = X_america[-forecast_out:]
    forecast_set_america = clf_america.predict(X_predict_america)

    X_predict_korea = X_korea[-forecast_out:]
    forecast_set_korea = clf_korea.predict(X_predict_korea)

    # create prediction data frame
    predict_worst_canada_df = canada_df.drop(
        ['Cases', 'Cases_x', 'Cases_y', 'Total_Deaths', 'Recoveries'], 1)
    predict_norm_canada_df = canada_df.drop(
        ['Cases', 'Cases_x', 'Cases_y', 'Total_Deaths', 'Recoveries'], 1)
    predict_best_canada_df = canada_df.drop(
        ['Cases', 'Cases_x', 'Cases_y', 'Total_Deaths', 'Recoveries'], 1)

    predict_worst_america_df = america_df.drop(
        ['Worst_Cases', 'Worst_Deaths', 'Worst_Recoveries'], 1)
    predict_norm_america_df = america_df.drop(
        ['Worst_Cases', 'Worst_Deaths', 'Worst_Recoveries'], 1)
    predict_best_america_df = america_df.drop(
        ['Worst_Cases', 'Worst_Deaths', 'Worst_Recoveries'], 1)

    predict_worst_korea_df = korea_df.drop(
        ['Best_Cases', 'Best_Deaths', 'Best_Recoveries'], 1)
    predict_norm_korea_df = korea_df.drop(
        ['Best_Cases', 'Best_Deaths', 'Best_Recoveries'], 1)
    predict_best_korea_df = korea_df.drop(
        ['Best_Cases', 'Best_Deaths', 'Best_Recoveries'], 1)

    inc_canada_df = expoIncrease(predict_worst_canada_df, forecast_set_canada)
    con_canada_df = continueTrend(predict_norm_canada_df, forecast_set_canada)
    lev_canada_df = levelOff(predict_best_canada_df, forecast_set_canada)

    inc_america_df = expoIncrease(
        predict_worst_america_df, forecast_set_america)
    con_america_df = continueTrend(
        predict_norm_america_df, forecast_set_america)
    lev_america_df = levelOff(predict_best_america_df, forecast_set_america)

    inc_korea_df = expoIncrease(
        predict_worst_korea_df, forecast_set_korea)
    con_korea_df = continueTrend(
        predict_norm_korea_df, forecast_set_korea)
    lev_korea_df = levelOff(predict_best_korea_df, forecast_set_korea)

    chart_canada(inc_canada_df, con_canada_df, lev_canada_df)
    chart_america(inc_america_df, con_america_df, lev_america_df)
    chart_korea(inc_korea_df, con_korea_df, lev_korea_df)

    return
