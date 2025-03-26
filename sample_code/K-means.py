import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

df = pd.read_csv('./Data/Spotify_YouTube.csv')
X = df[['Liveness', 'Energy', 'Loudness']].copy()

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

inertias = []
K_range = range(1, 15)
for k in K_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=0)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.figure()
plt.plot(K_range, inertias, marker='o')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.savefig('./imgs/Elbow_Method.png')
plt.close()

OPTIMAL_K = 5
kmeans_opt = KMeans(n_clusters=OPTIMAL_K, init='k-means++', random_state=0)
labels_kmeans = kmeans_opt.fit_predict(X_scaled)

centers_scaled = kmeans_opt.cluster_centers_
centers_original = scaler.inverse_transform(centers_scaled)

center_df = pd.DataFrame(
    centers_original, 
    columns=['Liveness', 'Energy', 'Loudness']
)
center_df.index.name = 'Cluster'
print("K-Means centers (original scale):")
print(center_df)

df['Cluster'] = labels_kmeans

cluster_labels = {
    0: "Quiet, Moderate Energy (Studio Feel)",
    1: "High Energy, Loud (Medium-Live Feel)",
    2: "High Energy, Loud (Studio-Focused)",
    3: "Very Quiet, Very Low Energy (Ambient/Minimal)",
    4: "High-Liveness, Moderate-High Energy (Live Performances)"
}

df['Cluster_Label'] = df['Cluster'].map(cluster_labels)

fig = plt.figure(figsize=(19, 8))
ax = fig.add_subplot(projection='3d')

scatter = ax.scatter(
    X_scaled[:, 0], X_scaled[:, 1], X_scaled[:, 2],
    c=labels_kmeans,
    alpha=0.7
)
ax.set_title(f'K-Means Clusters (K={OPTIMAL_K})')
ax.set_xlabel('Liveness (scaled)')
ax.set_ylabel('Energy (scaled)')
ax.set_zlabel('Loudness (scaled)')

handles_kmeans, uniques_kmeans = scatter.legend_elements(prop="colors")

legend_labels_kmeans = [
    "Quiet, Moderate Energy (Studio Feel)", 
    "High Energy, Loud (Medium-Live Feel)",
    "High Energy, Loud (Studio-Focused)",
    "Very Quiet, Very Low Energy (Ambient/Minimal)",
    "High-Liveness, Moderate-High Energy (Live Performances)"
]

ax.legend(
    handles_kmeans,
    legend_labels_kmeans,
    title="Clusters",
    bbox_to_anchor=(1.2, 1),
    loc='upper left'
)

plt.savefig('./imgs/3D_Clusters.png')
plt.close()

Z = linkage(X_scaled, method='ward')
plt.figure(figsize=(16, 8))
dendrogram(Z)
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Samples')
plt.ylabel('Distance')
plt.savefig('./imgs/dendrogram.png')
plt.close()

hc_clusters = 5
hc = AgglomerativeClustering(n_clusters=hc_clusters, metric='euclidean', linkage='ward')
labels_hc = hc.fit_predict(X_scaled)

hc_labels_dict = {
    0: "HC: Quiet, Moderate (Similar to K0?)",
    1: "HC: High Energy, Loud (Similar to K1?)",
    2: "HC: High Energy, Loud (Studio?)",
    3: "HC: Very Quiet & Low Energy",
    4: "HC: High-Liveness, Mod-High Energy"
}

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(projection='3d')

scatter_hc = ax.scatter(
    X_scaled[:, 0], X_scaled[:, 1], X_scaled[:, 2],
    c=labels_hc,
    alpha=0.7
)
ax.set_title(f'Hierarchical Clustering (n={hc_clusters})')
ax.set_xlabel('Liveness (scaled)')
ax.set_ylabel('Energy (scaled)')
ax.set_zlabel('Loudness (scaled)')

handles_hc, uniques_hc = scatter_hc.legend_elements(prop="colors")
legend_labels_hc = [
    "HC: Quiet, Moderate (Similar to K0?)",
    "HC: High Energy, Loud (Similar to K1?)",
    "HC: High Energy, Loud (Studio?)",
    "HC: Very Quiet & Low Energy",
    "HC: High-Liveness, Mod-High Energy"
]

ax.legend(
    handles_hc,
    legend_labels_hc,
    title="Clusters",
    bbox_to_anchor=(1.2, 1),
    loc='upper left'
)

plt.savefig('./imgs/Hierarchical_Cluster.png')
plt.close()
