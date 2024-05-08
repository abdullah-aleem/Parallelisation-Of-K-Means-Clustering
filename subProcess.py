
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






#master
packets=[]
if rank==0:
    with h5py.File('data.hdf5','r') as f:
        data=  f['data'][:]
    packet_size = -(-len(data) // size) 
    packets = [data[i:i+packet_size] for i in range(0, len(data), packet_size)]
    if len(packets) < size:
        packets.extend([None] * (size - len(packets)))
    
    print("packets are ",packets)
    
    
    
packets=comm.scatter(packets,root=0)
print(packets," from ",rank)

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
if rank == 0:
    print("processed data is ",processed_data)

    processed_data=np.transpose(processed_data,axes=(1,0,2))
    processed_data =[np.concatenate(subarr, axis=0) for subarr in processed_data]
    print("processed data is ",processed_data)