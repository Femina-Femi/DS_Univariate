
class univariate():
    #import pandas as pd
    #import numpy as np
    def quanqual(df):
        quan=[]
        qual=[]
        for colname in df.columns:
            if(df[colname].dtype=='O'):
                qual.append(colname)
            else:
                quan.append(colname)
        return(quan,qual)
    def mydescribe(df,quan):
        import pandas as pd
        import numpy as np        
        descriptive=pd.DataFrame(index=('Mean','Median','Mode','Q1:25%','Q2:50%',                                                                                             'Q3:75%','99%','Q4:100%','IQR','1.5rule','lower_bound','upper_bound','min','max','skew','kurtosis'),columns=quan)
        for colname in quan:
            descriptive[colname]['Mean']=df[colname].mean()
            descriptive[colname]['Median']=df[colname].median()
            descriptive[colname]['Mode']=df[colname].mode()[0]
            descriptive[colname]['Q1:25%']=df.describe()[colname]['25%']
            descriptive[colname]['Q2:50%']=df.describe()[colname]['50%']
            descriptive[colname]['Q3:75%']=df.describe()[colname]['75%']
            descriptive[colname]['99%']=np.percentile(df[colname],99)
            descriptive[colname]['Q4:100%']=df.describe()[colname]['max']
            descriptive[colname]['IQR'] = descriptive[colname]['Q3:75%']-descriptive[colname]['Q1:25%']
            descriptive[colname]['1.5rule'] =1.5 * descriptive[colname]['IQR']
            descriptive[colname]['lower_bound']= descriptive[colname]['Q1:25%']-descriptive[colname]['1.5rule']
            descriptive[colname]['upper_bound']=descriptive[colname]['Q3:75%']+descriptive[colname]['1.5rule']
            descriptive[colname]['min']= df[colname].min()
            descriptive[colname]['max']=df[colname].max()
            descriptive[colname]['skew']=df[colname].skew()
            descriptive[colname]['kurtosis']=df[colname].kurtosis()          
            
        return(descriptive)
    def find_outliercol(quan,descriptive):
        lesser=[]
        greater=[]
        for i in quan:
            if(descriptive[i]['min']<descriptive[i]['lower_bound']):
                lesser.append(i)
            if(descriptive[i]['max']>descriptive[i]['upper_bound']):
                greater.append(i)
        return (lesser,greater)   
    def freq_table(colname,df):
        import pandas as pd
        frequency_table = pd.DataFrame(columns=['unique','frequency','Relative_Freq','Cum_Rel_Freq'])
        frequency_table['unique']= df[colname].value_counts().index
        frequency_table['frequency']= df[colname].value_counts().values
        frequency_table['Relative_Freq']= frequency_table['frequency']/103
        frequency_table['Cum_Rel_Freq']= frequency_table['Relative_Freq'].cumsum()
        return(frequency_table)
    def freq_all_col(df,quan,central_details):
        freq_dict = {}
        for col in quan:
            freq_col =univariate.freq_table(col,df)
            temp={col:freq_col}
            freq_dict.update(temp)
        return(freq_dict)
    def replace_outlier(df,lesser,greater,central_details):
        ''' give data set, lesser outlier column details , central_details like min max and upper and lower bound 
            this function will replace lesser outler with lowerbound value and greater outlier with upper bound value and return updated 
            data set'''
        for i in lesser:
            df[i][df[i]<central_details[i]['lower_bound']]=central_details[i]['lower_bound']
        for i in greater:
            df[i][df[i]>central_details[i]['upper_bound']] = central_details[i]['upper_bound']
        return(df)
    def all_in_one(df):
        ''' give data set as input and this function will return below items 
        1.quan list which is list of all quantitative columns
        2.qual list which will give list of all qualitative columns
        3.central tendency details like min , max , mode , median , std diviation ,IQR 
        4.minimum outlier column list
        5.Maximum outlier column list
        6.all quantitative columns frequency details in dictionary , access with columns name '''
        
        quan,qual = univariate.quanqual(df)
        central_details=univariate.mydescribe(df,quan)
        lesser_outlier,Greater_outlier = univariate.find_outliercol(quan,central_details)
        all_frequency = univariate.freq_all_col(df,quan,central_details)
        return(quan,qual,central_details,lesser_outlier,Greater_outlier,all_frequency)

        
        
   