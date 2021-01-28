import re
import sys
import os
import string
import json
import datetime
from dateutil import parser 
from twython import Twython
from collections import Counter as ctr 
from random import randrange, choice

now = datetime.datetime.now()
day = int(now.day)
month = int(now.month)
year = int(now.year)


class TwitterCrawler:
    # Instancia para hacer peticiones al API
    def __init__(self):
        self.t = Twython(app_key= 't3cyFSkiWB4bSbUCOfKFQfdmU', 
                            app_secret= 'NMNpeBPl4Xb7Fppk3K2jGkuvEqut0X4xHv4Mi0n4PAvHlBMQmr',
                            oauth_token= '612153534-YdrJtLDMP4q5PzXNvlkVKQYAKK8manQOfdIorIfd', 
                            oauth_token_secret= 'wJFbjSZSYT4raoMYMTsaA76WUTklEYgW7gQzMG4h6xNFs')
        self.trends = list()

    # get twenty tweets from specific account 
    def get_twenty_tweets(self):

        print('Getting tweets . . .')

        # get profile info (dict)
        profile= self.t.show_user(screen_name= 'conagua_clima')

        account_name= profile['name']
        print('Cuenta: ' + account_name)
        print('Creada en: ' + profile['created_at'])

        # time parser
        #xtime= parser.parse(profile['created_at'])

        # uses search method to find conagua_clima queries (dict)
        #gross_tweets= self.t.search(q= "conagua_clima", tweet_mode= "extended", count="10")
        
        # list()
        gross_tweets= self.t.get_user_timeline(screen_name= "conagua_clima", tweet_mode= "extendend", count= 30)

        # object attributes
        #print(gross_tweets[0].keys())

        oneTweet= 'W'

        # use get_user_timeline method
        for item in gross_tweets:
            text= item['text']
            oneTweet= oneTweet + text + ' '

        return oneTweet


    def pipeline(self):

        print("Inicia módulo: Recolector")
        tweetString= self.get_twenty_tweets()
        #print(tweetString)

        return tweetString


