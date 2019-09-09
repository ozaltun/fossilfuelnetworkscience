import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import collections
import powerlaw
import community
import operator

def get_raw_data():
    # This is the function used to get all the raw data

    #Extracting all the data
    df2016 = pd.ExcelFile("resourceTradeData/resourcetradeearth-all-all-4-2016.xlsx")
    df2011 = pd.ExcelFile("resourceTradeData/resourcetradeearth-all-all-4-2011.xlsx")
    df2006 = pd.ExcelFile("resourceTradeData/resourcetradeearth-all-all-4-2006.xlsx")
    df2001 = pd.ExcelFile("resourceTradeData/resourcetradeearth-all-all-4-2001.xlsx")

    #Taking out the Trades tab from the excel sheet
    trades_df2016 = df2016.parse('Trades')
    trades_df2011 = df2011.parse('Trades')
    trades_df2006 = df2006.parse('Trades')
    trades_df2001 = df2001.parse('Trades')

    trades_df2016 = trades_df2016[pd.isnull(trades_df2016['Exporter ISO3'])==False]
    trades_df2011 = trades_df2011[pd.isnull(trades_df2011['Exporter ISO3'])==False]
    trades_df2006 = trades_df2006[pd.isnull(trades_df2006['Exporter ISO3'])==False]
    trades_df2001 = trades_df2001[pd.isnull(trades_df2001['Exporter ISO3'])==False]


    trades_df2016 = trades_df2016[pd.isnull(trades_df2016['Importer ISO3'])==False]
    trades_df2011 = trades_df2011[pd.isnull(trades_df2011['Importer ISO3'])==False]
    trades_df2006 = trades_df2006[pd.isnull(trades_df2006['Importer ISO3'])==False]
    trades_df2001 = trades_df2001[pd.isnull(trades_df2001['Importer ISO3'])==False]

    return trades_df2016, trades_df2011, trades_df2006, trades_df2001

def get_gas_data(trades_df2016, trades_df2011, trades_df2006, trades_df2001):
    #Extracting the NG
    gasTrades_2016 = trades_df2016.loc[trades_df2016['Resource'] == 'Gas']
    gasTrades_2011 = trades_df2011.loc[trades_df2011['Resource'] == 'Gas']
    gasTrades_2006 = trades_df2006.loc[trades_df2006['Resource'] == 'Gas']
    gasTrades_2001 = trades_df2001.loc[trades_df2001['Resource'] == 'Gas']
    #Taking out all 'nan' values
    gasTrades_2016 = gasTrades_2016[np.isnan(gasTrades_2016['Weight (1000kg)'])==False]
    gasTrades_2011 = gasTrades_2011[np.isnan(gasTrades_2011['Weight (1000kg)'])==False]
    gasTrades_2006 = gasTrades_2006[np.isnan(gasTrades_2006['Weight (1000kg)'])==False]
    gasTrades_2001 = gasTrades_2001[np.isnan(gasTrades_2001['Weight (1000kg)'])==False]

    gasTrades_Total = gasTrades_2016.append(gasTrades_2011.append(gasTrades_2006.append(gasTrades_2001)))

    return gasTrades_Total


def get_oil_data(trades_df2016, trades_df2011, trades_df2006, trades_df2001):
    #Extracting the Oil
    oilTrades_2016 = trades_df2016.loc[trades_df2016['Resource'] == 'Oil']
    oilTrades_2011 = trades_df2011.loc[trades_df2011['Resource'] == 'Oil']
    oilTrades_2006 = trades_df2006.loc[trades_df2006['Resource'] == 'Oil']
    oilTrades_2001 = trades_df2001.loc[trades_df2001['Resource'] == 'Oil']
    #Taking out all 'nan' values
    oilTrades_2016 = oilTrades_2016[np.isnan(oilTrades_2016['Weight (1000kg)'])==False]
    oilTrades_2011 = oilTrades_2011[np.isnan(oilTrades_2011['Weight (1000kg)'])==False]
    oilTrades_2006 = oilTrades_2006[np.isnan(oilTrades_2006['Weight (1000kg)'])==False]
    oilTrades_2001 = oilTrades_2001[np.isnan(oilTrades_2001['Weight (1000kg)'])==False]

    oilTrades_Total = oilTrades_2016.append(oilTrades_2011.append(oilTrades_2006.append(oilTrades_2001)))

    return oilTrades_Total


