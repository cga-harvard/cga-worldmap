pg_new_host='192.168.100.20'
pg_old_host='192.168.100.8'
pg_password='mypassword'

for db_store in wmdata dataverse wm_201605 wm_201606 wm_201607 wm_201608 wm_201609 wm_201610 wm_201611 wm_201612 wm_201701 wm_201702 wm_201703 wm_201704 wm_201705 wm_201706 wm_201707 wm_201708 wm_201709 wm_201710 wm_201711 wm_201712 wm_201801 wm_201802; do
    echo updating $db_store
    sed -i -e "s|<entry key=\"host\">$pg_old_host</entry>|<entry key=\"host\">$pg_new_host</entry>|g" $db_store/datastore.xml
    pw_string="    <entry key=\"passwd\">$pg_password</entry>"
    echo $pw_string
    sed -i "/passwd/c\\$pw_string" $db_store/datastore.xml
done
