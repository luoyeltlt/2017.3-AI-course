max=100
rm -rf res.log
cp main.py main_freeze.py
for i in `seq 2 $max`
do 
	python ./main_freeze.py
	echo $? >> res.log
done
rm main_freeze.py
