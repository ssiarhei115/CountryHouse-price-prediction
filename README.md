# Country house price prediction

## Main goal
Building a model predicting a price for countryhouses & cottages.

## Tasks to be realized
1. Collecting the data from web source using parsing thechnology
2. Data processing: handling duplicates, nan-values, features' types. Numeric & Categorical features treating. Handling outliers
3. Generating new features
4. EDA
5. Modeling, feature selection, hyperparameters optimization 
6. Model inference

## Data description

Primary dataset is one parsed from the web site realt.by. It contains data about cottages & countryhouses ads in Belarus in Apr 2024.

<i> Data fields </i>
* 'Тип объекта' - Object type
* 'Номер договора' - Contract number
* 'Возможен торг' - Negotiable
* 'Номер дома' - House number
* 'Условия продажи' - Terms of sale
* 'Аукцион' - Auction
* 'index' - ad's id
* 'Площадь участка' - Land area
* 'Площадь общая' - Total area
* 'Уровней в доме' - house levels
* 'Год постройки' - year of construction
* 'Процент готовности' - percentage of readiness
* 'Координаты' - house coordinates
* 'Площадь жилая' - living area
* 'Площадь кухни' - kitchen area
* 'Ширина застройки' - building width
* 'Длина застройки' - building length
* 'Материал стен' - wall material
* 'Материал крыши' - roof material
* 'Отопление' - heating
* 'Канализация' - sewerage
* 'Электроснабжение' - electricity
* 'Вода' - water supply
* 'Телефон' - phone
* 'Область' - region
* 'Район' - district
* 'Населенный пункт' - city/town
* 'Сельсовет' - village council
* 'Газ' - if there ia gas
* 'Баня' - if there is a sauna
* 'Гараж' - if there is a garage
* 'Статус земли' - land status
* 'Сад' - if there is a garden
* 'Хозпостройки' - if there are outbuildings
* 'Рядом лес' - if there is a forrest nearby
* 'Водоем' - if there is a pond nearby
* 'Ландшафтный дизайн' - landscape design
* 'Улица' - street name
* 'Теплица' - if there is a glasshouse
* 'Мебель' - if there is a furniture
* 'Направление' - direction
* 'Ремонт' - interior renovation type
* 'Камин' - if there is a fireplace in the house
* 'Строительные материалы' - building materials
* 'Район города' - city district
* 'Беседка' - if there is a 'small-talk' pavilion 
* 'Микрорайон' - subdistrict
* 'Новостройка' - if house is new (just finished)
* 'Бассейн' - if there is a swimming pool
* 'Элитный коттедж' - if house is elite
* 'Пруд на участке' - if there is a pond
* 'Цена' - price, target feature


## Metrics

The evaluation metrics for the priject was R2 & MAE.


## Summary
<i>Parsing (parsing.ipynb, parsing_2.ipynb) </i>

The data was parsed from realt.by web-site using Selenium library & Chrome Webdriver engine. At the first step, the site feed containing brief information about the objects was scanned. The main goal at this stage: parsing ad URLs containing a unique identifier (ID). At the second stage, a loop of saved URLs was carried out and detailed information about the objects was collected.

<i>Data processing </i>

All parsed data was mainly saved as type 'object'. So at this step it was supposed to transform numeric data to int or float. Main part of collected data was categorical: some binary, another - multi. Due to similarity of some Multicategorical feature options some options were merfged after statistical assessment of the statistical significance of the difference between similar options. Both numeric and categorical features required handlind nan values, whith was managed either by filling with median/mode value or str-value - depending on the feature type.

<i>Generating new features</i>

Some additional features were generated and added to the data set. They mainly based on house coordinates data and include distances till district city, regional city and capital.

<i>EDA </i>

Data preprocessing helped to identify the main dependencies between features and the target variable - price. 

<i>Modeling </i>

LinearRegression was used as base model to be compared with. GradientBoosting appeared one of the most effective from the point of view of the metrics.
The most useful features were selected using SelectKBest module.

<i>Model inference</i> 

This step was realised using Django framework. The final model was deployed on domain.com. Where it's available now for test purpose.

## Libraries & tools used
* see the requirements 
