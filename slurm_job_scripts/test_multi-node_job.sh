#!/bin/bash
#SBATCH --account=def-cgeroux

##SBATCH --account=cc-debug_gpu
##SBATCH --reservation=cc-debug_gpu_6
##SBATCH --gres=gpu:0

#SBATCH --account=def-cgeroux
#SBATCH --time=00:10:00
#SBATCH --nodes=3
#SBATCH --mem=2000M
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=test_multi-node_job
#SBATCH --output=%x-%j.out

module load spark
#module load python/2.7.13

export SPARK_IDENT_STRING=$SLURM_JOBID
export SPARK_WORKER_DIR=$SLURM_TMPDIR
start-master.sh

(
export SPARK_NO_DAEMONIZE=1;

srun -x $(hostname -s) -n $((SLURM_NTASKS -1)) --label --output=$SPARK_LOG_DIR/spark-$SPARK_IDENT_STRING-workers.out \
     start-slave.sh -m ${SLURM_MEM_PER_NODE}M -c ${SLURM_CPUS_PER_TASK} spark://$(hostname -f):7077
) &

SPARK_BM_ROOT_PATH=/home/cgeroux/big_data_benchmark
SPARK_BM_TMP_PATH=/scratch/cgeroux/spark_input_1part_1stripe
spark-submit --executor-memory ${SLURM_MEM_PER_NODE}M $SPARK_BM_ROOT_PATH/spark/linecount/linecount.py --num-partitions=1 $SPARK_BM_TMP_PATH/1G $SPARK_BM_TMP_PATH/1G_tmp_$SLURM_JOB_ID

stop-master.sh
