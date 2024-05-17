from setuptools import setup, find_packages

setup(
    name='KMeansParallel',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'h5py',
        'mpi4py',
    ],
    author='Abdullah Aleem',
    author_email='abdullahaleem2102@gmail.com',
    description='kMeans clustering algorithm with parallelization using MPI and h5py',
    url='https://github.com/abdullah-aleem/Parallelisation-Of-K-Means-Clustering',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)