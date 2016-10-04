TARGET=LineCount

INPUTDIR=../../input_files/10G_32.txt
#INPUTDIR=./test.txt
MAINCLASS=${TARGET}

bin/${TARGET}.jar:bin/${TARGET}.class
	jar cf bin/${TARGET}.jar bin/${TARGET}*.class

bin/${TARGET}.class:src/${TARGET}.java
	-mkdir bin
	javac -d bin -sourcepath src src/${TARGET}.java

run: bin/${TARGET}.jar
	echo `date`
	java -cp bin ${TARGET} ${INPUTDIR} ${OUTPUTDIR}
	echo `date`

clean:
	-rm -rf ./bin

help:
	@echo Targets:
	@echo   <no target>: builds the jar file
	@echo   run: runs the hadoop job in the forground
	@echo   clean: cleans up build files for a fresh rebuild
