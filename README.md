# Merctrans Project Manager 


## All services
- odoo 15 - Change version in docker-compose if you want. Example: odoo:14
- postgres 13
- pgadmin4 - Manage your postgres odoo database
- nginx - proxy server with config/odoo-nginx.conf
- debug docker  odoo
## Docker odoo python container
``` bash
docker exec -it web-odoo bash -c "odoo shell -d odoo"
```

## Odoo container Bash
Connect Postgres in docker 
```
docker exec -it web-odoo bash
# Sau khi connect duoc vao bash cua odoo service
psql -U odoo odoo

```
## pgadmin4 - Manage your odoo database in browser
connect pgadmin4 - port 5433 **localhost:5433**
**Create new server** \
Name your server then modify in **Connection** tab \
hostname/address : db \
username: odoo \
password: odoo \
