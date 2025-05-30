#!/bin/bash
#PBS -N MnZnC
#PBS -q gigabyte
#PBS -l nodes=1:ppn=16
#PBS -V

cd $PBS_O_WORKDIR
cat $PBS_NODEFILE > pbs_nodes
echo Working directory is $PBS_O_WORKDIR

NPROCS=`wc -l < $PBS_NODEFILE`
NNODES=`uniq $PBS_NODEFILE | wc -l`

### Display the job context
echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`
echo Using ${NPROCS} processors across ${NNODES} nodes


MPIRUN=/apps/intel_2019/compilers_and_libraries_2019.5.281/linux/mpi/intel64/bin/mpirun

${MPIRUN} -n ${NPROCS} /home/amrita/Codes/vasp.5.4.4.pl2.wan.patch/bin/vasp_std > vasp.out