def get_coal_data(trades_df2016, trades_df2011, trades_df2006, trades_df2001):
    #Extracting the NG
    coalTrades_2016 = trades_df2016.loc[trades_df2016['Resource'] == 'Coal']
    coalTrades_2011 = trades_df2011.loc[trades_df2011['Resource'] == 'Coal']
    coalTrades_2006 = trades_df2006.loc[trades_df2006['Resource'] == 'Coal']
    coalTrades_2001 = trades_df2001.loc[trades_df2001['Resource'] == 'Coal']
    #Taking out all 'nan' values
    coalTrades_2016 = coalTrades_2016[np.isnan(coalTrades_2016['Weight (1000kg)'])==False]
    coalTrades_2011 = coalTrades_2011[np.isnan(coalTrades_2011['Weight (1000kg)'])==False]
    coalTrades_2006 = coalTrades_2006[np.isnan(coalTrades_2006['Weight (1000kg)'])==False]
    coalTrades_2001 = coalTrades_2001[np.isnan(coalTrades_2001['Weight (1000kg)'])==False]

    coalTrades_Total = coalTrades_2016.append(coalTrades_2011.append(coalTrades_2006.append(coalTrades_2001)))

    return coalTrades_Total


def get_data():

    # Getting necessary data and cleaning
    trades_df2016, trades_df2011, trades_df2006, trades_df2001 = get_raw_data()
    gasTrades_Total = get_gas_data(trades_df2016, trades_df2011, trades_df2006, trades_df2001)
    coalTrades_Total = get_coal_data(trades_df2016, trades_df2011, trades_df2006, trades_df2001)
    oilTrades_Total = get_oil_data(trades_df2016, trades_df2011, trades_df2006, trades_df2001)

    trades_Total = trades_df2016.append(trades_df2011.append(trades_df2006.append(trades_df2001)))

    return trades_df2016, trades_df2011, trades_df2006, trades_df2001, trades_Total, gasTrades_Total, coalTrades_Total, oilTrades_Total


def exports_imports_plot(Trades_Total, fuel_type):
    tonsExportedW = list()
    tonsImportedW = list()

    tonsExportedV = list()
    tonsImportedV = list()
    years = sorted(Trades_Total['Year'].unique())

    for i in years:
        data = Trades_Total[Trades_Total['Year'] == i]
        data3 = data[data['Importer ISO3'] == 'USA']
        data2 = data[data['Exporter ISO3'] == 'USA']
        sumDollarsI = np.sum(data3['Value (1000USD)'])/1e6
        sumDollars = np.sum(data2['Value (1000USD)'])/1e6
        tonsImportedV.append((i, sumDollarsI))
        tonsExportedV.append((i, sumDollars))

        sumTonsI = np.sum(data3['Weight (1000kg)'])/1e6
        sumTons = np.sum(data2['Weight (1000kg)'])/1e6
        tonsImportedW.append((i, sumTonsI))
        tonsExportedW.append((i, sumTons))

    x, y = zip(*tonsExportedW)
    x2, y2 = zip(*tonsImportedW)
    plt.plot(x,y, color='b')
    plt.plot(x2, y2, color='r')
    plt.close()

    x, y = zip(*tonsExportedV)
    x2, y2 = zip(*tonsImportedV)
    plt.plot(x,y, label ='Exported')
    plt.plot(x2, y2, label = 'Imported')
    plt.legend()
    plt.ylabel('Billions of $')
    plt.xlabel('Year')
    plt.title('{} Exports/Imports'.format(fuel_type))

    plt.show()
    plt.close()

def genDegreeMatrix4Year(dataFrame, map2Row, year):
    energyYear = dataFrame[dataFrame.Year == year]
    energyYear_weight = energyYear.groupby(['Exporter ISO3','Importer ISO3' ])['Weight (1000kg)'].sum().reset_index()

    numberOfCountries = len(map2Row)
    columnList = range(0, numberOfCountries)

    finalMatrix = pd.DataFrame(np.zeros((numberOfCountries, 2), dtype= int), index=columnList, columns=['InDegree','OutDegree'])

    G = nx.from_pandas_edgelist(energyYear_weight,'Exporter ISO3',
                                    'Importer ISO3', ['Weight (1000kg)'],
                                    create_using=nx.DiGraph())
    for d in G.nodes:
        rowNumber = map2Row[d]
        finalMatrix['InDegree'][columnList[rowNumber]] = G.in_degree[d]
        finalMatrix['OutDegree'][columnList[rowNumber]] = G.out_degree[d]

    return finalMatrix

