## environment variables
je potřeba nastavit 2 .env files:

`cardMakerFE/.env`

obsahuje nastavení adresy pro FE, liší se podle toho jestli FE běží v kontejneru (produkce) nebo samostatně (vývoj) :
```
PUBLIC_BASE_API_URL="http://localhost:8003" # For development
PUBLIC_BASE_API_URL="/api" # For production
PUBLIC_USE_API_KEY="false" # "true" for use api key
```


`.env`
obsahuje nastavení pro docker-compose:

```
DATABASE_URL= "mysql+mysqlconnector://root:root@db:3307/Cardmaker"
SECRET_KEY= "6de9b7c10564fb4794c13a2c127b5a00e21259cd56df440aad5199dae182966b"
API_KEY="viroujimesalat"
API_KEY_USE="false" # "true" for use api key

MYSQL_ROOT_PASSWORD="root"  
MYSQL_DATABASE= "Cardmaker"
MYSQL_USER= "user"
MYSQL_PASSWORD= "pass"
MYSQL_TCP_PORT="3307"
```