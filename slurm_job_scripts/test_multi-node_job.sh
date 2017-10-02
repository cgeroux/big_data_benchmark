#!/bin/bash
#SBATCH --account=def-cgeroux
#SBATCH --time=03:00:00
#SBATCH --nodes=2
#SBATCH --mem=32000M
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
export -n HOSTNAME;

echo "SLURM_MEM_PER_NODE="${SLURM_MEM_PER_NODE}
echo "SLURM_CPUS_PER_TASK="${SLURM_CPUS_PER_TASK}
echo "SLURM_NTASKS="${SLURM_NTASKS}
echo "SLURM_JOB_NODELIST="$SLURM_JOB_NODELIST 
echo "MAX_TASKS_PER_NODE ="$MAX_TASKS_PER_NODE  

srun -O -x $(hostname) -n $((SLURM_NTASKS -1)) --label --output=$SPARK_LOG_DIR/spark-$SPARK_IDENT_STRING-workers.out \
     start-slave.sh -m ${SLURM_MEM_PER_NODE}M -c ${SLURM_CPUS_PER_TASK} spark://$(hostname -f):7077
)
# &

echo $(date): before spark-submit 
#spark-submit --executor-memory ${SLURM_MEM_PER_NODE}M $SPARK_HOME/examples/src/main/python/pi.py 100000
SPARK_BM_ROOT_PATH=/home/cgeroux/test_spark/big_data_benchmark
SPARK_BM_TMP_PATH=/scratch/cgeroux/spark_input_1part_1stripe
spark-submit --executor-memory ${SLURM_MEM_PER_NODE}M $SPARK_BM_ROOT_PATH/spark/linecount/linecount.py --num-partitions=1 $SPARK_BM_TMP_PATH/1G $SPARK_BM_TMP_PATH/1G_tmp_$SLURM_JOB_ID
echo $(date): after spark-submit 

echo $(date): before stopping slaves
srun -O stop-slave.sh
echo $(date): after stopping slaves

echo $(date): before stopping master
stop-master.sh
echo $(date): after stopping master