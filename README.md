# KMeans Parallel Clustering Library

This library provides an implementation of the KMeans clustering algorithm with parallel processing using MPI for Python (`mpi4py`). It leverages multiprocessing and HDF5 for data serialization to enhance the efficiency and scalability of clustering large datasets.

## Features

- **Parallel KMeans Clustering**: Distributes the clustering computation across multiple processors to accelerate the processing time.
- **HDF5 Serialization**: Uses HDF5 to handle large datasets efficiently by reading and writing data in a binary format.
- **Easy Integration**: Designed to be easily integrated into existing Python projects requiring KMeans clustering.

## Usage

### Initializing the KMeans Class

Create an instance of the `KMeans` class, specifying the number of clusters, maximum iterations, and optionally initial cluster centers.

```python
from kmeans import KMeans
import numpy as np

# Example data
data = np.random.rand(100, 2)

# Initialize KMeans with 3 clusters
kmeans = KMeans(n_clusters=3,cluster_centers=[[1,2],[2,3],[3,4]])

# Fit the model to the data
kmeans.fit(data)

KMeans Class
```
## The KMeans class handles the core functionality, including initialization, fitting the model to the data, and defining the method for parallel computation.

- **__init__(self, n_clusters=3, max_iter=1000, cluster_centers=None)**: Initializes the KMeans object with the specified number of clusters, maximum iterations, and optional initial cluster centers.
- **fit(self, data)**: Fits the KMeans model to the provided data, iterating up to the maximum number of iterations to adjust cluster centers and assign data points to clusters.
- **predict(self)**: Placeholder method for future implementation to predict cluster membership for new data points.
- **paralleleMethod(self)**: Handles the parallel computation of cluster assignments and updates cluster centers using MPI.

## Parallel Computation with subProcess.py

The parallel computation is handled by a separate script, subProcess.py, executed by the MPI environment:

- **MPI Initialization**: Sets up the MPI environment, determines the rank and size of the processors.
- **Data Distribution**: Distributes data among available processors, ensuring an even workload.
- **Cluster Assignment**: Each processor calculates the distance of its data points to the cluster centers and assigns them to the nearest cluster.
- **Data Gathering**: Gathers the processed data from all processors and updates the cluster centers on the root processor.
- **Cluster Center Update**: Recalculates the cluster centers based on the new assignments and updates the HDF5 file with the new centers.
- **Convergence Check**: Checks if the cluster centers have stabilized; if so, terminates the computation.

### Running the Code

1. **Set up the environment**: Ensure you have the necessary dependencies installed.
2. **Create an instance of KMeans**: Initialize with the desired number of clusters and fit the model to your data.
3. **Run the parallel processing script**: Ensure subProcess.py is in the same directory and is executed correctly by MPI.

Replace <number_of_processes> with the number of processors you want to use for parallel computation.
## Note

- This implementation is a basic example of parallelizing KMeans clustering. Further optimizations and improvements can be made for more robust and efficient performance.
- The predict method is not implemented yet and will need to be developed to use the trained model for making predictions on new data.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgements

- This implementation uses numpy for numerical operations.
- HDF5 file handling is done using the h5py library.
- Parallel processing is facilitated by the mpi4py library.

Contact

For any questions or contributions, feel free to open an issue or submit a pull request on the project's GitHub repository.
