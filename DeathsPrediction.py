# This file contains the prediction for our death data, unfortunately
# the predictions were innacurate and reflected a predicted amount of
# deaths that did not make sense with the rest of the data. Here is
# The fully functioning code anyways.

import pandas as pd
import altair as alt
import numpy as np
import math
from sklearn import linear_model, preprocessing, model_selection
import datetime

def expoIncreaseDeath(predict_df, forecast_set):
    # Prediction function focusing on expected exponential growth
    last_date = "2020-04-17"
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    index = 87
    diff = predict_df.loc[index - 1][1] - forecast_set[0]
    mult = 1.02

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        mult *= 1.03
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff)]
        index += 1

    return predict_df


 def continueTrendDeath(predict_df, forecast_set):
    # Prediction function focusing on maintaining current rate
    last_date = "2020-04-17"
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    index = 87
    diff = predict_df.loc[index - 1][1] - forecast_set[0]
    mult = 1.01

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        mult *= 1.007
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff)]
        index += 1

    return predict_df


def levelOffDeath(predict_df, forecast_set):
    # prediction function focusing on levelling off growth rate slowly
    last_date = "2020-04-17"
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    index = 87
    diff = predict_df.loc[index - 1][1] - forecast_set[0]
    if (diff <= 0):
        diff = 0
    mult = 1.03

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        mult *= 0.998
        predict_df.loc[index] = [str(next_date)] + [i]
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


    chart = alt.Chart(trimmed_total).transform_fold(
        ['Worst', 'Norm', 'Best'],
        as_=['Curve', 'Active Cases']
    ).mark_line().encode(
        x='Date:T',
        y='Active Cases:Q',
        color='Curve:N'
    ).interactive()

    chart.show()
    chart.save("JSON_charts/CAN_Full_Chart.json")

def trainDeathData(listDF):
    # organize data and perform training
    covidCanadaTotal_df = listDF[0]
    covidCanadaTotalDeaths_df = listDF[1]
    covidCanadaTotalRecovered_df = listDF[2]
    covidABDeath_df = listDF[4]
    covidBCDeath_df = listDF[6]
    covidMNDeath_df = listDF[8]
    covidNBDeath_df = listDF[10]
    covidNLDeath_df = listDF[12]
    covidNSDeath_df = listDF[14]
    covidONDeath_df = listDF[16]
    covidPEDeath_df = listDF[18]
    covidQCDeath_df = listDF[20]
    covidSADeath_df = listDF[22]
    worstcases = listDF[23]
    worstdeaths = listDF[24]
    worstrecovored = listDF[25]
    bestcases = listDF[26]
    bestdeaths = listDF[27]
    bestrecovered = listDF[28]

    # create dataframe to input as deaths trainer
    death_df = covidCanadaTotalDeaths_df
    death_df = death_df.merge(covidCanadaTotalRecovered_df, on='Date')
    death_df = death_df.merge(covidABDeath_df, on='Date')
    death_df = death_df.merge(covidBCDeath_df, on='Date')
    death_df = death_df.merge(covidMNDeath_df, on='Date')
    death_df = death_df.merge(covidNBDeath_df, on='Date')
    death_df = death_df.merge(covidNLDeath_df, on='Date')
    death_df = death_df.merge(covidNSDeath_df, on='Date')
    death_df = death_df.merge(covidONDeath_df, on='Date')
    death_df = death_df.merge(covidPEDeath_df, on='Date')
    death_df = death_df.merge(covidQCDeath_df, on='Date')
    death_df = death_df.merge(covidSADeath_df, on='Date')
    death_df = death_df.merge(worstdeaths, on='Date')
    death_df = death_df.merge(bestdeaths, on='Date')
    death_df.dropna(inplace=True)

    print(death_df)
    # create input arrays for training model
    X = np.array(death_df.drop(['Total_Deaths', 'Date'], axis=1))
    y = np.array(death_df['Total_Deaths'])
    X = preprocessing.scale(X)

    # split data into training and test data
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=0.1)

    # train using SGDRegressor
    clf = linear_model.SGDRegressor()
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    print(accuracy)

    # create size of forecast and perform prediction
    forecast_out = 30
    X_predict = X[-forecast_out:]
    forecast_set = clf.predict(X_predict)

    # create prediction data frame
    predict_worst_df = death_df.drop(
        ['Worst_Deaths', 'Deaths_y', 'Deaths_x', 'Best_Deaths', 'Recoveries'], 1)
    predict_norm_df = death_df.drop(
        ['Worst_Deaths', 'Deaths_y', 'Deaths_x', 'Best_Deaths', 'Recoveries'], 1)
    predict_best_df = death_df.drop(
        ['Worst_Deaths', 'Deaths_y', 'Deaths_x', 'Best_Deaths', 'Recoveries'], 1)

    inc_df = expoIncreaseDeath(predict_worst_df, forecast_set)
    con_df = continueTrendDeath(predict_norm_df, forecast_set)
    lev_df = levelOffDeath(predict_best_df, forecast_set)

    chart(inc_df, con_df, lev_df)

    return