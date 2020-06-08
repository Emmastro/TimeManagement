cd $1
sed -i 's/assets/\/static\/BootstrapAdmin/g' index.html
sed -i 's/assets/\/static\/BootstrapAdmin/g' period.html
sed -i 's/assets/\/static\/BootstrapAdmin/g' 404.html
mv index.html templates/admin_.html
mv period.html templates/period_.html
mv 404.html templates/404_.html
mv assets static/BootstrapAdmin
