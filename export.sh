cd $1
sed -i 's/assets/static/g' index.html
mv index.html templates/home.html
mv assets static
