# -*- coding: utf-8 -*-
"""
Created on Fri Dec 09 11:25:56 2016
#
@author: aidan.parkinson
"""

# import required packages

import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

import math, random

#
# # set working directory and print
#
# #dir_path = os.path.dirname(__file__)
# #os.chdir(dir_path)
#
# print(os.getcwd())

# wb = openpyxl.load_workbook("2017-02-07_Lifecycle Cost Model.xlsx", data_only=True)

# import building

# size_of_factor_sample = 1000

size_of_factor_sample = 1000

number_of_element_cost_samples = 1000

class Building():

    def __init__(self, wb, name):
        self.name = name
        self.ws = wb.get_sheet_by_name(self.name)

    def build_data_for_building_lifetime(self, building_life):
        ws = self.ws
        self.dRate = ws["G3"].value*ws["G5"].value+ws["G4"].value+ws["G2"].value

        element_count = ws.max_row - 16

        self.elements_cost_for_building_lifes = []

        for i_sample in range(size_of_factor_sample):

            self.elements_cost_for_building_life = []

            for i_element in range(element_count):
                row = i_element+17



                if ws["J" + str(row)].value is None: continue

     #           self.element_lifetime = np.ones([size_of_factor_sample])

                distribution = ws["O"+ str(row)].value
                mean = ws["M" + str(row)].value
                stdDeviation = ws["N" + str(row)].value

                if distribution == "Normal":
                    dist = np.random.normal(
                        mean,
                        stdDeviation,
                        size_of_factor_sample
                    )

    #                    elif distributionType == 'Log-normal':
    #                        print mean, math.log(standardError-mean)/1.64, size_of_factor_sample
    #                        dist = np.random.lognormal(
    #                            mean,
    #                            math.log(standardError-mean)/1.64,
    #                            size_of_factor_sample
    #                        )

                elif distribution == "Gumbel":
                    dist = np.ones(size_of_factor_sample)+np.ones(size_of_factor_sample)-np.random.gumbel(
                        mean,
                        stdDeviation,
                        size_of_factor_sample
                    )

                else:
                    dist = np.ones(size_of_factor_sample)

    #            self.element_lifetime = np.ones(size_of_factor_sample)*ws["J" + str(row)].value

                self.element_lifetime = dist*ws["J" + str(row)].value

                def element_netpv(yrs):
    #                print ws["H"+ str(row)].value, (1+self.dRate)**yrs
                    return ws["H"+ str(row)].value/(1+self.dRate)**yrs

                self.cost_of_first_failures = [element_netpv(y) for y in self.element_lifetime]

                def element_cost_for_building_life():
                    cost = 0
                    yrs = 0
                    while True:
                        i = random.choice(range(size_of_factor_sample))
                        yrs += self.element_lifetime[i]
                        if yrs < building_life:
                            cost += self.cost_of_first_failures[i]
                        else:
    #                        print cost
                            return -cost

 #               print "Done Row " + str(17+i_element)
  #              print element_cost_for_building_life()

                self.elements_cost_for_building_life.append(element_cost_for_building_life())

            self.elements_cost_for_building_lifes.append(self.elements_cost_for_building_life)

        self.elements_cost_for_building_lifes = np.transpose(self.elements_cost_for_building_lifes)

    def cost_for_building_life(self):
        cost = 0
        for i in range(len(self.elements_cost_for_building_lifes)):
            cost += self.elements_cost_for_building_lifes[i][random.choice(range(number_of_element_cost_samples))]
        return cost

    def costs_for_building_lifes(self, n_estimates):
        dataPlot = [self.cost_for_building_life() for i in range(n_estimates)]
#        print dataPlot
        self.figureData = [
                           go.Histogram(
                                  x = dataPlot,
                                  histnorm = "probability",
                                  xbins = dict(
                                               start = min(dataPlot),
                                               end = max(dataPlot),
                                               size = round((max(dataPlot)-min(dataPlot))/40,
                                                            -int(math.floor(math.log10(abs((max(dataPlot)-min(dataPlot))/40))))
                                                      ),
                                  ),
                            ),
        ]
        self.figureLayout = go.Layout(
                                 title = self.name,
                                 xaxis = dict(
                                              title = "Net Present Value / £"
                                 ),
                                 yaxis = dict(
                                              title = "Probability"
                                 ),
                                 bargap = 0.25
                            )
        self.figure = go.Figure(data = self.figureData, layout = self.figureLayout)
        return py.plot(self.figure)
