import numpy as np
import h5py
import subprocess
import multiprocessing
class KMeans:
    def __init__(self, n_clusters=3, max_iter=1000, cluster_centers=None):
        self.clusters=n_clusters
        self.max_iter=max_iter
        self.cluster_centers=np.array(cluster_centers)
        self.data=None
    def fit(self,data):
        for i in range(self.max_iter):    
            self.data=np.array(data)
            
            clusterArray=self.paralleleMethod()
            #m method implemented below, create new cluster centers
            previousClusterCenters=self.cluster_centers.copy()
            
            for w in range(len(clusterArray)):
                if len(clusterArray[w])!=0:
                    self.cluster_centers[w]=np.mean(clusterArray[w],axis=0)   
            
            
            if np.all(previousClusterCenters==self.cluster_centers):
                break
            print("the new cluster centers are", self.cluster_centers)
            
            
            
    def accuracy(self):
        print("KMeans accuracy method called")
        

    def predict(self):
        print("KMeans predict method called")
        
        
    def paralleleMethod(self):
        #assign points to clusters
        clustersArray=[[] for x in range(len(self.cluster_centers))]
        #serialize the data using HDF5 library
        with h5py.File("data.hdf5", "w") as f:
            f.create_dataset("data", data=self.data)
        with h5py.File("cluster.hdf5", "w") as f:
            f.create_dataset("cluster", data=self.cluster_centers)
                    
        #run a script that would parallelize the computation
        num_core = multiprocessing.cpu_count()
        
        process = subprocess.Popen(f"mpiexec --oversubscribe -n {num_core} python subProcess.py",shell=True)
        print("waitng for the process to finish")
        
        process.wait()
        
        return clustersArray
    
    
        
    def eMethod(self,data,clusters):
        #assign points to clusters
        clustersArray=[[] for x in range(len(clusters))]
        for i in range(len(data)):
            distance=0
            index=0 
            for j in range(len(clusters)):
                #compute ecludian distance
                temp = np.sqrt(np.sum((data[i] - clusters[j]) ** 2))
                if j == 0:
                    distance=temp
                    index=j
                elif distance>temp:
                    distance=temp
                    index=j
            clustersArray[index].append(data[i])
        print(clustersArray)
        return clustersArray
        
    
    



