# Covid-19 Dashboard



### Table of Contents
- [Description](#description)
- [Prerequisties](#prereusites)
- [How To Use](#how-to-use)
- [Testing](#testing)
- [Developer Manual](#developer-manual)
- [Refrences](#refrences)
- [License](#license)
- [Author Info](#author-info)

---

## Description

The Covid19 dashboard is a web application that keeps upto date with the current infection rates, both nationally and locally, also showing all upto date news. The dashboard coordinates information about Covid-19 infection rates from the Public Health England API and news stories about Covid from the given news API, specified in the config.json file. Events are not automated on the dasboard, the events are either secheduled from inside the source code or/but mostly triggerd by the user inputs meaning the software is built around an event-driven architecture; with the use of flask. All of the backend is coded in python with flask linking the backend with the front end, which is coded in html with flask bootstramp templating embedded in it.

[Back To The Top](#covid-19-dashboard)

---

## Prerequisites

1. Python 3.9+
2. uk_covid19 1.2.2+
3. flask 2.0.2+


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

A routine test has already been embedded in the code, and will be triggered at 6am every morning. These tests test the main functions of the program including API grabs and checking scheduled updates can be made and removed. More tests can be found in the tests file, where there is dedicated tests for each function in each module. To run these tests use pytest, or you can go into the routine_test.py and include the extra tests you wish to run in the routine cycle. The tests are setup for the use of the pytest module

[Back To The Top](#covid-19-dashboard)


---

## Developer Manual

The code has been created using an event driven archicture. With python as the backend, with the use of flask to create the functionality; with the frontend being coded in HTML, created as a flask template.
The project is split into 3 main modules: covid_data_handler.py, covid_news_handling and main.py. However other modules are required for smaller tasks. The logical structure of the software is the events are triggered by the user in the webpage which are picked up in the main.py, which then calls the backend modules to fufill the request and return back to the main.py the result of the event to be updated on the webpage.

### covid_data_handler.py

This module is responsible for dealing with all the statistical data needed for the software. This module uses the uk_covid19 module to allow for an API call to get all the upto date covid data. All the processing of the data is also contained in this module. Once the API call has been made, from the covid_API_request(), it updates the covid_data_cache.csv with all the new data on covid. Updates of this data can be called using the update_covid_data_json() function, this functions calls the API request function twice; once with the local area setting, then another time with the national area settings. Once the funciton has stored all the data values in corresponding local varaibles, a dictionary of these values are stored in a .json file(dashboard_covid_data.json). To get this data from the json to the main.py the function dashboard_covid_data() is called which returns all the data required on the dashboard out of the json file.

### covid_news_handling.py

All of the news requests and editing of the news articles is contained within this module. The news can be grabbed using an API call which returns the news source which match the parameters given. Once the news has been grabbed it is stored in the covid_news_data.json file. Updating the news which is specified by the user occurs in the update_news() funtion. This function removes the articles from the json file if the user presses the X on the widget and also is where an event is created in the scheduler if the user requests the news articles to be updates. Similarly to the covid_data_handler module the dashboard_news() function returns the articles, title and cotents with a hypertext link, to the main.py ready to be shown on the webage.

### Main.py

Where the connection between user triggerd events and the corresponding backend tasks are triggered and returned what the triggerd event caused. This module is built around an event driven architecture. Within the submitted_form() function, also the decerator methed, it started the scheduler with blocking=false to allow for events to be scheduled and not have to wait for them to complete for the code to continue. The code the checks if the user has triggered an event, such as removing an article. If an event is triggered it will complete its tasks before then continuing to the final section. The next section is responbsile for checking the scheduler is upto date with all the necessary events, but this section is also responsible for removing scheduled widgets which has been ran and executed. The final section of code is there to make sure the deployed test cycle is in the schedule ready to be run, if it has been ran for the day it'll readd the test cycle to the queue for the following day. The function then returns using the function render_template all the updates global variables containg dictionaires of all the required information to be rendered onto the webpage.

### time_conversion.py

This module converts a time from a string format to its correct delay in seconds, the returned value is the delay used when the event is created in other modules.

### routine_tests.py

This module creates an event in the scheduler for 6am everyday at which a selection of tests will be run on the code to make sure the main functionality is still working and has outcomes orginally expected/required.

### scheduler.py
Creates are scheduler object which is imported into each module, to be used to create and remove events.

### Tests
Tests for each module and function can be found in the tests folder. The tests are coded to allow pytest to be used to test the code at any time other than on the deployed test cycle


### Logging
Throughout the code I have implemented logging into each module. There are 3 log files; backend_log.log, for the modules covid_data_handler, covid_news_handling and time_conversion: frontend_log.log, for the main.py module which logs all the events truggered by the user: routine_tests, which logs when the test deployment cycle is created and ran, and logs any assertion errors which may occur.

### Further Development

The project could be adapted and built upon in several ways. A key area for improvement is the CSS of the webpage, which could make it more appealing; instead of only being text the news widgets could show the title and image of the news articles. Futher development could also be implemented on the testing schedule, which could be developed further with the use of a unit testing cycle. Another main improvement would be reducing the amount of files created and needed for the software, with the use of passing global data structures of the required information to the main.py instead of having to read a file for it to then be passed to the main.py.

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