# ANT+ Virtual Power Meter



## Clone app
* `git clone https://github.com/karthicksakkaravarti/vpower.git`
* `cd vpower`


## Building GUI 

Windows
* Clone or download this repo
* `npm install`
* `npm run electron:build` cmd will generate electron_dist folder

Mac

* https://www.electronjs.org/docs/latest/development/build-instructions-macos

## Running Server 

* `pip install -r requirements.txt`
* `python manage.py migrate`
* `python manage.py runserver 9010`

## Accessing GUI

* Open GUI app under  `/dist_electron/win-unpacked/vPower.exe` by double clicking
