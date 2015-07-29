# Adam Owes
## He owes things all around town
### USE
clone
```sh
git clone git@github.com:cldershem/adamOwes.git
cd adamOwes
```

setup virtualenv
```sh
sudo apt-get install virtualenv virtualenvwrapper

# Py2.7
mkvirtualenv adamOwes

# Py3
mkvirtualenv --python=/usr/bin/python3 adamOwes-Flask3
```

install dependencies
```sh
# Py2.7
pip install -r requirements.txt

# Py3
pip3 install -r requirements3.txt
sudo apt-get install rabbitmq-server
```

secrets
```sh
cp secrets.py.example secrets.py
```
follow instructions in `secrets.py`

run
```sh
sudo a+x ./manage.py
./manage.py run
```

run on network
```sh
./manage.py run_on_network
```

populate db
```sh
./manage.py populate_db
```

run celery
```sh
celery -A app worker
```

## LICENSE
See [`TOPMATTER.md`](https://github.com/cldershem/adamOwes/blob/master/TOPMATTER.md#license)
## COPYRIGHT
See [`TOPMATTER.md`](https://github.com/cldershem/adamOwes/blob/master/TOPMATTER.md#copyright)
## CONTRIBUTING
See [`TOPMATTER.md`](https://github.com/cldershem/adamOwes/blob/master/TOPMATTER.md#contributing)
