#import libraries
from __future__ import division
from datetime import datetime, timedelta,date
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold, cross_val_score, train_test_split
import xgboost as xgb

#function for ordering cluster numbers
def order_cluster(cluster_field_name, target_field_name,df, ascending):
        new_cluster_field_name = 'new_' + cluster_field_name
        df_new = df.groupby(cluster_field_name)[target_field_name].mean().reset_index()
        df_new = df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
        df_new['index'] = df_new.index
        df_final = pd.merge(df,df_new[[cluster_field_name,'index']], on=cluster_field_name)
        df_final = df_final.drop([cluster_field_name],axis=1)
        df_final = df_final.rename(columns={"index":cluster_field_name})
        return df_final

def get_all_clusters(data):
    # Feature selection
    features = ['CustomerID', 'InvoiceNo', 'InvoiceDate', 'Quantity', 'UnitPrice']
    data_clv = data[features]
    data_clv['TotalSales'] = data_clv['Quantity'].multiply(data_clv['UnitPrice'])

    # FEATURE ENGINEERING
    #converting the type of Invoice Date Field from string to datetime.
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    # # Printing the details of the dataset
    # maxdate = data['InvoiceDate'].dt.date.max()
    # mindate = data['InvoiceDate'].dt.date.min()
    # unique_cust = data['CustomerID'].nunique()
    # tot_quantity = data['Quantity'].sum()

    #we will be using only UK data
    data_uk = data.query("Country=='United Kingdom'").reset_index(drop=True)

    # RECENCY
    #create a generic user dataframe to keep CustomerID and new segmentation scores
    data_user = pd.DataFrame(data['CustomerID'].unique())
    data_user.columns = ['CustomerID']

    #get the max purchase date for each customer and create a dataframe with it
    data_max_purchase = data_uk.groupby('CustomerID').InvoiceDate.max().reset_index()
    data_max_purchase.columns = ['CustomerID','MaxPurchaseDate']
    # Compare the last transaction of the dataset with last transaction dates of the individual customer IDs.
    data_max_purchase['Recency'] = (data_max_purchase['MaxPurchaseDate'].max() - data_max_purchase['MaxPurchaseDate']).dt.days

    #merge this dataframe to our new user dataframe
    data_user = pd.merge(data_user, data_max_purchase[['CustomerID','Recency']], on='CustomerID')

    # ASSIGNING A RECENCY SCORE
    sse={} # error
    data_recency = data_user[['Recency']]
    for k in range(1, 10):
        kmeans = KMeans(n_clusters=k, max_iter=1000).fit(data_recency)
        data_recency["clusters"] = kmeans.labels_  #cluster names corresponding to recency values 
        sse[k] = kmeans.inertia_ #sse corresponding to clusters

    #build 4 clusters for recency and add it to dataframe
    kmeans = KMeans(n_clusters=4)
    data_user['RecencyCluster'] = kmeans.fit_predict(data_user[['Recency']])

    data_user = order_cluster('RecencyCluster', 'Recency',data_user,False)

    # FREQUENCY
    #get order counts for each user and create a dataframe with it
    data_frequency = data_uk.groupby('CustomerID').InvoiceDate.count().reset_index()
    data_frequency.columns = ['CustomerID','Frequency']

    #add this data to our main dataframe
    data_user = pd.merge(data_user, data_frequency, on='CustomerID')

    # FREQUENCY CLUSTERS
    sse={} # error
    data_recency = data_user[['Frequency']]
    for k in range(1, 10):
        kmeans = KMeans(n_clusters=k, max_iter=1000).fit(data_recency)
        data_recency["clusters"] = kmeans.labels_  #cluster names corresponding to recency values 
        sse[k] = kmeans.inertia_ #sse corresponding to clusters

    # Applying k-Means
    kmeans=KMeans(n_clusters=4)
    data_user['FrequencyCluster']=kmeans.fit_predict(data_user[['Frequency']])

    #order the frequency cluster
    data_user = order_cluster('FrequencyCluster', 'Frequency', data_user, True )

    # REVENUE
    #calculate revenue for each customer
    data_uk['Revenue'] = data_uk['UnitPrice'] * data_uk['Quantity']
    data_revenue = data_uk.groupby('CustomerID').Revenue.sum().reset_index()

    #merge it with our main dataframe
    data_user = pd.merge(data_user, data_revenue, on='CustomerID')

    # Elbow method to find out the optimum number of clusters for K-Means
    sse={} # error
    data_recency = data_user[['Revenue']]
    for k in range(1, 10):
        kmeans = KMeans(n_clusters=k, max_iter=1000).fit(data_recency)
        data_recency["clusters"] = kmeans.labels_  #cluster names corresponding to recency values 
        sse[k] = kmeans.inertia_ #sse corresponding to clusters

    # REVENUE CLUSTERS
    #apply clustering
    kmeans = KMeans(n_clusters=4)
    data_user['RevenueCluster'] = kmeans.fit_predict(data_user[['Revenue']])

    #order the cluster numbers
    data_user = order_cluster('RevenueCluster', 'Revenue',data_user,True)

    #calculate overall score and use mean() to see details
    data_user['OverallScore'] = data_user['RecencyCluster'] + data_user['FrequencyCluster'] + data_user['RevenueCluster']

    data_user['Segment'] = 'Low-Value'
    data_user.loc[data_user['OverallScore']>2,'Segment'] = 'Mid-Value' 
    data_user.loc[data_user['OverallScore']>4,'Segment'] = 'High-Value' 

    return data_user

def get_clv(data, data_user):
    # using only UK data:
    data_uk = data.query("Country=='United Kingdom'").reset_index(drop=True)
    data_3m = data_uk[(data_uk.InvoiceDate < pd.to_datetime(date(2011,6,1)).floor('D')) & (data_uk.InvoiceDate >= pd.to_datetime(date(2011,3,1)).floor('D'))].reset_index(drop=True) #3 months time
    data_6m = data_uk[(data_uk.InvoiceDate >= pd.to_datetime(date(2011,6,1)).floor('D')) & (data_uk.InvoiceDate < pd.to_datetime(date(2011,12,1)).floor('D'))].reset_index(drop=True) # 6 months time
    #calculate revenue and create a new dataframe for it
    data_6m['Revenue'] = data_6m['UnitPrice'] * data_6m['Quantity']
    data_user_6m = data_6m.groupby('CustomerID')['Revenue'].sum().reset_index()
    data_user_6m.columns = ['CustomerID','m6_Revenue']
    data_merge = pd.merge(data_user, data_user_6m, on='CustomerID', how='left') #Only people who are in the timeline of tx_user_6m
    data_merge = data_merge.fillna(0)
    data_graph = data_merge.query("m6_Revenue < 50000") #because max values are ending at 50,000

    #remove outliers
    data_merge = data_merge[data_merge['m6_Revenue']<data_merge['m6_Revenue'].quantile(0.99)]

    #creating 3 clusters
    kmeans = KMeans(n_clusters=3)
    data_merge['LTVCluster'] = kmeans.fit_predict(data_merge[['m6_Revenue']])
    #order cluster number based on LTV
    data_merge = order_cluster('LTVCluster', 'm6_Revenue',data_merge,True)

    #creatinga new cluster dataframe
    data_cluster = data_merge.copy()
    statistical_data = data_cluster.groupby('LTVCluster')['m6_Revenue'].describe()

    return data_graph, data_cluster, statistical_data

