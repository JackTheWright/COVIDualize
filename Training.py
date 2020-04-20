import pandas as pd
import altair as alt
import numpy as np
import math
from sklearn import linear_model, preprocessing, model_selection
# from statsmodels.tsa.arima_model import ARIMA
import datetime


def expoIncrease(predict_df, forecast_set, inpSize):
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
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff + 500)]
        index += 1
        mult *= 1.03

    chart(predict_df)


def levelOff(predict_df, forecast_set, inpSize):
    last_date = "2020-04-17"
    last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day
    index = 87
    diff = predict_df.loc[index - 1][1] - forecast_set[0]
    mult = 1

    for i in forecast_set:
        if (inpSize == 60):
            if (inpSize == 90):
                if (inpSize == 120):
                    if (index == 87 + 90):
                        diff = predict_df.loc[index - 1][1] - \
                            forecast_set[90]
                if (index == 87 + 60):
                    diff = predict_df.loc[index - 1][1] - forecast_set[60]
            if (index == 87 + 30):
                print(len(predict_df))
                diff = predict_df.loc[index - 1][1] - forecast_set[30]

        print(diff)
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        predict_df.loc[index] = [str(next_date)] + [mult*(i + diff)]
        index += 1
        mult *= 0.988

    chart(predict_df)


def chart(predict_df):
    trimmed_data = predict_df.loc[50:]
    print(trimmed_data)
    chart = alt.Chart(trimmed_data).mark_line().encode(
        x='Date',
        y='Total_Deaths'
    ).interactive()

    chart.show()


def trainData(listDF):
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

    active_df = covidCanadaTotal_df
    active_df = active_df.merge(covidCanadaTotalDeaths_df, on='Date')
    active_df = active_df.merge(covidCanadaTotalRecovered_df, on='Date')
    active_df = active_df.merge(covidABDeath_df, on='Date')
    active_df = active_df.merge(covidBCDeath_df, on='Date')
    active_df = active_df.merge(covidMNDeath_df, on='Date')
    active_df = active_df.merge(covidNBDeath_df, on='Date')
    active_df = active_df.merge(covidNLDeath_df, on='Date')
    active_df = active_df.merge(covidNSDeath_df, on='Date')
    active_df = active_df.merge(covidONDeath_df, on='Date')
    active_df = active_df.merge(covidPEDeath_df, on='Date')
    active_df = active_df.merge(covidQCDeath_df, on='Date')
    active_df = active_df.merge(covidSADeath_df, on='Date')
    active_df = active_df.merge(worstdeaths, on='Date')
    active_df = active_df.merge(bestdeaths, on='Date')

    print(active_df)
    

    # X = np.array(active_df.drop(['Active_Cases', 'Date'], axis=1))
    # y = np.array(active_df['Active_Cases'])

    # clf = ARIMA(y, (1, 1, 1))
    # clf_fit = clf.fit(disp=0)

    # start_index = len(y)
    # end_index = start_index + 6
    # forecast = clf_fit.predict(start=start_index, end=end_index)

    # history = [x for x in y]
    # day = 1
    # for yhat in forecast:
    #     print('Day %d: %f' % (day, yhat))
    #     history.append(yhat)
    #     day += 1

    # predict_df = active_df.drop(
    #     ['Cases', 'Cases_x', 'Cases_y', 'Deaths', 'Recoveries'], 1)

    # last_date = "2020-04-17"
    # last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
    # last_unix = last_date.timestamp()
    # one_day = 86400
    # next_unix = last_unix + one_day
    # index = 87

    # for i in forecast:
    #     next_date = datetime.datetime.fromtimestamp(next_unix)
    #     next_unix += one_day
    #     predict_df.loc[index] = [str(next_date)] + [i]
    #     index += 1

    # chart = alt.Chart(predict_df).mark_line().encode(
    #     x='Date',
    #     y='Active_Cases'
    # ).interactive()

    # chart.show()

    # forecast_col = 'Active_Cases'
    # forecast_out = int(math.ceil(0.01*len(active_df)))

    # active_df['Lag_Case_1'] = active_df['Active_Cases'].shift(-1)
    # active_df['Lag_Case_2'] = active_df['Active_Cases'].shift(-2)
    # active_df['Lag'] = active_df[forecast_col].shift(-forecast_out)
    active_df.dropna(inplace=True)

    X = np.array(active_df.drop(['Total_Deaths', 'Date'], axis=1))
    y = np.array(active_df['Total_Deaths'])
    X = preprocessing.scale(X)
    # X_predict = X[-forecast_out:]

    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=0.1)

    clf = linear_model.SGDRegressor()
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    print(accuracy)

    # forecast_set = clf.predict(X_predict)
    # forecast_set = predict(clf, active_df, X, 30, 30)
    forecast_out = 30
    X_predict = X[-forecast_out:]
    # print(X_predict)

    forecast_set = clf.predict(X_predict)

    predict_df = active_df.drop(
        ['Deaths_x', 'Deaths_y', 'Recoveries', 'Active_Cases', 'Cases'], 1)

    # expoIncrease(predict_df, forecast_set)
    levelOff(predict_df, forecast_set, 30)

    return
