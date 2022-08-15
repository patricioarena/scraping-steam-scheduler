## Scraping steam scheduler

El presente proyecto es un proceso encargado de realizar el raspado de datos de **Steam** y posteriormente guardarlo en mongodb.

### Variables de configuración
|VAR               				|TYPE 									|
|-------------------------------|---------------------------------------|
|AUTO_SCROLL_ACTIVE				|bool              						|
|CHROMEDRIVER_PATH				|**/app/.chromedriver/bin/chromedriver**|
|CONNECTION_STRING				|str									|
|DRIVER_WAIT					|int									|
|GOOGLE_CHROME_BIN				|**/app/.apt/usr/bin/google-chrome**	|
|LIMIT_ITERATION				|int									|
|PYTHONUNBUFFERED				|1										|
|SCRAPING_URL					|https://store.steampowered.com/search/?specials=1|
|TIME_SLEEP						|10										|
|TYPE_JOB						|**cron** OR **interval**				|
|TIMEZONE| Asia/Kolkata|   
|RUN_TIME|17:00|


Si se usa **interval** agregar
|VAR               				|TYPE 									|
|-------------------------------|---------------------------------------|
|SCHULER_MINUTES				|int **>=** 10 							|

Usando **cron** el trabajo es programado una vez por día laborable solo a las 5:00 p. m.

 ### Buildpacks para Heroku
 **heroku/python** <br>
 **https://github.com/heroku/heroku-buildpack-google-chrome** <br>
 **https://github.com/heroku/heroku-buildpack-chromedriver** <br>

 ### Almacenamiento de datos

Cada vez que se almacenan los datos se genera una nueva colección a la que se le da como nombre la fecha y hora en que se   realizo el proceso de raspado ejemplo.

> **2022-08-13T03:29:37.773481**

```json
[
	{
		"_id": ObjectId("62f71b775c3478613015d225"),
		"name":"Street Fighter V - Champion Edition Upgrade Kit",
		"link":"https://store.steampowered.com/app/...",
		"img":"https://cdn.akamai.steamstatic.com/steam/apps/...",
		"discount":null,
		"price_without_discounted":null,
		"price_with_discounted":null
	},
	{
		"_id": ObjectId("62f71b775c3478613015d22e"),
		"name":"Batman: Arkham Collection",
		"link":"https://store.steampowered.com/app...",
		"img":"https://cdn.akamai.steamstatic.com/steam/apps/...",
		"discount":"85",
		"price_without_discounted":"59.99",
		"price_with_discounted":"8.99"
	}
]
```

Al final de cada colección se puede encontrar un objeto que almacena el tiempo que tardo el proceso en realizar las tareas de raspado y almacenamiento.

```json
[
	{
		"_id": ObjectId("62f71b775c3478613015d22e"),
		"scraping_total_time":56.97572660446167,
		"mongo_total_time":0.9730274677276611
	}
]
```
