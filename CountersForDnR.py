import random as r
import pandas as pd

# This function will calculate the weekly number of deaths based on a 2-3% death
# rate of new cases and a 10 day average death time. 

def deathCounter(predict_df):
    predictdateless_df = predict_df.drop(['Date'], 1)
    predictlist = predictdateless_df.values.tolist()

    # Subtract the end of the week active cases from the start of week active cases to get
    # cases for the week for 10 days prior. This is the average Death time for a patient.
    weekOneDiff = predictlist[83][0] - predictlist[77][0]
    weekTwoDiff = predictlist[90][0] - predictlist[84][0]
    weekThreeDiff = predictlist[97][0] - predictlist[91][0]
    weekFourDiff = predictlist[104][0] - predictlist[98][0]

    # Calculate deaths for the week at a 2-3% death rate.
    weekOneDeaths = r.uniform(0.02, 0.03) * weekOneDiff
    weekTwoDeaths = r.uniform(0.02, 0.03) * weekTwoDiff
    weekThreeDeaths = r.uniform(0.02, 0.03) * weekThreeDiff
    weekFourDeaths = r.uniform(0.02, 0.03) * weekFourDiff

    print(weekOneDeaths)
    print(weekTwoDeaths)
    print(weekThreeDeaths)
    print(weekFourDeaths)


# This function will calculate the weekly number of recoveries based on a 80-83% recovery
# rate of new cases and a 10 day average recovery time. We have left some room for error
# where cases do not recover or do not die within the time period.

def recoverCounter(predict_df):
    #Turn the dataframe into a list for easier access to individual elements
    predictdateless_df = predict_df.drop(['Date'], 1)
    predictlist = predictdateless_df.values.tolist()

    # Subtract the end of the week active cases from the start of week active cases to get
    # cases for the week for 10 days prior. This is the average recovery time for a patient.
    weekOneDiff = predictlist[83][0] - predictlist[77][0]
    weekTwoDiff = predictlist[90][0] - predictlist[84][0]
    weekThreeDiff = predictlist[97][0] - predictlist[91][0]
    weekFourDiff = predictlist[104][0] - predictlist[98][0]

    # Calculate deaths for the week at a 80-83% recovery rate.
    weekOneRecovery = r.uniform(0.80, 0.83) * weekOneDiff
    weekTwoRecovery = r.uniform(0.80, 0.83) * weekTwoDiff
    weekThreeRecovery = r.uniform(0.80, 0.83) * weekThreeDiff
    weekFourRecovery = r.uniform(0.80, 0.83) * weekFourDiff

    print(weekOneRecovery)
    print(weekTwoRecovery)
    print(weekThreeRecovery)
    print(weekFourRecovery)