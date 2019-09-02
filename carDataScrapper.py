import requests, bs4, io, csv, datetime

#path = 'https://www.otomoto.pl/osobowe/toyota/yaris/od-2008/?search[filter_float_year%3Ato]=2008'
path = 'https://www.otomoto.pl/osobowe/toyota/yaris/ii-2005-2011/'


res = requests.get(path)
res.raise_for_status()

now = datetime.datetime.now()

#prepare the file
fname = 'carData___'+ str(now.date()) +'.csv'
carFile = io.open(fname, 'w', encoding="utf-8")


#check how many pages are there
carSoup = bs4.BeautifulSoup(res.text, features="lxml")
lastPage = int(carSoup.select('.page')[-1].text)

#csv file header
carFile.write('IDX,Price,City,Region,Model,Year,Mileage,Displacement,Petrol'+'\n')

for i in range(1, lastPage):
    res = requests.get(path + '?page=' + str(i))
    res.raise_for_status()
    currentPage = bs4.BeautifulSoup(res.text, features='lxml')
    carList = currentPage.select('article.offer-item')
    print("parsing page " + str(i))
    for car in carList:
        #get the interesting data and write to file
        try:
            ID = car.find('input', {'name': 'contact[adid]'}).get('value')
            carFile.write(ID + ',' )
        except:
            pass

        price = car.find('span',class_='offer-price__number').text.strip()
        price = price.replace(" ", "")
        carFile.write(price[:-4] + ',' )

        city = car.find('span',class_='ds-location-city').text.strip()
        carFile.write(city + ',' )

        region = car.find('span',class_='ds-location-region').text.strip()
        carFile.write(region + ',' )

        title = car.find('a',class_='offer-title__link').text.strip()
        carFile.write(title + ',' )
        params = car.find_all("li", class_='offer-item__params-item')
        for param in params:
            strip_txt = param.text.strip()
            strip_txt = strip_txt.replace(" ", "") # remove empty spaces
            strip_txt = strip_txt.replace("km", "") # remove km symbol
            strip_txt = strip_txt.replace("cm3", "") # remove cm3 symbol

            carFile.write(strip_txt+ ',')   
        carFile.write('\n')
    
carFile.close()