# Contains functions for handling the data from the CSV file and creating graphs

import pandas
import altair as alt
from SGDRegression import trainData

DEBUG = False

# Function:     Import CSV data and create dataframes
# Return:       11 data frames, 1 for each province and 1 for Canada's total


def MainDataImport():

    alt.renderers.enable('mimetype')

    # Create a Pandas dataframe to hold the imported CSV data from CanadaCovid.csv
    covidCanadaTotalCases_df = pandas.read_csv(
        "~/Desktop/COVIDualize/CanadaCovid.csv")
    covidCanadaTotalDeaths_df = pandas.read_csv(
        "~/Desktop/COVIDualize/CanadaCovidDeath.csv")
    covidCanadaTotalRecovered_df = pandas.read_csv(
        "~/Desktop/COVIDualize/CanadaCovidRecovered.csv")
    # Remove the columns we don't care about
    covidCanadaTotalCases_df = covidCanadaTotalCases_df.drop(
        ['Country/Region', 'Lat', 'Long'], axis=1)

    if DEBUG:
         print(covidCanadaTotalCases_df)

    columninds = ['Cases']

    # Split the covid data up by provice. One data frame per province, then drop the province column.
    covidAB_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'Alberta']).drop(
        ['Province'], axis=1))).transpose()
    covidAB_df.columns = columninds
    covidAB_df.index.name = 'Date'
    covidAB_df.reset_index(inplace=True)
    covidBC_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'British Columbia']).drop(
        ['Province'], axis=1))).transpose()
    covidBC_df.columns = columninds
    covidBC_df.index.name = 'Date'
    covidBC_df.reset_index(inplace=True)
    covidMN_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'Manitoba']).drop(
        ['Province'], axis=1))).transpose()
    covidMN_df.columns = columninds
    covidMN_df.index.name = 'Date'
    covidMN_df.reset_index(inplace=True)
    covidNB_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'New Brunswick']).drop(
        ['Province'], axis=1))).transpose()
    covidNB_df.columns = columninds
    covidNB_df.index.name = 'Date'
    covidNB_df.reset_index(inplace=True)
    covidNL_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'Newfoundland and Labrador']).drop(
        ['Province'], axis=1))).transpose()
    covidNL_df.columns = columninds
    covidNL_df.index.name = 'Date'
    covidNL_df.reset_index(inplace=True)
    covidNS_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'Nova Scotia']).drop(
        ['Province'], axis=1))).transpose()
    covidNS_df.columns = columninds
    covidNS_df.index.name = 'Date'
    covidNS_df.reset_index(inplace=True)
    covidON_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'Ontario']).drop(
        ['Province'], axis=1))).transpose()
    covidON_df.columns = columninds
    covidON_df.index.name = 'Date'
    covidON_df.reset_index(inplace=True)
    covidPE_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'Prince Edward Island']).drop(
        ['Province'], axis=1))).transpose()
    covidPE_df.columns = columninds
    covidPE_df.index.name = 'Date'
    covidPE_df.reset_index(inplace=True)
    covidQC_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'Quebec']).drop(
        ['Province'], axis=1))).transpose()
    covidQC_df.columns = columninds
    covidQC_df.index.name = 'Date'
    covidQC_df.reset_index(inplace=True)
    covidSA_df = (((covidCanadaTotalCases_df.loc[covidCanadaTotalCases_df['Province'] == 'Saskatchewan']).drop(
        ['Province'], axis=1))).transpose()
    covidSA_df.columns = columninds
    covidSA_df.index.name = 'Date'
    covidSA_df.reset_index(inplace=True)

    if DEBUG:
         print(covidAB_df)

    # Drop the province column and sum them all up to create the total per day for all provinces. Convert from series to df for Altair
    covidCanadaTotalCases_df = covidCanadaTotalCases_df.drop(
        ['Province'], axis=1)
    covidCanadaTotal_df = covidCanadaTotalCases_df.sum(axis=0, skipna=True)
    covidCanadaTotal_df = covidCanadaTotal_df.to_frame()
    covidCanadaTotal_df.columns = columninds
    covidCanadaTotal_df.index.name = 'Date'
    covidCanadaTotal_df.reset_index(inplace=True)
    
    if DEBUG:
        print(covidCanadaTotal_df)

    # Drop all columns for Deaths. Convert them to the same form as total cases above.
    covidCanadaTotalDeaths_df = covidCanadaTotalDeaths_df.drop(
        ['Province', 'Country/Region', 'Lat', 'Long'], axis=1)
    covidCanadaTotalDeaths_df = covidCanadaTotalDeaths_df.sum(
        axis=0, skipna=True)
    covidCanadaTotalDeaths_df = covidCanadaTotalDeaths_df.to_frame()
    covidCanadaTotalDeaths_df.columns = ['Deaths']
    covidCanadaTotalDeaths_df.index.name = 'Date'
    covidCanadaTotalDeaths_df.reset_index(inplace=True)

    if DEBUG:
        print(covidCanadaTotalDeaths_df)

    # Recovered is not by province so requires less clean up.
    covidCanadaTotalRecovered_df = covidCanadaTotalRecovered_df.transpose()
    covidCanadaTotalRecovered_df.columns = ['Recoveries']
    covidCanadaTotalRecovered_df.index.name = 'Date'
    covidCanadaTotalRecovered_df.reset_index(inplace=True)

    if DEBUG:
        print(covidCanadaTotalRecovered_df)

    covidCanadaTotal_df['Active_Cases'] = covidCanadaTotal_df.Cases - \
        (covidCanadaTotalDeaths_df.Deaths + covidCanadaTotalRecovered_df.Recoveries)

    if DEBUG:
        print(covidCanadaTotal_df)


    return covidCanadaTotal_df, covidCanadaTotalDeaths_df, covidCanadaTotalRecovered_df, covidAB_df, covidBC_df, covidMN_df, covidNB_df, covidNL_df, covidNS_df, covidON_df, covidPE_df, covidQC_df, covidSA_df


