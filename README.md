# Country house price prediction

## Main goal
Building a model predicting a price for countryhouses & cottages in Belarus.

## Tasks to be realized
1. Collecting the data from web source using parsing technology
2. Data processing: handling duplicates, nan-values, features' types, outliers. Numeric & Categorical features processiong
3. Generating new features
4. EDA
5. Modeling, feature selection, hyperparameters optimization 
6. Model inference

## Data description

Primary dataset is one parsed from the web site realt.by. It contains data about cottages & countryhouses ads in Belarus in Apr 2024: more tha 16000 rows with 52 columns initially.

## Metrics

The evaluation metrics for the priject was R2 & MAE.


## Summary

At the 1st iterration of the project the main goal was building a model predicting a price only for countryhouses. Approximately 3000+ ads was parsed from realt.by. Taking into account relatively small size of the data set it was decided and seemed reasonable to use R2-score to evaluate model quality. When R2-score close to 0.7 was obtained I moved to the 2nd iterration. The new goal was reformulated: Building a model predicting a price for countryhouses, houses & cottages. This goal required more data for analysis. At the 2nd iterration more than 13000 ads was additionaly parsed from the same web source yieldind in total the data set with the shape (16187, 52). 

<i>Parsing (parsing.ipynb) </i>

The data was parsed from realt.by web-site using Selenium library & Chrome Webdriver engine. At the first step, the site feed containing brief information about the objects was scanned. The main goal at this stage: parsing ad URLs containing a unique identifier (ID)(data/pars_res{int}.txt). At the second stage, a loop of saved URLs was carried out and detailed information about the objects was collected and saved in csv-format (data/country_houses.csv & data/country_houses.csv).

<i>Data processing (code.ipynb)</i>

All parsed data was mainly saved as type 'object'. So at this step it was supposed to transform numeric data to int or float. Main part of collected data was categorical: some binary, another - multi. Due to the similarity of some Multicategorical feature options some options were merged after statistical assessment of the statistical significance of the difference between similar options. Both numeric and categorical features required handlind nan values, which was managed either by filling with median/mode value or str-value - depending on the feature type. Due to not normal distribution of the target feature (price) outliers were handled using +/- 1.5 IQR method (Interquartile Range).

<i>Generating new features (code.ipynb)</i>

Some additional features were generated and added to the data set. They mainly based on house coordinates data and include distances till district city, regional city and Belarus capital.

<i>EDA (code.ipynb)</i>

Data preprocessing helped to identify the main dependencies between features and the target variable - price. 

<i>Modeling (code.ipynb)</i>

LinearRegression was used as base model to be compared with. GradientBoosting appeared one of the most effective from the point of view of the metrics.
40 the most useful features were selected using SelectKBest. 

<i>Model inference (django folder)</i> 

GradientBoosting model fit with selected features was serialized and infered as back-end of web-application.
This step was realised using Django framework. Web application is actually deployed on https://housespriceprediction-production.up.railway.app/. 
Where it's available now for test purpose.

## Libraries & tools used
* see the requirements.txt 
