import pandas as pd
import altair as alt
import numpy as np
import math
from sklearn import linear_model, preprocessing, model_selection
import datetime


def expoIncrease(predict_df, forecast_set):
    # Prediction function focusing on expected exponential growth
    last_date = "2020-04-17"
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    index = 87
    diff = (predict_df.loc[index - 1][1] - forecast_set[0])*1.05
    mult = 1.0

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        mult *= 1.03
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff)]
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
    diff = (predict_df.loc[index - 1][1] - forecast_set[0])*1.05
    mult = 1.0

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        mult *= 1
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff)]
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
    diff = (predict_df.loc[index - 1][1] - forecast_set[0])*1.05
    mult = 1.0

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        mult *= 0.988
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff)]
        index += 1

    return predict_df


def chart(worst_df, norm_df, best_df):
    # charts data using altair with the input predict_df
    trimmed_worst = worst_df.loc[50:]
    trimmed_worst.columns = ['Date', 'Worst']
    trimmed_norm = norm_df.loc[50:]
    trimmed_norm.columns = ['Date', 'Norm']
    trimmed_best = best_df.loc[50:]
    trimmed_best.columns = ['Date', 'Best']

    trimmed_total = trimmed_worst.merge(trimmed_norm, on='Date')
    trimmed_total = trimmed_total.merge(trimmed_best, on='Date')
    print(trimmed_total.tail(31))

    # chart entire prediction
    chart_full = alt.Chart(trimmed_total).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y='Active Cases:Q',
        color='Curve:N'
    ).properties(
        title='Predicted Amount of Active Cases for the Next Month'
    ).interactive()

    chart_full.show()
    chart_full.save("JSON_charts/CAN_Full_Chart.json")

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
        title='Predicted Amount of Active Cases for Week 1 of Next Month'
    ).interactive()

    chart_1.show()
    chart_1.save("JSON_charts/CAN_Week_1_Chart.json")

    chart_2 = alt.Chart(trimmed_week_2).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Predicted Amount of Active Cases for Week 2 of Next Month'
    ).interactive()

    chart_2.show()
    chart_2.save("JSON_charts/CAN_Week_2_Chart.json")

    chart_3 = alt.Chart(trimmed_week_3).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Predicted Amount of Active Cases for Week 3 of Next Month'
    ).interactive()

    chart_3.show()
    chart_3.save("JSON_charts/CAN_Week_3_Chart.json")

    chart_4 = alt.Chart(trimmed_week_4).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y=alt.Y('Active Cases:Q', scale=alt.Scale(zero=False)),
        color='Curve:N'
    ).properties(
        title='Predicted Amount of Active Cases for Week 4 of Next Month'
    ).interactive()

    chart_4.show()
    chart_4.save("JSON_charts/CAN_Week_4_Chart.json")


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
    worstcases = listDF[23]
    worstdeaths = listDF[24]
    worstrecovered = listDF[25]
    bestcases = listDF[26]
    bestdeaths = listDF[27]
    bestrecovered = listDF[28]

    # create dataframe to input as active cases trainer
    active_df = covidCanadaTotal_df
    active_df = active_df.merge(covidCanadaTotalDeaths_df, on='Date')
    active_df = active_df.merge(covidCanadaTotalRecovered_df, on='Date')
    active_df = active_df.merge(covidAB_df, on='Date')
    active_df = active_df.merge(covidBC_df, on='Date')
    active_df = active_df.merge(covidMN_df, on='Date')
    active_df = active_df.merge(covidNB_df, on='Date')
    active_df = active_df.merge(covidNL_df, on='Date')
    active_df = active_df.merge(covidNS_df, on='Date')
    active_df = active_df.merge(covidON_df, on='Date')
    active_df = active_df.merge(covidPE_df, on='Date')
    active_df = active_df.merge(covidQC_df, on='Date')
    active_df = active_df.merge(covidSA_df, on='Date')

    # create input arrays for training model
    X = np.array(active_df.drop(['Active_Cases', 'Date'], axis=1))
    y = np.array(active_df['Active_Cases'])
    X = preprocessing.scale(X)

    # split data into training and test data
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=0.1)

    # train using SGDRegressor
    clf = linear_model.SGDRegressor()
    clf.fit(X_train, y_train)
    #accuracy = clf.score(X_test, y_test)

    # create size of forecast and perform prediction
    forecast_out = 30
    X_predict = X[-forecast_out:]
    forecast_set = clf.predict(X_predict)

    # create prediction data frame
    predict_worst_df = active_df.drop(
        ['Cases', 'Cases_x', 'Cases_y', 'Total_Deaths', 'Recoveries'], 1)
    predict_norm_df = active_df.drop(
        ['Cases', 'Cases_x', 'Cases_y', 'Total_Deaths', 'Recoveries'], 1)
    predict_best_df = active_df.drop(
        ['Cases', 'Cases_x', 'Cases_y', 'Total_Deaths', 'Recoveries'], 1)

    inc_df = expoIncrease(predict_worst_df, forecast_set)
    con_df = continueTrend(predict_norm_df, forecast_set)
    lev_df = levelOff(predict_best_df, forecast_set)

    chart(inc_df, con_df, lev_df)

    return


# This function will calculate the weekly number of deaths based on a 2-3% death
# rate of new cases and a 10 day average death time. 

def deathCounter(predict_df):
        weekOneDays = predict_df[27:33]
        weekTwoDays = predict_df[34:40]
        weekOneDeaths = predict_df