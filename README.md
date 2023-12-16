# Docker Odoo Production
## How to use this template
1. On GitHub.com, navigate to the main page of the repository.

2. Above the file list, click Use this template.

3. Select Create a new repository.

![helper](https://docs.github.com/assets/cb-77734/mw-1440/images/help/repository/use-this-template-button.webp)

[Learn More](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
## All services
- odoo 16 - Change version in docker-compose if you want. Example: odoo:14
- postgres 13
- pgadmin4 - Manage your postgres odoo database
- nginx - proxy server with config/odoo-nginx.conf
- debug docker  odoo
## How to deploy docker odoo production?
``` bash
docker-compose up -d
```
- Tunr off services
``` bash
docker-compose down 
```
- Turn off and delete all data
```bash
docker-compose down -v
```
## Docker odoo python container
``` bash
docker exec -it web-odoo bash -c "odoo shell -d odoo"
```
## How to include your module in odoo docker for production 
Simply put the folder of your local add-ons into the "local-addons" folder

## Odoo container Bash
Connect Postgres in docker 
```
docker exec -it web-odoo bash
# psql in container
psql -U odoo odoo

```
## pgadmin4 - Manage your odoo database in browser
connect pgadmin4 - port 5433 **localhost:5433**
**Create new server** \
Name your server then modify in **Connection** tab \
hostname/address : db \
username: odoo \
password: odoo \
