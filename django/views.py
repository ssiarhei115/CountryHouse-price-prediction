from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import UserForm
import pandas as pd
import pickle
import category_encoders as ce


menu = ['home', 'about']
best_features = ['Гараж', 'Новостройка', 'Элитный коттедж', 'house_area', 'house_levels', 'in_city', 'distance_house_region_min',
       'distances_multiply', 'Материал стен_дерево', 'Материал стен_блок г/с', 'Материал стен_блок',
       'Материал крыши_шифер', 'Материал крыши_черепица мет.', 'Материал крыши_черепица мяг.', 'Отопление_печь',
       'Отопление_электрич.', 'Отопление_паровое г.', 'Канализация_местная', 'Канализация_нет',
       'Канализация_с/у наружн.', 'Канализация_центральн.', 'Вода_сезонная', 'Вода_водопровод', 'Вода_колодец',
       'Вода_рядом колодец', 'Газ_нет', 'Газ_есть', 'Ремонт_отделка дер.', 'Ремонт_евроотделка', 'Район_Брестский', 'Район_другой',
       'Район_Минский', 'year_group_2000+', 'Тип объекта_дача', 'Тип объекта_дом', 'Тип объекта_коттедж', 'Тип объекта_таунхаус',
       'Населенный пункт_другой', 'Населенный пункт_г Минск', 'Населенный пункт_г Брест']

def index(request):
    
    if request.method == "POST":
        params = {
            #'name': request.POST.get("name", 'Unknown user'),
            #'mood': request.POST.get("mood", 'good'),

            'Гараж': 1 if request.POST.get("garage")=='on' else 0, 
            'new_build': 1 if request.POST.get("new_build")=='on' else 0, 
            'Элитный коттедж': 1 if request.POST.get("elite_cottage")=='on' else 0,
            'in_city': 1 if request.POST.get("elite_cottage")=='on' else 0, 
            'house_area': request.POST.get("house_area"), 
            'house_levels': request.POST.get("house_levels"), 
            'distance_house_district_city': float(request.POST.get("distance_house_district_city")),  
            'distance_house_region_min': float(request.POST.get("distance_house_region_min")), 
            'distance_house_minsk': float(request.POST.get("distance_house_minsk")), 
            'Материал стен': request.POST.get("walls"), 
            'Материал крыши': request.POST.get("roof"), 
            'Отопление': request.POST.get("heating"), 
            'Канализация': request.POST.get("sewerage"), 
            'Вода': request.POST.get("water"), 
            'Район': request.POST.get("district"), 
            'Газ': request.POST.get("gas"), 
            'Ремонт': request.POST.get("repair"),
            'year_group': request.POST.get("year_group"),
            'Тип объекта': request.POST.get("house_type"),
            'Населенный пункт': request.POST.get("city"),            
        }
        params['distances_multiply'] = params["distance_house_district_city"]*params["distance_house_region_min"]*params["distance_house_minsk"]
        user_df = pd.DataFrame(params, index=['user'])
        user_df.to_csv('user_data.csv')
        user_df = pd.read_csv('user_data.csv', index_col=0)

        ohe_list = ['Материал стен', 'Материал крыши', 'Отопление', 'Канализация', 'Вода','Газ',  'Ремонт', 'Район','year_group', 'Тип объекта', 'Населенный пункт']
        encoder = ce.OneHotEncoder(cols=ohe_list, use_cat_names=True)
        add = encoder.fit_transform(user_df.loc[:,ohe_list])
        user_df = pd.concat([user_df,add], axis=1)#.drop(ohe_list, axis=1)

        default_dict = {i:0 for i in best_features}
        for col in user_df.columns:
            if col not in default_dict.keys():
                user_df = user_df.drop([col], axis=1)
        
        concat_df =pd.concat([pd.DataFrame(default_dict, index=['default']), user_df], axis=0).fillna(0)
        concat_df.loc['result', :] = concat_df.sum()

        with open('price/model.pkl', 'rb') as pkl_file:
            model = pickle.load(pkl_file)

        predict = round(model.predict(concat_df.loc['result', best_features].values.reshape(1,-1))[0],1)
        
        return render(request, 'price/index.html', context={
            'params':params, 
            'menu':menu, 
            'title':'CountryHouse Price Predictor',
            'params_entered': 'PARAMETERS ENTERED:',
            'prediction_text': 'PRICE PREDICTED:',
            'predict':predict})
    else:
        params = {
            'title': 'CountryHouse Price Predictor',
            'menu': menu,
            'form': UserForm(),
            'submit_button': "<input type='submit' value='Submit' />",
            'params_enter': 'ENTER PARAMETERS',
        }
        return render(request, "price/index.html", context=params)


def about(request):
    params = {
        'title': 'About',
        'menu': menu,
        }
    return render(request, 'price/about.html', context=params)


def postuser(request):
    params = {
        'title': 'Request result',
        'menu': menu,
        'name': request.POST.get("name", 'Unknown user'),
        'mood': request.POST.get("mood", 'good'),
        'water': request.POST.getlist("water", 'колодец'),
    }
    return render(request, 'price/postuser.html', context=params)


def categories(request, cat_id):
    if cat_id > 100:
        #raise Http404()
        uri = reverse('catslug', args=('music',))
        return redirect(uri) #302, permanent=True - 301, redirect('home'), redirect('') 
    return HttpResponse(f'<h3>Categories</h3><p>id: {cat_id}</p>')


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h3>Categories</h3><p>slug: {cat_slug}')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h3>s/th wrong. can't find the page</h3>")
