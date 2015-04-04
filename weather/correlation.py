#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def string2Date(s):
    return datetime.strptime("-".join([s[:4],s[4:6],s[6:]]),"%Y-%m-%d")

def mean(l):
    return float(sum(l))/len(l)

def varianceP (l1):
    avg = mean(l1)
    return float(sum(map(lambda x:(x-avg)*(x-avg),l1)))/len(l1)

def stdevP (l1):
    return math.sqrt(varianceP(l1))

def covariance (l1, l2):
    avg1 = mean(l1)
    avg2 = mean(l2)
    return float(sum(map(lambda x:(x[0]-avg1)*(x[1]-avg2),zip(l1,l2))))/len(l1)

def correlation (l1, l2):
    std1 = stdevP(l1)
    std2 = stdevP(l2)
    prod = std1 * std2
    if (prod == 0):
        return -10
    return covariance(l1,l2)/(std1*std2)
    
def readDownJones(fname):
    djl = [i.strip().split(",") for i in open(fname).readlines()]
    djl = [(i[0],float(i[1])) for i in djl]
    return djl

def readTemps(fname):
    temps = [i.strip().split(",") for i in open(fname).readlines()]
    temps = [(i[0],i[1],float(i[2])/10.0) for i in temps]
    dicTemps = dict()
    for i in temps:
        if dicTemps.has_key(i[0]):
            dicTemps[i[0]].append((i[1],i[2]))
        else:
            dicTemps[i[0]] = list()
    return dicTemps

def correlation_station (stationName, temps, dji):
    temps_l = temps[stationName]
    temps_l.sort(key=lambda tup: tup[0])
    date_temp = [i[0] for i in temps_l]
    date_dji  = [i[0] for i in dji]
    date_unif = [filter(lambda x: x in date_dji, [sublist]) for sublist in date_temp]
    date_unif = [i[0] for i in date_unif if len(i)>0]
    if len(date_unif)==0:
        return -10;
    l_temp = [i for i in temps_l if i[0] in date_unif]
    l_dji  = [i for i in dji if i[0] in date_unif]
    if (len(l_temp)< 2 or len(l_dji) < 2):
        return -10;
    else:
        return (correlation([i[1] for i in l_temp], [i[1] for i in l_dji]), len(l_temp))
    
def plot_station (stationName, temps, dji):
    temps_l = temps[stationName]
    temps_l.sort(key=lambda tup: tup[0])
    date_temp = [i[0] for i in temps_l]
    date_dji  = [i[0] for i in dji]
    date_unif = [filter(lambda x: x in date_dji, [sublist]) for sublist in date_temp]
    date_unif = [i[0] for i in date_unif if len(i)>0]
    if len(date_unif)==0:
        return -10;
    l_temp = [i for i in temps_l if i[0] in date_unif]
    l_dji  = [i for i in dji if i[0] in date_unif]
    if (len(l_temp)< 2 or len(l_dji) < 2):
        return
    x = [string2Date(i) for i in date_unif]
    y = [i[1] for i in l_temp]
    z = [i[1] for i in l_dji]
    with plt.style.context('fivethirtyeight'):
        fig, ax = plt.subplots()
        line1 = ax.plot(x, y,'o')
        plt.title('daily high-temp in Riverhead, NY ')

        plt.ylabel("high temp ºC".decode("utf-8"))
        ax2 = fig.add_subplot(111, sharex=ax, frameon=False)
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        plt.ylabel ("Dow Jones Index")
        line2 = ax2.plot(x, z, 'r-')
        blue_line = mlines.Line2D([], [], color='blue', label='Temp')
        reds_line = mlines.Line2D([], [], color='red', label='DowJones')
        plt.legend(bbox_to_anchor=(1, 1),
           bbox_transform=plt.gcf().transFigure, handles=[blue_line,reds_line])

        plt.show()


def main (param = "print"):
    djil = readDownJones("DJCA_2014.csv")
    djil.sort(key=lambda tup: tup[0])
    temps = readTemps("2014_TMAX_US.csv")
    if (param == "print"):
        print "Station, Correlation, #Samples"
        for i in temps.keys():
            if len(temps[i])>10:
                corr = correlation_station (i, temps, djil )
                print "%s,%f,%d"%(i, corr[0], corr[1])
    else:
        plot_station (param,temps,djil)

#
# usage correlation.py [code of meterological station]
# with no parameter will print all correlation
# with parameter will plot the graph of the selected station and DJCA
#
if __name__ == "__main__":
    import sys
    if (len(sys.argv)>1):
        main (sys.argv[1])
    else:
        main()
