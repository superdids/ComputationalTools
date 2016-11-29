#!/bin/sh

PBS -N MinMaxLatLng

PBS -q hpc

PBS -l walltime=00:05:00

PBS -l nodes=5:ppn=20

PBS -l pmem=512mb

PBS -l vmem=6bg

PBS -M didrik.aubert@gmail.com

PBS -m abe

if test X$PBS_ENVIRONMENT = XPBS_BATCH; then cd $PBS_O_WORKDIR; fi

module load numpy/1.9.2-python-2.7.3-openblas-0.2.14 
module load scipy/scipy-0.15.1-python-2.7.3 
module load pandas/0.16.2-python.2.7.3

# run with qsub jobMinMaxLatLng.sh

cat CrimesChicago.json | ./mapperMinMaxLatLng.py | sort | ./reducerMinMaxLatLng.py > resultMinMaxLatLng
