import pandas as pd;
import numpy;
import matplotlib;
import scipy;
import sklearn;
import kivy;
import urllib3;
import json;
import certifi;
import datetime as dt;
import time as timeLib;
#CSV
    #https://chrisalbon.com/python/data_wrangling/pandas_dataframe_importing_csv/

class Historical:

    def parseJsonToDictionary(numObjects, coins, duration, jsonFrame):
        historicalDict = {};

        connection = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where());
        for w in coins:
            request = connection.request('GET', 'https://min-api.cryptocompare.com/data/histo'+duration+'?fsym='+w+'&tsym=USD&limit='+str(numObjects));
            if request.status == 200:
                data = request.data;
                jsonObject = json.loads(data);
                data = jsonObject['Data'];
                print(data);
                ii = 0;
                dataDict = {};
                for y in jsonFrame:
                    tempList = [];
                    j = 0;
                    for z in data:
                        tempData = data[j];
                        tempList.insert(ii, tempData[y]);
                        j = j + 1;
                    dataDict[ii] = tempList;
                    ii = ii + 1;
            historicalDict[w] = dataDict;

        return historicalDict;

    def coinsToCsv(dict, coins, jsonFrame, dir):
        time = []; close = []; high = []; low = []; open = []; volumefrom = []; volumeto = [];

        for c in coins:
            convertedDate = [];
            all = [convertedDate, time, close, high, low, open, volumefrom, volumeto];
            list = dict[c];
            #initialize value lists
            for i in range(0, len(list)):
                all[i] = list[i];
                #print("length all : ", len(all[i]))
                if i is 0:
                    for j in range(0, len(all[i])):
                        stamp = all[i][j];
                        #index [0] for date (w/out time)
                        convertedDate.insert(j, str(Historical.unixTimeStampToDate(stamp)).split()[0]);
            #print("len(convertedDate): ", len(convertedDate));
            #rawData was here
            jsonFrame2 = ['date'] + jsonFrame;
            all2 = [x for x in all if x != []];
            #print(len(all2));
            #for ii in range(0, len(all2)):
                #print(len(all2[ii]));
            rawData = {'date': convertedDate,
                       'time': all2[0],
                       'close': all2[1],
                       'high': all2[2],
                       'low': all2[3],
                       'open': all2[4],
                       'volumefrom': all2[5],
                       'volumeto': all2[6]};
            df = pd.DataFrame(rawData, columns=jsonFrame2);
            lizt = [];
            b = False;
            for x in df.get_values():
                #print(x)
                for y in x:
                    #print(y)
                    #print("type: ", type(y))
                    if type(y) is type(0.0) and y == 0.0 or type(y) is type(0.0) and y is 0.0:
                        #print("ZERO FOUND!!!!!!")
                        b = False;
                        break;
                    else:
                        b = True;
                if b is True:
                    lizt.append(x)
            #for x in lizt:
                #print(x)

            all3 = [];
            l1=[]; l2=[]; l3=[]; l4=[]; l5=[]; l6=[]; l7=[]; l8=[];
            for x in lizt:
                l1.append(x[0])
                l2.append(x[1])
                l3.append(x[2])
                l4.append(x[3])
                l5.append(x[4])
                l6.append(x[5])
                l7.append(x[6])
                l8.append(x[7])
                all3 = [l1, l2, l3, l4, l5, l6, l7, l8];

            rawDataCleaned = {'date': all3[0],
                       'time': all3[1],
                       'close': all3[2],
                       'high': all3[3],
                       'low': all3[4],
                       'open': all3[5],
                       'volumefrom': all3[6],
                       'volumeto': all3[7]};
            df = pd.DataFrame(rawDataCleaned, columns=jsonFrame2);

            print(c);
            print(df);
            df.to_csv(dir+'/'+c+'.csv', index=False);

    def countriesToCsv(countryDict, countries):
        countryList = [];
        tempList = [];

        for cc in countries:
            countryList.append(str(cc).lower());

        for country in countryList:
            timeList = [];
            salaries = [];
            timeList = countryDict[country][0];
            salaries = countryDict[country][1];
            jsonFrame = ["date", "time", "salary"];

            dates = [];
            print(len(timeList))
            print(len(salaries))
            for d in timeList:
                dates.append(Historical.unixTimeStampToDate(d));

            rawData = {'date': dates,
                       'time': timeList,
                       'salary': salaries};
            df = pd.DataFrame(rawData, columns=jsonFrame);

            print(country);
            print(df);
            df.to_csv(dir + '/' + str(country) + '_avgSalaries.csv', index=False);

    def unixTimeStampToDate(timeStamp):
        date = dt.datetime.fromtimestamp(int(timeStamp)).strftime('%y-%m-%d %H:%M:%S');
        return date;

    def dateToUnixTimeStamp(date):
        parseDate = date.split("-");
        time = dt.date(int(parseDate[0]), int(parseDate[1]), int(parseDate[2]))
        unixTimeStamp = timeLib.mktime(time.timetuple());

        return int(unixTimeStamp);

    def getAdzunaByCountry(countries):
        month = [];
        countryList = [];
        for c in countries:
            countryList.append(str(c).lower());
        #print(countryList);

        countryDict = {};
        for country in countryList:
            url = "https://api.adzuna.com:443/v1/api/jobs/"+country+"/history?app_id=cdfe0292&app_key=443963c1650589a0b03967a3c6d97f47&months=48";
            connection = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where());
            request = connection.request('GET', url);
            if request.status == 200:
                month = [];
                monthFix = [];
                date = [];
                sal = [];

                data = request.data;
                jsonObject = json.loads(data);

                for x in jsonObject['month']:
                    month.append(x);
                    monthFix.append(str(x)+"-01");
                for t in monthFix:
                    date.append(Historical.dateToUnixTimeStamp(t));

                for key in month:
                    print("salllll: ", jsonObject['month'][str(key)])
                    sal.append(jsonObject['month'][str(key)]);

                all = [date, sal];
                countryDict[country] = all;

        return countryDict;

    def getAdzunaByCity(country, city):
        url = "http://api.adzuna.com/v1/api/jobs/gb/history?app_id=cdfe0292&app_key=443963c1650589a0b03967a3c6d97f47&location0=" + country + "&location1=" + city + "&category=it-jobs&content-type=application/json";
        locat = [];
        month = [];
        monthFix = [];
        sal = [];
        date = [];

        connection = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where());
        request = connection.request('GET',url);
        if request.status == 200:
            data = request.data;
            jsonObject = json.loads(data);
            print(jsonObject);

            where = str(jsonObject['location']['display_name']).split()[1];

            for i in range(0, len(jsonObject['month'])):
                locat.append(where);

            for x in jsonObject['month']:
                #just concat day=01
                month.append(x);
                monthFix.append(str(x)+"-01");

            for key in month:
                print(jsonObject['month'][str(key)])
                sal.append(jsonObject['month'][str(key)]);

            for t in monthFix:
                date.append(Historical.dateToUnixTimeStamp(t));

            all = [date, sal];
            return all;


