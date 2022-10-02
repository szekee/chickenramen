# DLW Hackathon

By team chickenramen.

For model building and datasets, refer to https://github.com/jieshengc/DLWHackathon-Models

## Problem Statement

As Singapore moves towards Smart Nation initiative, bad actors continue to use phishing attacks to obtain precious information from unsuspecting users. Furthermore, there is a exponential increase of phishing attacks using links, QR codes and more. This issue is exacerbated by Covid-19 as more Singaporeans shift online. Our project aims to use ML models to detect and prevent such attacks.

- 25% of Singapore’s population is predicted to be aged 65 and older by 2030, versus 14.4% in 2019. 
- As Singapore marches towards a Smart Nation Initiative. It has to take into account the massive eldery population that are vulnerable to such phishing attacks.
- Besides the elderly, COVID-19 taught our nation being to trust QR codes and URL redirects as we relied on these technologies to facilitate safe-entry access. 
- As a result of these technological adoption, there was been a 94% increase in scam frequency within the first half of 2022 alone as compared to 2021.
- However, the reliance on the aforementioned technology has also increased the amount of phishing attacks brought about by bad actors in society.
- Furthermore, the use of QR code to register for links have given rise to “Quishing”. It occurs when an individual uses QR code to trick people to share personal or financial information. 

## Business Value
- Gain customer trust through verification → Increased customer willingness to transact with the company → Builds brand loyalty → Increased revenue for the company
- Legitimacy of transactions are ensured → Reduces number of fraud cases faced by the company → Reduced losses to scams by the company → Increased profits for the company 
- Victims of phishing scams lost at least S$34.7 million in 2021 → Potential “gain” to Singapore society → Reduced number of phishing cases in Singapore

## Web Application
Built with Flask backend with a Javascript frontend.
Our web application allows users to either: Input a link in the app OR Input a QR Code in the app

From the backend,a built in QR Code reader will be able to extract the URL from the QR.
The URLs are then passed through our Feature Extractor and Machine Learning Ensemble Model.

The results will be displayed to the User on the Frontend.

## Running the Web Application

#### Clone Repository
Clone Repository by running: 
```
git clone https://github.com/szekee/chickenramen.git
```

#### Install Requirements
Install Requirements using:
Note: to install requirements, please ensure that python version is 3.7.14
```
pip install -r requirements.txt
```
For backend, in main folder run:
```
cd phishing_detector
npm install
```

#### Run Frontend
In the repository main folder run:
```
cd src
```
Then run
```
python main.py
```

#### Run Backend
In the repository main folder run:
```
cd phishing_detector
```
Then run
```
npm run dev
```
