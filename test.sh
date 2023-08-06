shellfile=hello.sh

./sheepy.py "$shellfile" > out.py
exitC=$?

if [ "$exitC" -ne 0 ]
then
	echo Problems When Running Code
	exit 1
fi

if [ -d tmp ]
then
	rm -r tmp
fi

mkdir tmp

pyflakes out.py > tmp/flakes.err
pyf=$?

pycodestyle out.py > tmp/codestyle.err
pyc=$?

if [ "$pyf" -ne 0 ] || [ "$pyc" -ne 0 ]; then
	echo Errors in Style!
fi


./"$shellfile" $@ > tmp/out.exp
./out.py $@ > tmp/out.test

if diff tmp/out.exp tmp/out.test > /dev/null
then
	echo ":)"
else
	echo ">:("
fi

