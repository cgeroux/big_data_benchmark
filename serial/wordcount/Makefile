TARGET=WordCount

INPUTDIR=../../input_files/10G.txt
#INPUTDIR=./test.txt
OUTPUTDIR=./output.txt
MAINCLASS=${TARGET}

bin/${TARGET}.jar:bin/${TARGET}.class
	jar cf bin/${TARGET}.jar bin/${TARGET}*.class

bin/${TARGET}.class:src/${TARGET}.java
	-mkdir bin
	javac -d bin -sourcepath src src/${TARGET}.java

run: bin/${TARGET}.jar cleanoutput
	echo `date`
	java -cp bin ${TARGET} ${INPUTDIR} ${OUTPUTDIR}
	echo `date`

cleanoutput:
	-rm -rf ${OUTPUTDIR}

clean:
	-rm -rf ./bin

help:
	@echo Targets:
	@echo   <no target>: builds the jar file
	@echo   run: runs the hadoop job in the forground
	@echo   clean: cleans up build files for a fresh rebuild
	@echo   cleanoutput: cleans up output files
