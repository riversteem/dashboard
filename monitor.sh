while : 
do 
  python3 dashboard.py > tmp.html # intermediate file to strip off headers from the API
  cat tmp.html |grep -v \{\' > index.html #This should land in your /var/www/html directory or similar
  sleep 3 # Refresh interval. Should be at or higher than block period.
done
