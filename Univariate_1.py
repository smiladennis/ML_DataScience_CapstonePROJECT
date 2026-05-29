import pandas as pd
import numpy as np

class UnivariateClass():
    
    @staticmethod
    def QualQuan(dataset):
        Quan, Qual = [], []
        for columnName in dataset.columns:
            dataset[columnName] = pd.to_numeric(dataset[columnName], errors='ignore')
        for columnName in dataset.columns:
            if dataset[columnName].dtypes == 'O':
                Qual.append(columnName)
            else:
                Quan.append(columnName)
        return (Qual, Quan)
        
    @staticmethod   
    def Univariate_Table(dataset, quan):
        dataset = dataset.copy()
        for col in quan:
            dataset[col] = pd.to_numeric(dataset[col], errors='coerce')  

        descriptive = pd.DataFrame(
            index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%",
                   "99%","Q4:100%","IQR","1.5rule","Lesser","Greater","Min","Max","kurtosis","skew","Variance","S.D"],
            columns=quan
        )

        desc = dataset[quan].describe()

        for columnName in quan:
            q1   = desc[columnName]["25%"]
            q3   = desc[columnName]["75%"]
            iqr  = q3 - q1
            rule = 1.5 * iqr

            descriptive.loc["Mean",     columnName] = dataset[columnName].mean()
            descriptive.loc["Median",   columnName] = dataset[columnName].median()
            descriptive.loc["Mode",     columnName] = dataset[columnName].mode()[0]
            descriptive.loc["Q1:25%",   columnName] = q1
            descriptive.loc["Q2:50%",   columnName] = desc[columnName]["50%"]
            descriptive.loc["Q3:75%",   columnName] = q3
            descriptive.loc["99%",      columnName] = np.percentile(dataset[columnName].dropna(), 99)
            descriptive.loc["Q4:100%",  columnName] = desc[columnName]["max"]
            descriptive.loc["IQR",      columnName] = iqr
            descriptive.loc["1.5rule",  columnName] = rule
            descriptive.loc["Lesser",   columnName] = q1 - rule
            descriptive.loc["Greater",  columnName] = q3 + rule
            descriptive.loc["Min",      columnName] = dataset[columnName].min()
            descriptive.loc["Max",      columnName] = dataset[columnName].max()
            descriptive.loc["kurtosis", columnName] = dataset[columnName].kurtosis()
            descriptive.loc["skew",     columnName] = dataset[columnName].skew()
            descriptive.loc["Variance", columnName] = dataset[columnName].var()
            descriptive.loc["S.D",      columnName] = dataset[columnName].std()

        return descriptive

    @staticmethod
    def check_OutlierColumns(descriptive,quan):
        lesser=[]
        greater=[]
        for columnName in quan:
            if(descriptive[columnName]["Min"]<descriptive[columnName]["Lesser"]):
                lesser.append(columnName)
            if(descriptive[columnName]["Max"]>descriptive[columnName]["Greater"]):
                greater.append(columnName)
                    
        return lesser,greater
        
    @staticmethod
    def replace_Outlier(dataset,descriptive,lesser,greater):
        for columnName in lesser:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["Lesser"]]=descriptive[columnName]["Lesser"]
        for columnName in greater:
            dataset[columnName][dataset[columnName]>descriptive[columnName]["Greater"]]=descriptive[columnName]["Greater"]

    @staticmethod
    def freqTable(columnName,dataset):
        FreqTable=pd.DataFrame(columns=["Unique_Values","Frequency","Relative_Frequency","Cumulative_Relative_Frequency"])
        FreqTable["Unique_Values"]=dataset[columnName].value_counts().index
        FreqTable["Frequency"]=dataset[columnName].value_counts().values
        FreqTable["Relative_Frequency"]=FreqTable["Frequency"]/103
        FreqTable["Cumulative_Relative_Frequency"]=FreqTable["Relative_Frequency"].cumsum()
        
        return FreqTable
