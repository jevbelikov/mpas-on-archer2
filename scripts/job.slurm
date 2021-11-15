#!/bin/bash

#SBATCH --job-name=mpas_test
#SBATCH --nodes=RUN_NODE_COUNT
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:0
#SBATCH --account=pr1ujaes
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --output=log.slurm.out
#SBATCH --error=log.slurm.err

export PIO=/work/pr1ushpc/pr1ushpc/pr1ujaes/MPAS/pio-2.5.2
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PIO/lib

module -s load epcc-job-env
module restore /etc/cray-pe.d/PrgEnv-gnu
module load cray-parallel-netcdf
module load cray-netcdf-hdf5parallel
module load cray-hdf5-parallel

#start_time=$(date +%s%3N)
srun --distribution=block:block --hint=nomultithread ./atmosphere_model > MPAS_output
#elapsed_time=$(expr $(date +%s%3N) - $start_time)
