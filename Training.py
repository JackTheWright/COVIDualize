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
    diff = predict_df.loc[index - 1][1] - forecast_set[0]
    mult = 1.02

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff)]
        index += 1
        mult *= 1.03

    chart(predict_df)


def continueTrend(predict_df, forecast_set):
    # Prediction function focusing on maintaining current rate
    last_date = "2020-04-17"
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    index = 87
    diff = predict_df.loc[index - 1][1] - forecast_set[0]
    mult = 1

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff)]
        index += 1
        mult *= 1

    chart(predict_df)


def levelOff(predict_df, forecast_set):
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
    mult = 1

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff)]
        index += 1
        mult *= 0.988

    chart(predict_df)


def chart(predict_df):
    # charts data using altair with the input predict_df
    trimmed_data = predict_df.loc[50:]
    # print(trimmed_data)
    chart = alt.Chart(trimmed_data).mark_line().encode(
        x='Date',
        y='Active_Cases'
    ).interactive()

    chart.show()


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
    worstdeaths = listDF[23]
    bestdeaths = listDF[24]

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

    # create dataframe to input as deaths trainer
    death_df = active_df.merge(covidABDeath_df, on='Date')
    death_df = active_df.merge(covidBCDeath_df, on='Date')
    death_df = active_df.merge(covidMNDeath_df, on='Date')
    death_df = active_df.merge(covidNBDeath_df, on='Date')
    death_df = active_df.merge(covidNLDeath_df, on='Date')
    death_df = active_df.merge(covidNSDeath_df, on='Date')
    death_df = active_df.merge(covidONDeath_df, on='Date')
    death_df = active_df.merge(covidPEDeath_df, on='Date')
    death_df = active_df.merge(covidQCDeath_df, on='Date')
    death_df = active_df.merge(covidSADeath_df, on='Date')
    death_df = active_df.merge(worstdeaths, on='Date')
    death_df = active_df.merge(bestdeaths, on='Date')
    active_df.dropna(inplace=True)
    death_df.dropna(inplace=True)

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
    print(active_df)
    predict_df = active_df.drop(
        ['Cases', 'Cases_x', 'Cases_y', 'Total_Deaths', 'Recoveries'], 1)

    expoIncrease(predict_df, forecast_set)
    continueTrend(predict_df, forecast_set)
    levelOff(predict_df, forecast_set)

    return