class DataAnalysis:
    
    def hashtagSearch(self, totalText):

        print('Getting keywords . . .')
        # texto representado por palabras
        word_list= totalText.split()
        actual_hashtags= list()
        actual_states= list()    
        forecast= list()
        temperatures= list()
        temp= 0

        states= ['Aguascalientes', 'BajaCalifornia', 'BajaCaliforniaSur', 'Campeche', 'CDMX', 'Chiapas',
                    'Chihuahua', 'Coahuila', 'Colima', 'Durango', 'EdoMéx', 'Guanajuato',
                    'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán', 'Morelos', 'Nayarit', 'NuevoLeón', 
                    'Oaxaca', 'Puebla', 'Querétaro', 'QuintanaRoo', 'SanLuisPotosí', 'Sinaloa', 'Sonora',
                    'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Zacatecas', 'ValleDeMéxico', 'México']

        # Realiza búsqueda de hashtags
        for item in word_list:
            if item[0] == '#':
                actual_hashtags.append(item)

        # Une en una cadena el contenido de actual_hashtags
        key_string= '<> '
        for item in actual_hashtags:
            key_string= key_string + item + ' '

        # elimina los signos de puntuación 
        new_str = re.sub(r'[^\w\s]','',key_string)        
        #print(new_str)

        # Crea lista de pronósticos
        for item in new_str.split():
            if item not in states:
                if item not in forecast:
                    forecast.append(item)
        
        # Realiza la busqueda de temperaturas
        """
        for item in word_list:
            if int(item.isdigit()):
                temperatures.append(item)
                temp= temp + int(item)
        # calcula la temperatura promedio         
        mean_temp= temp // len(temperatures)
        #print(mean_temp)
        """

        # Crea lista de estados
        for item in new_str.split():
            if item in states:
                if item not in actual_states:
                    actual_states.append(item)

        # crea estado del tiempo
        estado_tiempo= dict()
        estado_tiempo= {'account_name': 'SMN',
                        'date': [month, day, year],
                        'states': actual_states,
                        'forecast': forecast
        }

        #print('\n', estado_tiempo)
        return estado_tiempo

    def weather(self, hS):
        print('Calculating the weather . . .')
        #print(hS)

        # Estaciones del año
        invierno= {'temperatura': ' bajas temperaturas ',
                    'clima': ['Frío', 'Lluvias', 'Nieve']}
        primavera= {'temperatura': ' temperaturas oscilando los 25 °C',
                    'clima': 'Cálido'}
        verano= {'temperatura': ' altas temperaturas ',
                    'clima': ['Calor', 'Caluroso']}
        otoño= {'temperatura': ' temperaturas agradables ',
                    'clima': 'Fresco'}

        # Regiones de la República Mexicana
        region_1= {'region': ' Región NorOeste ',
                    'estados': ['BajaCalifornia', 'BajaCaliforniaSur', 'Chihuahua', 'Durango', 'Sinaloa', 'Sonora'],
                    'semaforo': 'Naranja y Rojo'}
        region_2= {'region': 'Región NorEste',
                    'estados': ['Coahuila', 'NuevoLeón', 'Tamaulipas'],
                    'semaforo': 'Naranaja'}
        region_3= {'region': 'Región Occidente',
                    'estados': ['Nayarit', 'Jalisco', 'Colima', 'Michoacán'],
                    'semaforo': 'Naranja'}
        region_4= {'region': 'Región Oriente', 
                    'estados': ['Puebla', 'Veracruz', 'Tlaxcala', 'Hidalgo'],
                    'semaforo': 'Naranja y Amarillo'}
        region_5= {'region': 'Región Centro Norte',
                    'estados': ['Aguascalientes', 'Guanajuato', 'SanLuisPotosí', 'Zacatecas', 'Querétaro'],
                    'semaforo': 'Naranja y Rojo'}
        region_6= {'region': 'Región Centro Sur',
                    'estados': ['Morelos', 'EdoMéx', 'CDMX'],
                    'semaforo': 'Rojo'}
        region_7= {'region': 'Región SurOeste',
                    'estados': ['Guerrero', 'Oaxaca', 'Chiapas'],
                    'semaforo': 'Naranja y Verde'}
        region_8= {'region': 'Región SurEste',
                    'estados': ['Tabasco', 'Campeche', 'QuintanaRoo', 'Yucatán'],
                    'semaforo': 'Naranja y Verde'}
        
        #regiones= [region_1, region_2, region_3, region_4, region_5, region_6, region_7, region_8]

        weather_dict= dict()  
        weather_dict['date']= hS['date']  
        weather_dict['states']= []      

        # Se determina la estación del año respecto al mes 
        month= hS['date'][0]

        if month < 3:
            weather_dict['season']= 'Invierno'
            weather_dict['temperature']= invierno['temperatura']
            weather_dict['climate']= invierno['clima']

        elif (month > 3) & (month < 7):
            weather_dict['season']= 'Primavera'
            weather_dict['temperature']= primavera['temperatura']
            weather_dict['climate']= primavera['clima']

        elif month > 6 & month < 10:
            weather_dict['season']= 'Verano'
            weather_dict['temperature']= verano['temperatura']
            weather_dict['climate']= verano['clima']

        elif month > 9 & month < 13:
            weather_dict['season']= 'Otoño'
            weather_dict['temperature']= otoño['temperatura']
            weather_dict['climate']= otoño['clima']

        # 
        estados= hS['states']
        R1, R2, R3, R4, R5, R6, R7, R8= ([] for i in range(8))

        # Se determina la región de la República Mexicana        
        for item in estados:
            if item in region_1['estados']:
                R1.append(item)
        if ctr(R1) == ctr(region_1['estados']):
            weather_dict['states'].append(region_1)

        for item in estados:
            if item in region_2['estados']:
                R2.append(item)
        if ctr(R2) == ctr(region_2['estados']):
            weather_dict['states'].append(region_2)

        for item in estados:
            if item in region_3['estados']:
                R3.append(item)
        if ctr(R3) == ctr(region_3['estados']):
            weather_dict['states'].append(region_3)

        for item in estados:
            if item in region_4['estados']:
                R4.append(item)
        if ctr(R4) == ctr(region_4['estados']):
            weather_dict['states'].append(region_4)

        for item in estados:
            if item in region_5['estados']:
                R5.append(item)
        if ctr(R5) == ctr(region_5['estados']):
            weather_dict['states'].append(region_5)

        for item in estados:
            if item in region_6['estados']:
                R6.append(item)
        if ctr(R6) == ctr(region_6['estados']):
            weather_dict['states'].append(region_6)

        for item in estados:
            if item in region_7['estados']:
                R7.append(item)
        if ctr(R7) == ctr(region_7['estados']):
            weather_dict['states'].append(region_7)

        for item in estados:
            if item in region_8['estados']:
                R8.append(item)
        if ctr(R8) == ctr(region_8['estados']):
            weather_dict['states'].append(region_8)

        #print(weather_dict)

        return weather_dict
        
    def pipeline(self):
        print('\nInicia módulo: Data Analysis')
        ET= self.hashtagSearch(tweetText)
        w= self.weather(ET)
        
        return w


