cd $1
sed -i 's/assets/\/static\/BootstrapAdmin/g' newTemplate.html
sed -i 's/assets/\/static\/BootstrapAdmin/g' setupCalendar.html
sed -i 's/assets/\/static\/BootstrapAdmin/g' templates.html
sed -i 's/assets/\/static\/BootstrapAdmin/g' 404.html
mv newTemplate.html templates/base/newTemplate.html
mv setupCalendar.html templates/base/setupCalendar.html
mv templates.html templates/base/templates.html
mv 404.html templates/base/404.html
mv assets static/BootstrapAdmin
