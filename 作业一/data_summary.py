# -*- coding: UTF-8 -*-
__author__ = 'Baicheng Zhao'

import pandas as pd
import numpy as np
import json
import math
col=['surgery','Age','Hospital_Number','rectal_temperature','pulse','respiratory_rate','temperature_of_extremities',
    'peripheral_pulse','mucous_membranes','capillary_refill_time','pain','peristalsis','abdominal_distension','nasogastric_tube',
    'nasogastric_reflux','nasogastric_reflux_PH','rectal_examination_feces','abdomen','packed_cell_volume','total_protein',
    'abdominocentesis_appearance','abdomcentesis_total_protein','outcome','surgical_lesion','type_of_lesion_1','type_of_lesion_2',
    'type_of_lesion_3','cp_data']
data_origin = pd.read_table("data/horse-colic.data.txt",names=col,na_values = "?",sep=' ')
data_origin.to_csv("data/horse-colic.data.csv") #将原始数据存入csv文件中

#标称属性部分
nominal_attribute=['surgery','Age','temperature_of_extremities',
                  'peripheral_pulse','mucous_membranes','nasogastric_reflux',
                   'rectal_examination_feces','abdomen', 'abdominocentesis_appearance',
                  'outcome','cp_data']
#数值属性部分
numeric_attribute=['rectal_temperature','pulse','respiratory_rate','nasogastric_reflux_PH',
                  'packed_cell_volume','total_protein','abdomcentesis_total_protein']

#对数据进行初始化
def init():
    #获取标称属性
    data=data_origin
    nominalData={}
    nominalData[col[0]]=data[col[0]]
    nominalData[col[1]]=data[col[1]]
    nominalData[col[6]]=data[col[6]]
    nominalData[col[7]]=data[col[7]]
    nominalData[col[8]]=data[col[8]]
    nominalData[col[9]]=data[col[9]]
    nominalData[col[14]]=data[col[14]]
    nominalData[col[16]]=data[col[16]]
    nominalData[col[17]]=data[col[17]]
    nominalData[col[20]]=data[col[20]]
    nominalData[col[22]]=data[col[22]]
    nominalData[col[23]]=data[col[23]]
    nominalData[col[27]]=data[col[27]]
    #获取数值属性
    numericData={}
    numericData[col[3]]=data[col[3]]
    numericData[col[4]]=data[col[4]]
    numericData[col[5]]=data[col[5]]
    numericData[col[15]]=data[col[15]]
    numericData[col[18]]=data[col[18]]
    numericData[col[19]]=data[col[19]]
    numericData[col[21]]=data[col[21]]
    
    return nominalData,numericData

#计算标称属性的频数
def frequencyCompute(nominalData,colName):
    temp={}
    for item in nominalData[colName]:
        if str(item) not in temp.keys():
            temp[str(item)]=1
        else:
            temp[str(item)]+=1
    return temp
    
def nominalDataFrequency(nominalData):
    nominalData=cleaning(nominalData)
    nominalData_surgery=frequencyCompute(nominalData,"surgery")
    nominalData_Age=frequencyCompute(nominalData,"Age")
    nominalData_temperature_of_extremitiese=frequencyCompute(nominalData,"temperature_of_extremities")
    nominalData_peripheral_pulse=frequencyCompute(nominalData,"peripheral_pulse")
    nominalData_mucous_membranes=frequencyCompute(nominalData,"mucous_membranes")
    nominalData_nasogastric_reflux=frequencyCompute(nominalData,"nasogastric_reflux")
    nominalData_rectal_examination_feces=frequencyCompute(nominalData,"rectal_examination_feces")
    nominalData_abdomen=frequencyCompute(nominalData,"abdomen")
    nominalData_abdominocentesis_appearance=frequencyCompute(nominalData,"abdominocentesis_appearance")
    nominalData_outcome=frequencyCompute(nominalData,"outcome")
    nominalData_surgical_lesion=frequencyCompute(nominalData,"surgical_lesion")
    nominalData_cp_data=frequencyCompute(nominalData,"cp_data")
    #将频数的统计结果保存到本地
    nominalDataFrequency={}
    nominalDataFrequency["surgery"]=nominalData_surgery
    nominalDataFrequency["Age"]= nominalData_Age
    nominalDataFrequency["temperature_of_extremities"]=nominalData_temperature_of_extremitiese
    nominalDataFrequency["peripheral_pulse"]=nominalData_peripheral_pulse
    nominalDataFrequency["mucous_membranes"]=nominalData_mucous_membranes
    nominalDataFrequency["nasogastric_reflux"]=nominalData_nasogastric_reflux
    nominalDataFrequency["rectal_examination_feces"]=nominalData_rectal_examination_feces
    nominalDataFrequency["abdomen"]=nominalData_abdomen
    nominalDataFrequency["abdominocentesis_appearance"]=nominalData_abdominocentesis_appearance
    nominalDataFrequency["outcome"]=nominalData_outcome
    nominalDataFrequency["surgical_lesion"]=nominalData_surgical_lesion
    nominalDataFrequency["cp_data"]=nominalData_cp_data
    #写入json文件
    save_tofile(nominalDataFrequency,"data/numinalDataFrequency.json")  
    return nominalDataFrequency

#对缺失值进行清除
def cleaning(obj):
    for key in obj.keys():
        temp=[]
        for i in range(0,len(obj[key])):
            if not math.isnan(obj[key][i]):
                temp.append(float(obj[key][i]))
        obj[key]=temp
    return obj

#对数值属性求取五数概要及缺失值
def statistic(numericData):
    numericData_cleaned=cleaning(numericData)
    result={}
    for key in numericData_cleaned:
        result[key]={}
        result[key]["max"]=max(numericData_cleaned[key])
        result[key]["min"]=min(numericData_cleaned[key])
        result[key]["mean"]=sum(numericData_cleaned[key])/len(numericData_cleaned[key])
        result[key]["midian"]=midian(numericData_cleaned[key])
        result[key]["quartiles"]=quartiles(numericData_cleaned[key])
        result[key]["miss_num"]=300-len(numericData_cleaned[key])
    #将结果写入json中
    save_tofile(result,'data/numericDataStatistic.json')
    return result

def midian(arr):
    arr.sort()
    if(len(arr)%2==0):
        return (arr[int(len(arr)/2)]+arr[int(len(arr)/2)-1])/2.0
    else:
        return arr[int(len(arr)/2)]

def quartiles(arr):
    arr.sort()
    Q=[]
    Q1=arr[int((len(arr)+1)/4)-1]
    Q2=arr[int((len(arr)+1)/4)*2-1]
    Q3=arr[int((len(arr)+1)/4)*3-1]
    Q.append(Q1)
    Q.append(Q2)
    Q.append(Q3)
    return Q


#将数据存入文件中
def save_tofile(obj,path):
    jsObj=json.dumps(obj)
    fileObject = open(path, 'w')  
    fileObject.write(jsObj)  
    fileObject.close()
    
if __name__=="__main__":
    nominalData,numericData=init() #初始化
    nominalDataFrequency=nominalDataFrequency(nominalData) #获取标称属性的频数
    numericData_cleaned=cleaning(numericData) #清除数值属性中缺失的值
    save_tofile(numericData_cleaned,"data/numericData_cleaned.json") #保存清理后的数值属性
    result=statistic(numericData) #求出数值属性的五数概要及缺失值个数
