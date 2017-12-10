# stock-sim
### By Sam Burba and Long Nguyen

### To install and run:
 ```bash
	virtualenv -p python3 env
	source env/bin/activate
	pip install -r requirements.txt
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver
```
### TO ADD STOCKS TO THE DATABASE:
**This is a manual process, be warned!**
* Open up the contents of */stocks/stock\_uploader.py* and copy the contents.
* Run ```python manage.py shell``` and paste the contents into the terminal.
* Run the command.
Now all the stocks are in the database.

The website can be seen at [stock-sim.com](http://stock-sim.com)

