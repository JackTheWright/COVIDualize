# Contains functions for handling the data from the CSV file and creating graphs

import pandas
import altair as alt
from SGDRegression import trainData

DEBUG = False

# Function:     Import CSV data and create dataframes
# Return:       11 data frames, 1 for each province and 1 for Canada's total


def dataImport():

    alt.renderers.enable('mimetype')

    # Create a Pandas dataframe to hold the imported CSV data from CanadaCovid.csv
    covidCanadaTotalCases_df = pandas.read_csv(
        "~/Desktop/SCHOOL/cmpt-340/term-proj/covidualize/CanadaCovid.csv")
    covidCanadaTotalDeaths_df = pandas.read_csv(
        "~/Desktop/SCHOOL/cmpt-340/term-proj/covidualize/CanadaCovidDeath.csv")
    covidCanadaTotalRecovered_df = pandas.read_csv(
        "~/Desktop/SCHOOL/cmpt-340/term-proj/covidualize/CanadaCovidRecovered.csv")
    # Remove the columns we don't care about
    covidCanadaTotalCases_df = covidCanadaTotalCases_df.drop(
        ['Country/Region', 'Lat', 'Long'], axis=1)

    # if DEBUG:
    #     print(covidCanadaTotalCases_df)

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

    # if DEBUG:
    #     print(covidAB_df)

    # Drop the province column and sum them all up to create the total per day for all provinces. Convert from series to df for Altair
    covidCanadaTotalCases_df = covidCanadaTotalCases_df.drop(
        ['Province'], axis=1)
    covidCanadaTotal_df = covidCanadaTotalCases_df.sum(axis=0, skipna=True)
    covidCanadaTotal_df = covidCanadaTotal_df.to_frame()
    covidCanadaTotal_df.columns = columninds
    covidCanadaTotal_df.index.name = 'Date'
    covidCanadaTotal_df.reset_index(inplace=True)
    # print(covidCanadaTotal_df)

    # Drop all columns for Deaths. Convert them to the same form as total cases above.
    covidCanadaTotalDeaths_df = covidCanadaTotalDeaths_df.drop(
        ['Province', 'Country/Region', 'Lat', 'Long'], axis=1)
    covidCanadaTotalDeaths_df = covidCanadaTotalDeaths_df.sum(
        axis=0, skipna=True)
    covidCanadaTotalDeaths_df = covidCanadaTotalDeaths_df.to_frame()
    covidCanadaTotalDeaths_df.columns = ['Deaths']
    covidCanadaTotalDeaths_df.index.name = 'Date'
    covidCanadaTotalDeaths_df.reset_index(inplace=True)
    # print(covidCanadaTotalDeaths_df)

    # Recovered is not by province so requires less clean up.
    covidCanadaTotalRecovered_df = covidCanadaTotalRecovered_df.transpose()
    covidCanadaTotalRecovered_df.columns = ['Recoveries']
    covidCanadaTotalRecovered_df.index.name = 'Date'
    covidCanadaTotalRecovered_df.reset_index(inplace=True)
    # print(covidCanadaTotalRecovered_df)

    covidCanadaTotal_df['Active Cases'] = covidCanadaTotal_df.Cases - \
        (covidCanadaTotalDeaths_df.Deaths + covidCanadaTotalRecovered_df.Recoveries)
    # print(covidCanadaTotal_df)

    # chart = alt.Chart(covidCanadaTotal_df).mark_line().encode(
    #     x='Date',
    #     y='Active Cases'
    # ).interactive()

    # chart.show()

    # if DEBUG:
    #     print(covidCanadaTotal_df)

    return covidCanadaTotal_df, covidCanadaTotalDeaths_df, covidCanadaTotalRecovered_df, covidAB_df, covidBC_df, covidMN_df, covidNB_df, covidNL_df, covidNS_df, covidON_df, covidPE_df, covidQC_df, covidSA_df


def main():
    covidCanadaTotal_df, covidCanadaTotalDeaths_df, covidCanadaTotalRecovered_df, covidAB_df, covidBC_df, covidMN_df, covidNB_df, covidNL_df, covidNS_df, covidON_df, covidPE_df, covidQC_df, covidSA_df = dataImport()
    listDF = [covidCanadaTotal_df, covidCanadaTotalDeaths_df, covidCanadaTotalRecovered_df, covidAB_df, covidBC_df, covidMN_df, covidNB_df,
              covidNL_df, covidNS_df, covidON_df, covidPE_df, covidQC_df, covidSA_df]
    trainData(listDF)
    return


main()
