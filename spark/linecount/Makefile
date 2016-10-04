run: 
	-hdfs dfs -rm -R /user/ubuntu/wordcounts
	spark-submit --master yarn --deploy-mode cluster --executor-cores=8 wordcount.py "10GB.txt"