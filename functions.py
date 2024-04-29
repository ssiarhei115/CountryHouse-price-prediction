import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.common.exceptions import TimeoutException
import re
import geocoder 
from sklearn import metrics 
import geopy.distance


def draw_categories(df,features, ax_width=10, tick_rotation=30):
    """Visualization of category value_counts (left image) & categories VS price (right image)   

    Args:
        features ('object'): feature name
        ax_width (int, optional): width of fthe figure. Defaults to 10.
        tick_rotation (int, optional): tick rotation angle. Defaults to 30.
    """
    n = len(features) 
    fig, axes = plt.subplots(n, 2, figsize=(ax_width, n*3)) 

    for i, feature in enumerate(features):
        #print(n,i,feature)
        count_data = (df[feature].value_counts(normalize=True)
                  .sort_values(ascending=False)
                  .rename('percentage')
                  .reset_index())
        sns.barplot(data=count_data, x=feature, y='percentage', ax=axes[i][0], width=0.4).set(title=f'{feature} (ratio)', xlabel='');
        axes[i][0].xaxis.set_tick_params(rotation=tick_rotation)
        sns.barplot(df, x=feature, y='price', ax=axes[i][1], width=0.4).set(title=f'{feature} (price)', xlabel='');
        axes[i][1].xaxis.set_tick_params(rotation=tick_rotation)
    plt.tight_layout() 
  


def outliers_z_score(data, feature, left=3, right=3, log_scale=False):
    """Remove outliers according 3 sigma method

    Args:
        data (dataframe): source dataframe
        feature (string): feature name
        log_scale (bool, optional): if the feature should be logarithmizeв. Defaults to False.

    Returns:
        dataframe: dataframe without outliers
    """
    if log_scale:
        x = np.log(data[feature]+1)
    else:
        x = data[feature]
    mu = x.mean()
    sigma = x.std()
    lower_bound = mu - left * sigma
    upper_bound = mu + right * sigma
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x >= lower_bound) & (x <= upper_bound)]
    return cleaned


def outliers_iqr_mod(data, feature, left=1.5, right=1.5, log_scale=False):
    if log_scale:
        x = np.log(data[feature])
    else:
        x = data[feature]
    quartile_1, quartile_3 = x.quantile(0.25), x.quantile(0.75),
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * left)
    upper_bound = quartile_3 + (iqr * right)
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x >= lower_bound) & (x <= upper_bound)]
    return cleaned


def stat_compare(data,category, category_opt_1, category_opt_2, alpha=0.05):
    """ Assess if the difference between feature options is statistically significant

    Args:
        category (_type_): _description_
        category_opt_1 (_type_): _description_
        category_opt_2 (_type_): _description_
        alpha (_type_, optional): _description_. Defaults to alpha.

    Returns:
        _type_: _description_
    """
        
    opt_1 = data[data[category]==category_opt_1]['price']
    opt_2 = data[data[category]==category_opt_2]['price']
    max_opt = data[data[category].isin([category_opt_1,category_opt_2])][category].value_counts().idxmax()

    def get_normality(data, alpha=alpha):
        _, p = stats.shapiro(data)
        if p <= alpha:
            return 1
        else:
            return 0
    
    def test_t(data_1, data_2, alpha=alpha):
        result = stats.levene(data_1, data_2)
        p = result[1]
        if p <= alpha:
            equal_var=False
        else:
            equal_var=True

        _, p = stats.ttest_ind(data_1, data_2, alternative='two-sided', equal_var=True)
        if p <= alpha:
            return 'not equal'
        else:
            return 'equal'


    def test_mannwhit(data_1, data_2, alpha=alpha):
        _, p = stats.mannwhitneyu(data_1, data_2, alternative='two-sided')
        if p <= alpha:
            return 'not equal'
        else:
            return 'equal'
    
    norm_1 = get_normality(opt_1)
    norm_2 = get_normality(opt_2)

    if norm_1==0 and norm_2==0:
        res = test_t(opt_1,opt_2)
        if res == 'equal':
            return f"{category.upper():} {category_opt_1} ({get_normality(opt_1)}), {category_opt_2} ({get_normality(opt_2)}): {res.upper()} --> {max_opt}"
        else:
            return f"{category.upper():} {category_opt_1} ({get_normality(opt_1)}), {category_opt_2} ({get_normality(opt_2)}): {res}"
    else:
        res = test_mannwhit(opt_1,opt_2)
        if res == 'equal':
            return f"{category.upper():} {category_opt_1} ({get_normality(opt_1)}), {category_opt_2} ({get_normality(opt_2)}): {res.upper()} --> {max_opt}"
        else:
            return f"{category.upper():} {category_opt_1} ({get_normality(opt_1)}), {category_opt_2} ({get_normality(opt_2)}): {res}" 