class NarrativeGenerator:

    def generator(self, w):

        region_6= {'region': 'Región Centro Sur',
                    'estados': ['Morelos', 'EdoMéx', 'CDMX'],
                    'semaforo': 'Rojo'}
        #print(w.keys())
        # En caso de no completar ninguna región de la República Mexicana
        if w['states'] == []:
            w['states'].append(region_6)

        # Textos alternativos
        recomendaciones= ['Lávate las manos con frecuencia. Usa agua y jabón o un desinfectante de manos a base de alcohol.',
                            'Mantén una distancia de seguridad con personas que tosan o estornuden.',
                            'Utiliza mascarilla cuando no sea posible mantener el distanciamiento físico.',
                            'No te toques los ojos, la nariz ni la boca.',
                            'Cuando tosas o estornudes, cúbrete la nariz y la boca con el codo flexionado o con un pañuelo.',
                            'Si no te encuentras bien, quédate en casa.',
                            'En caso de que tengas fiebre, tos o dificultad para respirar, busca atención médica.']

        recursos= ['* Consulta el Mapa del Semáforo Epidemiológico: https://datos.covid-19.conacyt.mx/#SemaFE',
                    '* Mantente informado con las últimas noticias sobre COVID-19 en la República Mexicana en: https://coronavirus.gob.mx/']

        # Templates
        template_1= {'entrada': 'Fecha: {}-{}-{}'.format((w['date'][0]), (w['date'][1]), (w['date'][2]) ),
                    'txt_1': 'De acuerdo a reportes del SMN la {} se mantiene con semaforos {}.'.format( w['states'][0]['region'], w['states'][0]['semaforo']),
                    'txt_2': 'La presencia de {} acompañada de {}, {} y {} ocasiona complicaciones en la región.'.format(w['temperature'], w['climate'][0], w['climate'][1], w['climate'][2]),
                    'txt_3': 'Recuerda: \n~ ' + choice(recomendaciones),                                         
                    'txt_4': choice(recursos)
        }
        
        template_2= {'entrada': 'Hoy {} del mes {}, '.format((w['date'][1]), (w['date'][0])),
                    'txt_1': 'El Servicio Meteorológico Nacional señala que la {} se mantiene con semaforos {}.'.format( w['states'][0]['region'], w['states'][0]['semaforo']),
                    'txt_2': 'Mayormente se presentarán {} acompañada de {}, {} y {} así que no olvides tomar precauciones.'.format(w['temperature'], w['climate'][0], w['climate'][1], w['climate'][2]),
                    'txt_3': 'Es importante: \n~ ' + choice(recomendaciones),                                         
                    'txt_4': choice(recursos)
        }

        template_3= {'entrada': 'Este mes {} del año {}, '.format((w['date'][0]), (w['date'][2])),
                    'txt_1': 'Las condiciones sanitarias en los estados de {} se mantienen con semaforos {}.'.format( str(w['states'][0]['estados']), w['states'][0]['semaforo']),
                    'txt_2': 'Esta temporada de {} viene acompañada de {}, {} y {}, esto afectará la región {}.'.format(w['season'], w['climate'][0], w['climate'][1], w['climate'][2], w['states'][0]['region']),
                    'txt_3': 'Aquí te recomendamos: \n~ ' + choice(recomendaciones),                                         
                    'txt_4': choice(recursos)
        }

        template_4= {'entrada': 'Este {} del mes {} el SMN informa: '.format((w['date'][1]), (w['date'][0])),
                    'txt_1': 'La región de {} se mantiene con semaforos {}, aumentando el número de casos por día.'.format( w['states'][0]['region'], w['states'][0]['semaforo']),
                    'txt_2': 'Recordemos que estamos en {} y se esperan {} para los próximos días.'.format(w['season'], w['temperature']),
                    'txt_3': 'Es importante mantegas las siguientes indicaciones: \n~ ' + choice(recomendaciones)+ '\n~ ' +choice(recomendaciones),                                         
                    'txt_4': choice(recursos)
        }

        template_5= {'entrada': 'Hoy {} del mes {}: '.format((w['date'][1]), (w['date'][0])),
                    'txt_1': 'El gobierno de la República Mexicana informa que la región {} se mantiene con semaforos {}.'.format( w['states'][0]['region'], w['states'][0]['semaforo']),
                    'txt_2': 'La presencia de {} acompañada de {}, {} y {} ocasionará complicaciones en la región. Es importante que este {} tomes precauciones.'.format(w['temperature'], w['climate'][0], w['climate'][1], w['climate'][2], w['season']),
                    'txt_3': 'Aquí algunas recomendaciones sanitarias: \n~ ' + choice(recomendaciones),                                         
                    'txt_4': choice(recursos)
        }

        templates= [template_1, template_2, template_3, template_4, template_5]
        template_choice= choice(templates)

        print('\n')
        
        print(template_choice['entrada'])
        print(template_choice['txt_1'])
        print(template_choice['txt_2'])
        print(template_choice['txt_3'])
        print(template_choice['txt_4'])
        

    def pipeline(self):
        self.generator(estado_tiempo)
        
        

if __name__ == '__main__':
    
    myCrawler= TwitterCrawler()
    tweetText= myCrawler.pipeline()

    data= DataAnalysis()
    estado_tiempo= data.pipeline()

    generator= NarrativeGenerator()
    generator.pipeline()
