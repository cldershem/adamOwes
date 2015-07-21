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
mkvirtualenv adamOwes
```

install dependencies
```sh
pip install -r requirements.txt
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

## LICENSE
See `TOPMATTER.md`
## COPYRIGHT
See `TOPMATTER.md`
## CONTRIBUTING
See `TOPMATTER.md`
