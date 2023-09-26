class univariate():
        def quanqual(df):
            quan=[]
            qual=[]
            for colname in df.columns:
                if(df[colname].dtype=='O'):
                    qual.append(colname)
                else:
                    quan.append(colname)
            return(quan,qual)
