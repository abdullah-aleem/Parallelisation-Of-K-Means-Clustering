
'''
This script will divide the data create required processes,scatter the data, process the emethod  and then rewrite the data back


'''
import h5py
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
#get clusters
with h5py.File('cluster.hdf5','r') as f:
    cluster=  f['cluster'][:]







packets=[]
#get data 
with h5py.File('data.hdf5','r') as f:
    data=  f['data'][:]
packet_size = -(-len(data) // size)
if rank>=len(data):
    packets=None
else: 
    packets = data[rank*packet_size:(rank+1)*packet_size]
print(packets," from ",rank)


#we need to calculate cluster array and then save that array to new hdf5 file
#perform emethod
clustersArray=[[] for x in range(len(cluster))]
if type(packets) is not type(None):
    for i in range(len(packets)):
        distance=0
        index=0 
        for j in range(len(cluster)):
            #compute ecludian distance
            temp = np.sqrt(np.sum((packets[i] - cluster[j]) ** 2))
            if j == 0:
                distance=temp
                index=j
            elif distance>temp:
                distance=temp
                index=j
        clustersArray[index].append(packets[i])
    print(clustersArray)
processed_data = comm.gather(clustersArray, root=0)

print("processed data is:",processed_data)
if rank == 0:
    #this process has more memory complexity 
    array=[[] for x in range(len(cluster))]
    for x in range(len(processed_data)):
        for y in range(len(processed_data[x])):
            if len(processed_data[x][y])>0:
                array[y].append(processed_data[x][y])
    print("final array is:",array)
    
    
    #m-method
    previousClusterCenters=cluster.copy()
            
    for w in range(len(array)):
        if len(array[w])!=0:
            cluster[w]=np.mean(array[w],axis=0)   
    
    
    if np.all(previousClusterCenters==cluster):
        pass   
    print("the new cluster centers are", cluster)
    with h5py.File("cluster.hdf5", "w") as f:
            f.create_dataset("cluster", data=cluster)