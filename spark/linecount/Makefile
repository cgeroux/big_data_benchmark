run: 
	-hdfs dfs -rm -R /user/ubuntu/wordcounts
	spark-submit --master yarn --deploy-mode cluster --executor-cores=1 --num-executors=8 --executor-memory=3G --driver-memory=3G linecount.py "100GB.txt"