def get_district_details(district_name):
    service = Service(executable_path=r'/usr/bin/chromedriver')
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless') #It allows users to run automated scripts in headless mode, meaning that the browser window wouldn’t be visible. 
    driver = webdriver.Chrome(service=service, options=options)
    url = 'https://google.com'#"https://realt.by/sale/dachi/?page=1"
    headers = ({'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0', 'Accept-Language':'en-US, en;q=0.5'})
    driver.get(url);
    time.sleep(1)
    #input_box = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea")))
    input_box = driver.find_element(By.CSS_SELECTOR, "textarea")
    input_box.send_keys(district_name)
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

    wiki_link = driver.find_element(By.XPATH,"//a[contains(@href, 'https://ru.wikipedia.org')]")
    wiki_link.click()

    def get_soup(page):
        soup = BeautifulSoup(page, 'html.parser')
        res = soup.find("span", class_='coordinates plainlinks nourlexpansion').find("a").text
        res = re.findall(r"(\d{2}\°\d{2,}\′*\d*).", res)
        res = [x.replace('°','.') for x in res]
        res = [x.replace('′','') for x in res]
        return (res[0],res[1])
    
    res_1 = get_soup(driver.page_source)

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        res = soup.find_all('tr')
        for i in res:
            if i.find('th') and i.find('th').text == 'Адм. центр':
                wiki = i.find('a').text
        wiki_link2 = driver.find_element(By.LINK_TEXT, wiki)
        wiki_link2.click()
        res_2 = get_soup(driver.page_source)
    except:
        res_2 = res_1
        

    driver.quit()
    
    return [(float(res_1[0]), float(res_1[1])), (float(res_2[0]), float(res_2[1]))]


def get_location(name):
    try:
        g = geocoder.bing(name, key='AgY4Qy8qL2I1oMf6xu6SSpqncKEFzpjZIKzs3Y_lhKvdA4cRPMUpBEIDmgXxm5_e')
        results = g.json
        #print(name, results['lat'], results['lng'])
        return (results['lat'], results['lng'])
    except:
        print('exception', name)
        return name
    

def get_metrics(y_train, y_train_predict, y_test, y_test_predict, y_test_dacha, y_test_pred_dacha, only_mae=False):
    train_r2 = round(metrics.r2_score(y_train, y_train_predict),2)
    train_mae = round(metrics.mean_absolute_error(y_train, y_train_predict),2)
    test_r2 = round(metrics.r2_score(y_test, y_test_predict),2)
    test_mae = round(metrics.mean_absolute_error(y_test, y_test_predict),2)
    test_dacha_r2 = round(metrics.r2_score(y_test_dacha, y_test_pred_dacha),2)
    test_dacha_mae = round(metrics.mean_absolute_error(y_test_dacha, y_test_pred_dacha),2)
    err_dict = {'r2':[train_r2,test_r2,test_dacha_r2], 'mae':[train_mae,test_mae, test_dacha_mae]}
    if only_mae:
        return pd.DataFrame(err_dict['mae'], index=['TRAIN', 'TEST', 'TEST_dacha']) 
    else:
        return pd.DataFrame(err_dict, index=['TRAIN', 'TEST', 'TEST_dacha'])


def get_distance(data,d1,d2,regions_dict, extra=0):
    coord1 = str(d1).replace(',',' ').lstrip('(').rstrip(')').split()
    coord2 = d2.replace(',',' ').lstrip('(').rstrip(')').split()
    distance = geopy.distance.geodesic((float(coord1[0]),float(coord1[1])), (float(coord2[0]),float(coord2[1]))).km

    if extra == 0:
        return round(distance,1)
    else:
        distances = dict()
        for key in regions_dict:
            distances[key] = geopy.distance.geodesic((float(coord1[0]),float(coord1[1])), (regions_dict[key][0],regions_dict[key][1])).km
        distance_region_min = min(distances.values())
        return(round(distance,1), round(distance_region_min,1))