# py_otomoto
Tool for webscrapping and parsing Toyota Yaris II offers on otomoto.pl website.



## scrapy_otomoto

Scrapy 1.8.0 required, usage: 

```
cd ./scarapy_otomoto/
scrapy crawl otomoto
```

This will generate `otomoto_YYMMDD.html` file with all cars that are currently available and `YYMMDD` folder.  Folder contains  separate JSON files with details of each car.  



**carDataParser** - tool for parsing `otomoto_YYMMDD.html` file

**carFeatureParser** - tool for parsing JSON files

Result is stored in SQLite database

## www

Simple flask application for visualization of data. Preview: [remontmaszyn.pl](http://remontmaszyn.pl)

![](http://remontmaszyn.pl/static/img/mainpage.jpg)



---

Initial code:
https://bananovitch.github.io/blog/2018/09/19/python-car-scraper.html




