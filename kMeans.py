import numpy as np
import h5py
import subprocess
import multiprocessing
import os
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
            print('finally completed training')
            try:
                if os.path.exists('cluster.hdf5'):
                    os.remove('cluster.hdf5')
                if os.path.exists('data.hdf5'):
                    os.remove('data.hdf5')
            except Exception as e:
                print(f"An error occurred while trying to delete the file: {e}")
            return 
            
            

    def predict(self):
        ##not implemented yet
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
        
        process = subprocess.Popen(f"mpiexec python subProcess.py",shell=True)
        process.wait()
        print("waitng for the process to finish")
        
        
        
        return clustersArray
    
    
        
    
        
    
    



