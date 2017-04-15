# -*- coding: UTF-8 -*-
__author__ = 'Baicheng Zhao'

import figCompare as fc
import pandas as pd
import numpy as np
import math
import operator
import json

col=['surgery','Age','Hospital_Number','rectal_temperature','pulse','respiratory_rate','temperature_of_extremities',
    'peripheral_pulse','mucous_membranes','capillary_refill_time','pain','peristalsis','abdominal_distension','nasogastric_tube',
    'nasogastric_reflux','nasogastric_reflux_PH','rectal_examination_feces','abdomen','packed_cell_volume','total_protein',
    'abdominocentesis_appearance','abdomcentesis_total_protein','outcome','surgical_lesion','type_of_lesion_1','type_of_lesion_2',
    'type_of_lesion_3','cp_data']

#标称属性部分
nominal_attribute=['surgery','Age','temperature_of_extremities',
                  'peripheral_pulse','mucous_membranes','nasogastric_reflux',
                   'rectal_examination_feces','abdomen', 'abdominocentesis_appearance',
                  'outcome','cp_data']
#数值属性部分
numeric_attribute=['rectal_temperature','pulse','respiratory_rate','nasogastric_reflux_PH',
                  'packed_cell_volume','total_protein','abdomcentesis_total_protein']

data_origin=pd.read_table("data/horse-colic.data.txt", sep=' ',names=col,na_values = "?")


#该部分对缺失值采取剔除
def filtrating_delete(data_origin):
    data_origin_temp=data_origin.copy()
    cols=[]
    for i in range(0,len(data_origin_temp)):
        flag=0
        for j in range(0,len(data_origin_temp.iloc[i])):
            if(math.isnan(data_origin_temp.iloc[i][j])):
                flag=1
                break
        if(flag==0):
            cols.append(i)
    
    data_filtrated=data_origin_temp.iloc[cols,:]
    data_filtrated.to_csv("data/data_filtrated_delete.csv")

    fc.plot_compare(data_origin,data_filtrated,"image/handle_data/missing_data_delete.png")

#该部分使用最高频率的值来填补缺失值
def filtrating_filledByMost(data_origin):
    data_filtrated=data_origin.copy()
    for item in nominal_attribute+numeric_attribute:
        most_frequent_value=data_filtrated[item].value_counts().idxmax()
        data_filtrated[item].fillna(value=most_frequent_value,inplace=True)

    data_filtrated.to_csv("data/data_filtrated_filledByMost.csv")
    fc.plot_compare(data_origin,data_filtrated,"image/handle_data/missing_data_filledByMost.png")

#该部分使用相关关系进行缺失值得填补
def filtrating_illedByCorelation(data_origin):
    data_filtrated = data_origin.copy()
    for item in numeric_attribute:
        data_filtrated[item].interpolate(inplace = True)
    data_filtrated.to_csv("data/data_filtrated_filledByCorelation.csv")
    fc.plot_compare(data_origin,data_filtrated,"image/handle_data/missing_data_filledByCorelation.png")


#该部分使用相似性进行缺失值的填补
def dist_compute(data_origin):
     #将数据进行标准化
    data_toNormal= data_origin.copy()
    data_toNormal[numeric_attribute] = data_toNormal[numeric_attribute].fillna(0)
    data_toNormal[numeric_attribute] = data_toNormal[numeric_attribute].apply(lambda x : (x - np.mean(x)) / (np.max(x) - np.min(x)))
    #利用dist{}来表示各个元组之间的相关程度，dist越大越不相关
    dist={}
    num=len(data_origin)
    for i in range(0,num):
        dist[i]={}
        for j in range(0,num):
            dist[i][j]=0
    #计算各个属性之间的dist值
    for i in range(0,num):
        for j in range(i,num):
            for item in nominal_attribute:
                if data_toNormal.iloc[i][item]!=data_toNormal.iloc[j][item]:
                    dist[i][j]+=1
            for item in numeric_attribute:
                dist[i][j]+=abs(data_toNormal.iloc[i][item]-data_toNormal.iloc[j][item])
            dist[j][i]=dist[i][j]
  #  with open('data/dist.json', 'w') as f:
   # json.dump(data, f)
    return dist


def filtrating_filledBySimilar(data_origin):
    #计算dist值，该过程计算比较耗时，所以，在该处把运行一遍后的dist存下来，下次直接调用
    #dist=dist_compute(data_origin)
    with open('data/dist.json', 'r') as f:
        dist = json.load(f)
    data_filtrated = data_origin.copy()
    nan_list = pd.isnull(data_origin).any(1).nonzero()[0]  #取出有缺失值元组的索引
    for index in nan_list:
        nearest = int(sorted(dist[str(index)].items(), key=operator.itemgetter(1), reverse = False)[1][0])
        #当直接计算dist时，用下面一条语句代替上面一条语句（因为将dist存为json文件时，key的值自动从int转为str类型）
        #nearest = sorted(dist[index].items(), key=operator.itemgetter(1), reverse = False)[1][0]
        for item in numeric_attribute+nominal_attribute:
            if pd.isnull(data_filtrated.iloc[index][item]):
                if pd.isnull(data_origin.iloc[nearest][item]):
                    data_filtrated.ix[index, item] = data_origin[item].value_counts().idxmax()
                else:
                    data_filtrated.ix[index, item] = data_origin.iloc[nearest][item]
    data_filtrated.to_csv("data/data_filtrated_filledBySimilar.csv")
    fc.plot_compare(data_origin,data_filtrated,"image/handle_data/missing_data_filledBySimilar.png")


if __name__=="__main__":
    filtrating_delete(data_origin)  #该部分对缺失值采取剔除
    filtrating_filledByMost(data_origin)  #该部分使用最高频率的值来填补缺失值
    filtrating_illedByCorelation(data_origin)  #该部分使用相关关系进行缺失值得填补
    filtrating_filledBySimilar(data_origin)  #该部分使用相似性进行缺失值的填补
        