#day (12:00 AM MAY 1 to 12:00 AM MAY2), hour, minute
duration = "day";
jsonFrame = ["time", "close", "high", "low", "open", "volumefrom", "volumeto"];
#returns n+1 objects
n = 2000;
coins = ["BTC", "ETC"];
countries = ["GB", "US"];
country = "UK";
city = "London";
dir = "C:/Users/yo/Desktop/CyrptoStat";

#Historical.getAdzunaByCity(country, city);
countryDict = Historical.getAdzunaByCountry(countries);
Historical.countriesToCsv(countryDict, countries);

h = Historical.parseJsonToDictionary(n, coins, duration, jsonFrame);
Historical.coinsToCsv(h, coins, jsonFrame, dir);





#predicting changes in volume
    #predictors 2:6 with response = the differences of volumeto - volumefrom with fine tree best results for a single currency
#predicting price
    #Now take average of high and low prices for a price as response.
    #with close, volumefrom, volumeto as predictors get high r-squared = 1
    #without close, but with time, volumefrom, volumto as predictors get insig less r-squared, awesome??
#predict avg price with time
    #HIGh R^2 with curve fitting polynomial degree 9

#*********use non-cryptocurrency predictors such as data about difference currencies like USD, KRW
    #append those predictors as columns to the matrix in matlab !