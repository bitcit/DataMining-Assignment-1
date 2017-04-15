# -*- coding: UTF-8 -*-
__author__ = 'Baicheng Zhao'

import matplotlib.pyplot as plt
import pandas as pd


nominal_attribute=['surgery','Age','temperature_of_extremities',
                  'peripheral_pulse','mucous_membranes','nasogastric_reflux',
                   'rectal_examination_feces','abdomen', 'abdominocentesis_appearance',
                  'outcome','cp_data']
numeric_attribute=['rectal_temperature','pulse','respiratory_rate','nasogastric_reflux_PH',
                  'packed_cell_volume','total_protein','abdomcentesis_total_protein']
#绘制对比图
def plot_compare(data_origin,data_filtrated,save_path):
    fig=plt.figure(figsize=(25,16))
    i=1
    for item in nominal_attribute:
        ax=fig.add_subplot(5,4,i)
        ax.set_title(item)
        pd.value_counts(data_origin[item].values).plot(ax = ax, marker = '^', label = 'origin', legend = True)
        pd.value_counts(data_filtrated[item].values).plot(ax = ax, marker = 'o', label = 'filtrated', legend = True)
        i=i+1

    for item in numeric_attribute:
        ax = fig.add_subplot(5, 4, i)
        ax.set_title(item)
        data_origin[item].astype(float).plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'origin', color='g',legend = True)
        data_filtrated[item].astype(float).plot(ax = ax, alpha = 0.5, kind = 'hist', label = 'filtrated', color='y',legend = True)
        ax.axvline(data_origin[item].astype(float).mean(), color = 'r')
        ax.axvline(data_filtrated[item].astype(float).mean(), color = 'b')
        i=i+1
    plt.subplots_adjust(wspace=0.3,hspace=0.3)

    fig.savefig(save_path)
