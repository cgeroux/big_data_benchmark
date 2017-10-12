#!/bin/bash
#SBATCH --account=def-cgeroux

##SBATCH --account=cc-debug_gpu
##SBATCH --reservation=cc-debug_gpu_6
##SBATCH --gres=gpu:0

#SBATCH --account=def-cgeroux
#SBATCH --time=<job-time>
#SBATCH --nodes=4
#SBATCH --cpus-per-task=32
#SBATCH --ntasks-per-node=1
#SBATCH --mem=128000MB
#SBATCH --job-name=spark_IO_multi-node_<spark-partitions.name>_<lustre-stripes.name>_<data-size.name>
#SBATCH --output=%x-%j.out

module load spark

export SPARK_IDENT_STRING=$SLURM_JOBID
export SPARK_WORKER_DIR=$SLURM_TMPDIR
start-master.sh

(
export SPARK_NO_DAEMONIZE=1;

srun -x $(hostname -s) -n $((SLURM_NTASKS -1)) --label --output=$SPARK_LOG_DIR/spark-$SPARK_IDENT_STRING-workers.out \
     start-slave.sh -m ${SLURM_MEM_PER_NODE}M -c ${SLURM_CPUS_PER_TASK} spark://$(hostname -f):7077
) &

source ./paths.sh
TMP_PATH=$SPARK_BM_TMP_PATH/spark_input_<spark-partitions.name>_<lustre-stripes.name>
spark-submit --deploy-mode cluster --executor-memory ${SLURM_MEM_PER_NODE}M $SPARK_BM_ROOT_PATH/spark/linecount/linecount.py --num-partitions=<spark-partitions.text> $TMP_PATH/<data-size.name> $TMP_PATH/<data-size.name>_tmp_$SLURM_JOB_ID

stop-master.sh
