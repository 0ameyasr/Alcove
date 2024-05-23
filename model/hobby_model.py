import pandas,os
from random import randint
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score,calinski_harabasz_score,davies_bouldin_score
from stabilised_doping import stabilised_doping

columns = ["Patience","Creativity","Active","Observation","Curiosity","Persistence","Analytical","Social","Nature","Outdoorsy"]
stabilised_doping("Doped_Hobbies.csv","Doped_Hobbies.csv",0.05,5,25,column_names=columns,feedback=True)
# kmeans = KMeans(n_clusters=20,init='k-means++',random_state=0,n_init="auto")

dataset = pandas.read_csv(os.path.dirname(__file__)+"/Doped_Hobbies.csv")
X = dataset
# y_kmeans = kmeans.fit_predict(X)
# list_y = list(y_kmeans)

# for i in range(20):
#     print(f"{i+1} ==> {list_y.count(i)}")

scores = []
for n_clusters in range(2, 21):
    kmeans = KMeans(n_clusters=n_clusters,n_init='auto')
    kmeans.fit(X)
    labels = kmeans.labels_
    
    silhouette_avg = silhouette_score(X, labels)
    ch_score = calinski_harabasz_score(X, labels)
    db_score = davies_bouldin_score(X, labels)
    
    scores.append({
        'n_clusters': n_clusters,
        'silhouette': silhouette_avg,
        'calinski_harabasz': ch_score,
        'davies_bouldin': db_score
    })

for score in scores:
    print(f"n_clusters: {score['n_clusters']}")
    print(f"Silhouette Score, Calinski-Harabasz: {score['silhouette'],score['calinski_harabasz']}")
    print(f"Davies-Bouldin: {score['davies_bouldin']} ")
    print("-" * 20)

# import pandas as pd
# def get_cluster_averages(csv_file, labels):
#     df = pd.read_csv(csv_file)
#     df['cluster'] = labels
#     averages = df.groupby('cluster').mean().to_dict('list')
#     return {k: v for k, v in averages.items() if k != 'cluster'}

# cluster_averages = get_cluster_averages(os.path.dirname(__file__)+'/Doped_Hobbies_4.csv', y_kmeans)

# file = open("avg.txt","w")
# for cluster, averages in cluster_averages.items():
#     file.write(f"Cluster {cluster}: {', '.join(map(str, averages))}\n")