# py_otomoto
Tool for webscrapping and parsing Toyota Yaris II offers on otomoto.pl website.



## scrapy_otomoto

Scrapy 1.8.0 required, usage: 

```
cd ./scarapy_otomoto/
scrapy crawl otomoto
```

This will generate `otomoto_YYMMDD.html` file with all cars that are currently available and `YYMMDD` folder.  Folder contains  separate JSON files with details of each car in.  



**carDataParser** - tool for parsing `otomoto_YYMMDD.html` file

**carFeatureParser** - tool for parsing JSON files

## www

Simple flask application with visualization of data. Preview: [remontmaszyn.pl](remontmaszyn.pl)

![](http://remontmaszyn.pl/static/img/mainpage.jpg)



initial code:
https://bananovitch.github.io/blog/2018/09/19/python-car-scraper.html



---



### Features

"abs" : "ABS"
"cd" : "CD"
"central-lock" : "Centralny zamek"
"front-electric-windows" : "Elektryczne szyby przednie"
"electronic-rearview-mirrors" : "Elektrycznie ustawiane lusterka"
"electronic-immobiliser" : "Immobilizer"
"front-airbags" : "Poduszka powietrzna kierowcy"
"front-passenger-airbags" : "Poduszka powietrzna pasażera"
"original-radio" : "Radio fabryczne"
"assisted-steering" : "Wspomaganie kierownicy"
"alarm" : "Alarm"
"alloy-wheels" : "Alufelgi"
"asr" : "ASR (kontrola trakcji)"
"park-assist" : "Asystent parkowania"
"lane-assist" : "Asystent pasa ruchu"
"bluetooth" : "Bluetooth"
"automatic-wipers" : "Czujnik deszczu"
"blind-spot-sensor" : "Czujnik martwego pola"
"automatic-lights" : "Czujnik zmierzchu"
"both-parking-sensors" : "Czujniki parkowania przednie"
"rear-parking-sensors" : "Czujniki parkowania tylne"
"panoramic-sunroof" : "Dach panoramiczny"
"electric-exterior-mirror" : "Elektrochromatyczne lusterka boczne"
"electric-interior-mirror" : "Elektrochromatyczne lusterko wsteczne"
"rear-electric-windows" : "Elektryczne szyby tylne"
"electric-adjustable-seats" : "Elektrycznie ustawiane fotele"
"esp" : "ESP (stabilizacja toru jazdy)"
"aux-in" : "Gniazdo AUX"
"sd-socket" : "Gniazdo SD"
"usb-socket" : "Gniazdo USB"
"towing-hook" : "Hak"
"head-display" : "HUD (wyświetlacz przezierny)"
"isofix" : "Isofix"
"rearview-camera" : "Kamera cofania"
"automatic-air-conditioning" : "Klimatyzacja automatyczna"
"quad-air-conditioning" : "Klimatyzacja czterostrefowa"
"dual-air-conditioning" : "Klimatyzacja dwustrefowa"
"air-conditioning" : "Klimatyzacja manualna"
"onboard-computer" : "Komputer pokładowy"
"side-window-airbags" : "Kurtyny powietrzne"
"shift-paddles" : "Łopatki zmiany biegów"
"mp3" : "MP3"
"gps" : "Nawigacja GPS"
"dvd" : "Odtwarzacz DVD"
"speed-limiter" : "Ogranicznik prędkości"
"auxiliary-heating" : "Ogrzewanie postojowe"
"heated-windshield" : "Podgrzewana przednia szyba"
"heated-rearview-mirrors" : "Podgrzewane lusterka boczne"
"front-heated-seats" : "Podgrzewane przednie siedzenia"
"rear-heated-seats" : "Podgrzewane tylne siedzenia"
"driver-knee-airbag" : "Poduszka powietrzna chroniąca kolana"
"front-side-airbags" : "Poduszki boczne przednie"
"rear-passenger-airbags" : "Poduszki boczne tylne"
"tinted-windows" : "Przyciemniane szyby"
"radio" : "Radio niefabryczne"
"adjustable-suspension" : "Regulowane zawieszenie"
"roof-bars" : "Relingi dachowe"
"system-start-stop" : "System Start-Stop"
"sunroof" : "Szyberdach"
"daytime-lights" : "Światła do jazdy dziennej"
"leds" : "Światła LED"
"fog-lights" : "Światła przeciwmgielne"
"xenon-lights" : "Światła Xenonowe"
"leather-interior" : "Tapicerka skórzana"
"velour-interior" : "Tapicerka welurowa"
"cruise-control" : "Tempomat"
"active-cruise-control" : "Tempomat aktywny"
"tv" : "Tuner TV"
"steering-whell-comands" : "Wielofunkcyjna kierownica"
"cd-changer" : "Zmieniarka CD 