#Create a function that runs a for loop for all years

def genDegreeMatrix4AllYears(dataFrame, map2Row):
    years = sorted(dataFrame['Year'].unique())
    dicYears = {}
    for i in years:
        dicYears[i] = None

    for i in years:
        dicYears[i] = genDegreeMatrix4Year(dataFrame, map2Row, i)

    return dicYears

def in_out_degree_plot(graph, map2Row, fuel_type):
    in_degree = list()
    out_degree = list()

    for i in graph.keys():
        in_degree.append((i, graph[i]['InDegree'][map2Row['USA']]))
        out_degree.append((i, graph[i]['OutDegree'][map2Row['USA']]))

    x, y = zip(*in_degree)
    plt.subplot(2,1,1)

    plt.scatter(x,y)
    plt.ylabel('In Degree')
    plt.title('US {} Trade Partners'.format(fuel_type))


    x, y = zip(*out_degree)
    plt.subplot(2,1,2)
    plt.scatter(x,y)
    plt.ylabel('Out Degree')

    plt.show()
    plt.close()


def power_compared2_expo(dataAll):
    final = list()
    for i in dataAll.keys():
        data_in = np.array(dataAll[i]['OutDegree'])
        data_out = np.array(dataAll[i]['InDegree'])
        data = data_in+data_out
        data = data[data>0]
        fitInitial = powerlaw.Fit(data, discrete=True)
        R, p = fitInitial.distribution_compare('power_law','exponential')
        final.append((i, R, p))
    return final

def plotting_power_compared2_expontial(gasDegree, oilDegree, coalDegree, totalDegree, save=False):
    dictionary  = {}

    gasPL = power_compared2_expo(gasDegree)
    year, Rgas, pgas = zip(*gasPL)
    dictionary['gas'] = [Rgas, pgas]

    oilPL = power_compared2_expo(oilDegree)
    year, Roil, poil = zip(*oilPL)
    dictionary['oil'] = [Roil, poil]

    coalPL = power_compared2_expo(coalDegree)
    year, Rcoal, pcoal = zip(*coalPL)
    dictionary['coal'] = [Rcoal, pcoal]

    totalPL = power_compared2_expo(totalDegree)
    year, Rtotal, ptotal = zip(*totalPL)
    dictionary['total'] = [Rtotal, ptotal]

    #plt.subplot(1, 1, 1)
    fig, axes = plt.subplots(4, 2, figsize=(8,16))
    fig.suptitle('Plots of loglikelihood ratio between power law and exponential distributions', fontsize=16)

    for i, fuel in enumerate(['gas', 'oil', 'coal','total']):
        axes[i,0].scatter(year, dictionary[fuel][0])
        axes[i,0].set_title('Loglikelihood ratio of {}'.format(fuel))
        axes[i,0].set_ylabel('Loglikelihood')
        axes[i,0].axhline(y=0)

        axes[i,1].scatter(year, dictionary[fuel][1])
        axes[i,1].set_title('Probability ratio of {}'.format(fuel))
        axes[i,1].set_ylabel('Probability')
        axes[i,1].set_ylim([0,1])

    if save == True:
        plt.savefig('figures/power_compared2_exponential.eps', format='eps')


    plt.show()
    plt.close()

def inDoutDtotD(dataAll):
    final = list()
    for i in dataAll.keys():
        data_in = np.array(dataAll[i]['InDegree'])
        data_out = np.array(dataAll[i]['OutDegree'])
        data = data_in+data_out
        meanTot = np.mean(data)
        final.append((i, meanTot))
    return final

def connectivity_plot(gasDegree, oilDegree, coalDegree, totalDegree):
    gasD = inDoutDtotD(gasDegree)
    year,meanTotgas = zip(*gasD)

    oilD = inDoutDtotD(oilDegree)
    year,  meanTotoil = zip(*oilD)

    coalD = inDoutDtotD(coalDegree)
    year, meanTotcoal = zip(*coalD)

    totalD = inDoutDtotD(totalDegree)
    year, meanTottotal = zip(*totalD)


    plt.plot(year, meanTotgas, label = 'Gas')
    plt.plot(year, meanTotoil, label = 'Oil')
    plt.plot(year, meanTotcoal, label = 'Coal')
    plt.legend()
    plt.title('Average Degree')
    plt.xlabel('Year')
    plt.ylabel('Degree')

    plt.show()
    plt.close()


