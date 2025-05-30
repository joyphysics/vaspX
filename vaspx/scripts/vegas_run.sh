#!/bin/bash
#PBS -N MonteCarlo
#PBS -q long
#PBS -l nodes=1:ppn=1
#PBS -V

cd $PBS_O_WORKDIR

~/vegas config.json > vegas.out
                                                               
