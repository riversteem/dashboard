while : 
do 
  python3 dashboard.py > tmp.html
  cat tmp.html |grep -v \{\' > index.html 
  sleep 5
done
