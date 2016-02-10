TARGET=ParseMetaData

INPUTDIR=../testArchive.txt
OUTPUTDIR=./output.txt
MAINCLASS=${TARGET}

bin/${TARGET}.jar:bin/${TARGET}.class
	jar cf bin/${TARGET}.jar bin/${TARGET}*.class

bin/${TARGET}.class:src/${TARGET}.java
	-mkdir bin
	javac -d bin -sourcepath src src/${TARGET}.java

run: bin/${TARGET}.jar cleanoutput
	java -cp bin ${TARGET} ${INPUTDIR} ${OUTPUTDIR}

runbg: ${TARGET}.jar cleanoutput
	hadoop jar ${TARGET}.jar ${MAINCLASS} ${SEARCHSTRING} ${INPUTDIR} ${OUTPUTDIR} &>std_out.txt&

cleanoutput:
	-rm -rf ${OUTPUTDIR}

clean:
	-rm -rf ./bin

help:
	@echo Targets:
	@echo   <no target>: builds the jar file
	@echo   run: runs the hadoop job in the forground
	@echo   runbg: runs the hadoop job in the background and redirects stdout and 
	@echo     std error to std_out.txt file
	@echo   clean: cleans up build files for a fresh rebuild
