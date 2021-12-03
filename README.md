# Covid-19 Dashboard



### Table of Contents
- [Description](#description)
- [Prerequisties](#prereusites)
- [How To Use](#how-to-use)
- [Testing](#testing)
- [Developer Manual](#developer-manual)
- [Refrences](#references)
- [License](#license)
- [Author Info](#author-info)

---

## Description

The Covid19 dashboard is a web application that keeps upto date with the current infection rates, both nationally and 
locally, also showing all upto date news. The dashboard coordinates information about Covid-19 infection rates from the Public Health England API and news stories about Covid from the given news API, specified in the config.json file. Events are not automated on the dasboard, the events are either secheduled from inside the source code or/but mostly triggerd by the user inputs meaning the software is built around an event-driven architecture; with the use of flask. All of the backend is coded in python with flask linking the backend with the front end, which is coded in html with flask bootstramp templating embedded in it.

[Back To The Top](#covid-19-dashboard)

---

## Prerequisites

1. Pyhton 3.9+
2. requests 2.26.0+
3. sched 3.10.0+
4. uk_covid19 1.2.2+
5. flask 2.0.2+


[Back To The Top](#covid-19-dashboard)

---


## How To Use

### Installation
1. Once you have dowloaded the respoiroty, open the command prompt in the directory the project is located, then use the following command
```
$ cd Covid19-Dashboard
```
2. Then using pip use the following command 
```
$ pip install -r requirements.txt
```
* If you don't have pip installed, first install pip.
    Once pip is install, go back and complete step 2
3. Once everthing has been installed correctly the appilication should have all the required modules to run.

### Getting your own API key:
This step is also mandatory to get the software to run. To get an api key go to newsapi.org and register for an account. Once registered make note of your key as you will need this is the following steps

### Configuring the dashboard:
To change the default locaions of the Public Health England API, news sources and API key, you will need to open the config.json file and change the default values to ones you wish to use. This must be done before running the program to have a personalised dashboard. The source code will not need to be edited at any point if you change data in the config.json file. For the software to be run you will have to put your own api key into the config file, this is the only mandatory change you will have to do in the config file

### How to run the dashboard:
To run the dashboard, run main.py. Then go onto your prefered browser and enter http://127.0.0.1:5000/. If you get errors there is a chance that you do not have the required modules installed: flask, uk_covid19, sched. These modules are necessary to run the application. Refer back to the [isntallation](#installation) to resolve these errrors.

[Back To The Top](#covid-19-dashboard)

---
## Testing

A routine test has already been embedded in the code, and will be triggered at 6am every morning. These tests test the main functions of the program including API grabs and checking scheduled updates can be made and removed. More tests can be found in the tests file, where there is dedicated tests for each function in each module. To run these tests use pytest, or you can go into the routine_test.py and include the extra tests you wish to run in the routine cycle.

[Back To The Top](#covid-19-dashboard)


---
## Developer Manual
--> TODO

[Back To The Top](#covid-19-dashboard)

---

## Refrences

- GitHub - [@Jude Wallace](https://github.com/JudeWallace?tab=repositories)

[Back To The Top](#covid-19-dashboard)

---

## License

MIT

Copyright (c) [2021] [Jude Wallace]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[Back To The Top](#covid-19-dashboard)

---

## Author Info

- GitHub - [@Jude Wallace](https://github.com/JudeWallace?tab=repositories)

[Back To The Top](#covid-19-dashboard)