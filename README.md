# CryptoStat

An application in progress that analyzes the cryptocurency market in attempt to characterize the data and extract knowledge from that data.
Multiple sources of data will be taken as features in order to find the find what may influence the market directly or indrectly.
Reggression and classification will be used to learn from the data, such as classification for determining whether certain predictors are
important to classify good and bad candlesticks. Regression to predict outcomes of data.

Stat.py is used to generate the .csv files. These files will be edited in Matlab to create a final .csv file including all the predictors including GDP, average income, OHLC, and other features. From this final .csv file will the data be used by the machine learning algorithms.