def WorstCaseDataImport():
    covidWorseTotal_df = pandas.read_csv(
        "~/Desktop/COVIDualize/WorstCaseData.csv")
    covidWorseTotalDeaths_df = pandas.read_csv(
        "~/Desktop/COVIDualize/WorstCaseDeaths.csv")
    covidWorseTotalRecovered_df = pandas.read_csv(
        "~/Desktop/COVIDualize/WorstCaseRecovery.csv")

    covidWorseTotal_df = covidWorseTotal_df.transpose()
    covidWorseTotal_df.columns = ['Cases']
    covidWorseTotal_df.index.name = 'Date'
    covidWorseTotal_df.reset_index(inplace=True)

    covidWorseTotalDeaths_df = covidWorseTotalDeaths_df.sum(
        axis=0, skipna=True)
    covidWorseTotalDeaths_df = covidWorseTotalDeaths_df.to_frame()
    covidWorseTotalDeaths_df.columns = ['Deaths']
    covidWorseTotalDeaths_df.index.name = 'Date'
    covidWorseTotalDeaths_df.reset_index(inplace=True)

    covidWorseTotalRecovered_df = covidWorseTotalRecovered_df.transpose()
    covidWorseTotalRecovered_df.columns = ['Recoveries']
    covidWorseTotalRecovered_df.index.name = 'Date'
    covidWorseTotalRecovered_df.reset_index(inplace=True)

    covidWorseTotal_df['Active_Cases'] = covidWorseTotal_df.Cases - \
        (covidWorseTotalDeaths_df.Deaths + covidWorseTotalRecovered_df.Recoveries)
    print(covidWorseTotal_df)
    return


def BestCaseDataImport():
    covidBestTotal_df = pandas.read_csv(
        "~/Desktop/COVIDualize/BestCaseData.csv")
    covidBestTotalDeaths_df = pandas.read_csv(
        "~/Desktop/COVIDualize/BestCaseDeaths.csv")
    covidBestTotalRecovered_df = pandas.read_csv(
        "~/Desktop/COVIDualize/BestCaseRecovery.csv")

    covidBestTotal_df = covidBestTotal_df.transpose()
    covidBestTotal_df.columns = ['Cases']
    covidBestTotal_df.index.name = 'Date'
    covidBestTotal_df.reset_index(inplace=True)
    print(covidBestTotal_df)

    covidBestTotalDeaths_df = covidBestTotalDeaths_df.sum(axis=0, skipna=True)
    covidBestTotalDeaths_df = covidBestTotalDeaths_df.to_frame()
    covidBestTotalDeaths_df.columns = ['Deaths']
    covidBestTotalDeaths_df.index.name = 'Date'
    covidBestTotalDeaths_df.reset_index(inplace=True)

    covidBestTotalRecovered_df = covidBestTotalRecovered_df.transpose()
    covidBestTotalRecovered_df.columns = ['Recoveries']
    covidBestTotalRecovered_df.index.name = 'Date'
    covidBestTotalRecovered_df.reset_index(inplace=True)

    covidBestTotal_df['Active_Cases'] = covidBestTotal_df.Cases - \
        (covidBestTotalDeaths_df.Deaths + covidBestTotalRecovered_df.Recoveries)
    print(covidBestTotal_df)

    return


def main():
    covidCanadaTotal_df, covidAB_df, covidBC_df, covidMN_df, covidNB_df, covidNL_df, covidNS_df, covidON_df, covidPE_df, covidQC_df, covidSA_df = MainDataImport()
    WorstCaseDataImport()
    BestCaseDataImport()
    chart = alt.Chart(covidCanadaTotal_df).mark_line().encode(
        x='Date',
        y='Active_Cases'
    ).interactive()

    chart.show()
    return


main()
