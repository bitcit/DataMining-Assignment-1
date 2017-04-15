# -*- coding: UTF-8 -*-
__author__ = 'Baicheng Zhao'
import matplotlib
import matplotlib.pyplot as plt
import pylab as pl
import scipy.stats as stats
import json

def readFile(path):
    fileObj=open(path)
    data=fileObj.read()
    return data

def show():
    data=readFile("data/numericData_cleaned.json")
    data=json.loads(data)
    for key in data.keys():
        dataCell=data[key]
        
        #histogram
        pl.figure()
        pl.hist(dataCell,bins=50,normed=True)
        plt.title(key+"_histogram")
        pl.savefig("image/origin_dataVisual/"+key+"_histogram.png")
        pl.close()
        
        #QQ plot
        pl.figure()
        stats.probplot(dataCell,dist="norm",plot=plt)
        plt.title(key+"_qq plot")
        plt.savefig("image/origin_dataVisual/"+key+"_qq_plot.png")
        plt.close()
        
        #box plot
        fig=plt.figure(1,figsize=(9,6))
        axes=fig.add_subplot(111)
        boxplot=axes.boxplot(dataCell)
        plt.title(key+"_box plot")
        fig.savefig("image/origin_dataVisual/"+key+"_box_plot.png",bbox_inches="tight")
        plt.close()

if __name__=="__main__":
    show()