def genGraph4Year(dataFrame, year):
    energyYear = dataFrame[dataFrame.Year == year]
    energyYear_weight = energyYear.groupby(['Exporter ISO3','Importer ISO3' ])['Weight (1000kg)'].sum().reset_index()
    energyYear_Value = energyYear.groupby(['Exporter ISO3','Importer ISO3' ])['Value (1000USD)'].sum().reset_index()
    G_weight = nx.from_pandas_edgelist(energyYear_weight,'Exporter ISO3',
                                    'Importer ISO3', ['Weight (1000kg)'],
                                    create_using=nx.DiGraph())
    G_value = nx.from_pandas_edgelist(energyYear_Value,'Exporter ISO3',
                                    'Importer ISO3', ['Value (1000USD)'],
                                    create_using=nx.DiGraph())

    return G_weight, G_value


def pageRank(dataFrame, year):
    weightG, valueG = genGraph4Year(dataFrame, year)
    dicPRWeight = nx.pagerank_numpy(weightG, weight='Weight (1000kg)')
    sortedPRWeight = sorted(dicPRWeight.items(), key=operator.itemgetter(1), reverse = True)
    dicPRValue = nx.pagerank_numpy(valueG, weight='Value (1000USD)')
    sortedPRValue = sorted(dicPRValue.items(), key=operator.itemgetter(1), reverse = True)
    return sortedPRWeight, sortedPRValue



def authority_matrix(G, nodelist=None, weight = 'weight'):
    """Return the HITS authority matrix."""
    M = nx.to_numpy_matrix(G, nodelist=nodelist, weight = weight)
    return M.T * M



def hub_matrix(G, nodelist=None, weight = 'weight'):
    """Return the HITS hub matrix."""
    M = nx.to_numpy_matrix(G, nodelist=nodelist, weight = weight)
    return M * M.T



def hits_numpy(G, weight='weight', normalized=True):
    if len(G) == 0:
        return {}, {}
    H = hub_matrix(G, list(G), weight = weight)
    e, ev = np.linalg.eig(H)
    m = e.argsort()[-1]  # index of maximum eigenvalue
    h = np.array(ev[:, m]).flatten()
    A = authority_matrix(G, list(G), weight = weight)
    e, ev = np.linalg.eig(A)
    m = e.argsort()[-1]  # index of maximum eigenvalue
    a = np.array(ev[:, m]).flatten()
    if normalized:
        h = h / h.sum()
        a = a / a.sum()
    else:
        h = h / h.max()
        a = a / a.max()
    hubs = dict(zip(G, map(float, h)))
    authorities = dict(zip(G, map(float, a)))
    return hubs, authorities


def weightedHITS(dataFrame, year):
    import operator
    weightG, valueG = genGraph4Year(dataFrame, year)

    dictWeightH, dictWeightA= hits_numpy(weightG, weight='Weight (1000kg)')
    sortedWeightH = sorted(dictWeightH.items(), key=operator.itemgetter(1), reverse = True)
    sortedWeightA = sorted(dictWeightA.items(), key=operator.itemgetter(1), reverse = True)


    dictValueH, dictValueA = hits_numpy(valueG, weight='Value (1000USD)')
    sortedValueH = sorted(dictValueH.items(), key=operator.itemgetter(1), reverse = True)
    sortedValueA = sorted(dictValueA.items(), key=operator.itemgetter(1), reverse = True)

    return sortedWeightH, sortedWeightA, sortedValueH, sortedValueA

def HITS(dataFrame, year):
    import operator
    weightG, valueG = genGraph4Year(dataFrame, year)
    dicHWeight, dicAWeight = nx.hits(weightG)
    sortedWeightH = sorted(dicHWeight.items(), key=operator.itemgetter(1), reverse = True)
    sortedWeightA = sorted(dicAWeight.items(), key=operator.itemgetter(1), reverse = True)
    return sortedWeightH, sortedWeightA
