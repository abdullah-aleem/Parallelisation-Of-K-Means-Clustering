
'''
This script will divide the data create required processes,scatter the data, process the emethod  and then rewrite the data back


'''
import h5py
import numpy as np
from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor
import sys
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
SHUTDOWN_TAG = 999  # Custom tag for shutdown messages
packets=[]
#get data 
with h5py.File('data.hdf5','r') as f:
    data=  f['data'][:]

# Calculate packet size
packet_size = (len(data) // size)
print(len(data) // size)

# Initialize packets to None
packets = None

# Distribute data among ranks
if rank < size:
    # Check if it's the last rank
    if rank == size - 1:
        # Assign remaining data to the last rank
        packets = data[rank * packet_size:]
    else:
        # Regular packet assignment
        packets = data[rank * packet_size:(rank + 1) * packet_size]

print(packets, " from ", rank)

#we need to calculate cluster array and then save that array to new hdf5 file
#perform emethod
while True:
    with h5py.File('cluster.hdf5','r') as f:
        cluster=  f['cluster'][:]
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

    
    comm.barrier() 
    print("processed data is:",processed_data)
    if rank == 0:
        #this process has more memory complexity 
        array=[[] for x in range(len(cluster))]
        
        for x in range(len(processed_data)):
            for y in range(len(processed_data[x])):
                if len(processed_data[x][y])>0:
                    if(len(array[y])!=0):
                        array[y]+=processed_data[x][y]
                    else:
                        array[y]+=(processed_data[x][y])
        print("final array is:",array)
        
        
        #m-method
        previousClusterCenters=cluster.copy()
        newCluster=[[] for x in range(len(cluster))]
        for w in range(len(array)):
            if len(array[w])!=0:
                newCluster[w]=np.mean(array[w],axis=0)   
        print(newCluster)
        print("the new cluster centers are", cluster)
        if np.all(previousClusterCenters==newCluster):
            break   
        with h5py.File("cluster.hdf5", "w") as f:
                f.create_dataset("cluster", data=newCluster)
    comm.barrier()
print('done')
comm.Abort()

     