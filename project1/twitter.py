'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy
import json

poi_tweet_ids = {}
tweet_ids = {}

class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("RcFG1u9quKQGG8R68RmubK79n", "Rhlyi4zVFvadp98fUhJHcdZIwHBzZv8yWCCdkKsjLPouQuI6Sy")
        self.auth.set_access_token("1432461231680598022-k4xCu47h0qJu8klui9t5gLpZ1XCBFT", "5EYJmAwzNThDMejPCQso7iF1vTBWYmB4103zUeW3E2yJ4")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def _meet_basic_tweet_requirements(self):
        '''
        Add basic tweet requirements logic, like language, country, covid type etc.
        :return: boolean
        '''
        print('Basic Requirements mentioned Here>>>>>>>>>>>>>>>>>>>>>>>>>>>!');
        meet_requirements = {
            'USA': 5000,
            'Mexico': 5000,
            'India': 5000,
            'en': 5000,
            'hi': 5000,
            'es': 5000,
            'poi_covid': 50,
            'poi_gen': 500
        }
        return meet_requirements

    def get_tweets_by_poi_screen_name(self,poi):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        tweets = []
        poi_tweet_ids[poi['id']] = []
        tweet_ids[poi['id']] = []
        # max_id = 0
        # keyword_index = 0
        keywords = [  
            "quarentena",
            "hospital",
            "covidresources",
            "rt-pcr",
            "वैश्विकमहामारी",
            "oxygen",
            "सुरक्षित रहें",
            "stayhomestaysafe",
            "covid19",
            "quarantine",
            "मास्क",
            "face mask",
            "covidsecondwaveinindia",
            "flattenthecurve",
            "corona virus",
            "wuhan",
            "cierredeemergencia",
            "autoaislamiento",
            "sintomas",
            "covid positive",
            "casos",
            "कोविड मृत्यु",
            "स्वयं चुना एकांत",
            "stay safe",
            "#deltavariant",
            "covid symptoms",
            "sarscov2",
            "covidiots",
            "brote",
            "alcohol en gel",
            "disease",
            "asintomático",
            "टीकाकरण",
            "encierro",
            "covidiot",
            "covidappropriatebehaviour",
            "fever",
            "pandemia de covid-19",
            "wearamask",
            "flatten the curve",
            "oxígeno",
            "desinfectante",
            "super-spreader",
            "ventilador",
            "coronawarriors",
            "quedate en casa",
            "mascaras",
            "mascara facial",
            "trabajar desde casa",
            "संगरोध",
            "immunity",
            "स्वयं संगरोध",
            "डेल्टा संस्करण",
            "mask mandate",
            "health",
            "dogajkidoori",
            "travelban",
            "cilindro de oxígeno",
            "covid",
            "staysafe",
            "variant",
            "yomequedoencasa",
            "doctor",
            "एंटीबॉडी",
            "दूसरी लहर",
            "distancia social",
            "मुखौटा",
            "covid test",
            "अस्पताल",
            "covid deaths",
            "कोविड19",
            "muvariant",
            "susanadistancia",
            "personal protective equipment",
            "remdisivir",
            "quedateencasa",
            "asymptomatic",
            "social distancing",
            "distanciamiento social",
            "cdc",
            "transmission",
            "epidemic",
            "social distance",
            "herd immunity",
            "transmisión",
            "सैनिटाइज़र",
            "indiafightscorona",
            "surgical mask",
            "facemask",
            "desinfectar",
            "वायरस",
            "संक्रमण",
            "symptoms",
            "सामाजिक दूरी",
            "covid cases",
            "ppe",
            "sars",
            "autocuarentena",
            "प्रक्षालक",
            "breakthechain",
            "stayhomesavelives",
            "coronavirusupdates",
            "sanitize",
            "covidinquirynow",
            "कोरोना",
            "workfromhome",
            "outbreak",
            "flu",
            "sanitizer",
            "distanciamientosocial",
            "variante",
            "कोविड 19",
            "कोविड-19",
            "covid pneumonia",
            "कोविड",
            "pandemic",
            "icu",
            "वाइरस",
            "contagios",
            "वेंटिलेटर",
            "washyourhands",
            "n95",
            "stayhome",
            "lavadodemanos",
            "fauci",
            "रोग प्रतिरोधक शक्ति",
            "maskmandate",
            "डेल्टा",
            "कोविड महामारी",
            "third wave",
            "epidemia",
            "fiebre",
            "मौत",
            "travel ban",
            "फ़्लू",
            "muerte",
            "स्वच्छ",
            "washhands",
            "enfermedad",
            "contagio",
            "infección",
            "faceshield",
            "self-quarantine",
            "remdesivir",
            "oxygen cylinder",
            "mypandemicsurvivalplan",
            "कोविड के केस",
            "delta variant",
            "wuhan virus",
            "लक्षण",
            "corona",
            "maskup",
            "gocoronago",
            "death",
            "curfew",
            "socialdistance",
            "second wave",
            "máscara",
            "stayathome",
            "positive",
            "lockdown",
            "propagación en la comunidad",
            "तीसरी लहर",
            "aislamiento",
            "rtpcr",
            "coronavirus",
            "variante delta",
            "distanciasocial",
            "cubrebocas",
            "घर पर रहें",
            "socialdistancing",
            "covidwarriors",
            "प्रकोप",
            "covid-19",
            "stay home",
            "संक्रमित",
            "jantacurfew",
            "cowin",
            "कोरोनावाइरस",
            "virus",
            "distanciamiento",
            "cuarentena",
            "indiafightscovid19",
            "healthcare",
            "natocorona",
            "मास्क पहनें",
            "delta",
            "ऑक्सीजन",
            "wearmask",
            "कोरोनावायरस",
            "ventilator",
            "pneumonia",
            "maskupindia",
            "ppe kit",
            "sars-cov-2",
            "testing",
            "fightagainstcovid19",
            "महामारी",
            "नियंत्रण क्षेत्र",
            "who",
            "mask",
            "pandemia",
            "deltavariant",
            "वैश्विक महामारी",
            "रोग",
            "síntomas",
            "work from home",
            "antibodies",
            "masks",
            "confinamiento",
            "flattening the curve",
            "मुखौटा जनादेश",
            "thirdwave",
            "mascarilla",
            "usacubrebocas",
            "covidemergency",
            "inmunidad",
            "cierre de emergencia",
            "self-isolation",
            "स्वास्थ्य सेवा",
            "सोशल डिस्टन्सिंग",
            "isolation",
            "cases",
            "community spread",
            "unite2fightcorona",
            "oxygencrisis",
            "containment zones",
            "homequarantine",
            "स्पर्शोन्मुख",
            "लॉकडाउन",
            "hospitalización",
            "incubation period",
            "anticuerpos",
            "vaccine mandate",
            "eficacia de la vacuna",
            "vacuna covid",
            "covidvaccine",
            "zycov-d",
            "vaccines",
            "#largestvaccinedrive",
            "vaccination",
            "dosis de vacuna",
            "moderna",
            "campaña de vacunación",
            "vaccineshortage",
            "vacunar",
            "covid vaccine",
            "efectos secundarios de la vacuna",
            "कोविशील्ड",
            "hydroxychloroquine",
            "efficacy",
            "टीके",
            "टीकाकरण",
            "वैक्सीनेशन",
            "shots",
            "covishield",
            "vaccine",
            "antibody",
            "j&j vaccine",
            "booster shot",
            "वैक्सीन पासपोर्ट",
            "covidvaccination",
            "दूसरी खुराक",
            "inyección de refuerzo",
            "astrazeneca",
            "टीकाकरण अभियान",
            "vacunacovid19",
            "johnson & johnson",
            "पहली खुराक",
            "sinopharm",
            "immunity",
            "vaccination drive",
            "inmunización",
            "vaccine dose",
            "we4vaccine",
            "पूर्ण टीकाकरण",
            "vaccine passports",
            "एंटीबॉडी",
            "vacunado",
            "vacunarse",
            "johnson",
            "efecto secundario",
            "astra zeneca",
            "yomevacunoseguro",
            "injection",
            "cdc",
            "वैक्सीन के साइड इफेक्ट",
            "getvaxxed",
            "teeka",
            "टीका",
            "herd immunity",
            "वैक्सीन जनादेश",
            "vaccinepassports",
            "estrategiadevacunación",
            "ivermectin",
            "cansino",
            "vacunas",
            "vaccinehesitancy",
            "sputnik",
            "johnson & johnson’s janssen",
            "unvaccinated",
            "janssen",
            "sputnik v",
            "vacunaton",
            "seconddose",
            "कोवेक्सिन",
            "getvaccinatednow",
            "tikakaran",
            "कोविशिल्ड",
            "खुराक",
            "covaxine",
            "mrna",
            "first dose",
            "वाइरस",
            "booster shots",
            "dosis",
            "side effect",
            "रोग प्रतिरोधक शक्ति",
            "jab",
            "get vaccinated",
            "vaccinessavelives",
            "pinchazo",
            "vaccinesideeffects",
            "vaccinated",
            "कोविड का टीका",
            "खराब असर",
            "vacunación",
            "कोवैक्सिन",
            "tikautsav",
            "efectos secundarios",
            "remdesivir",
            "covid19vaccine",
            "eficacia",
            "anticuerpo",
            "vaccinequity",
            "vaccinesamvaad",
            "फाइजर",
            "vaccinesamvad",
            "covid-19 vaccine",
            "pasaporte de vacuna",
            "largestvaccinationdrive",
            "firstdose",
            "doses",
            "vacuna",
            "la inmunidad de grupo",
            "कोवैक्सीन",
            "vaccine side effects",
            "कोविन",
            "vaccinationdrive",
            "clinical trial",
            "vaccinemandate",
            "segunda dosis",
            "cowin",
            "vaccinate",
            "clinical trials",
            "fully vaccinated",
            "johnson and johnson",
            "primera dosis",
            "largestvaccinedrive",
            "vaccine hesitancy",
            "वैक्सीन",
            "प्रभाव",
            "vacunacion",
            "second dose",
            "sabkovaccinemuftvaccine",
            "लसीकरण",
            "vaccineswork",
            "वैक्‍सीन",
            "दुष्प्रभाव",
            "pfizer",
            "vaccine efficacy",
            "टीका लगवाएं",
            "एमआरएनए वैक्सीन",
            "antibodies",
            "getvaccinated",
            "covidshield",
            "booster",
            "टीका_जीत_का",
            "vaccine jab",
            "vaccine passport",
            "vaccinepassport",
            "mrna vaccine",
            "inmunidad",
            "एस्ट्राजेनेका",
            "mandato de vacuna",
            "astrazenca",
            "vacúnate",
            "vacuna para el covid-19",
            "vacunada",
            "side effects",
            "dose",
            "novavax",
            "j&j",
            "covaxin",
            "fullyvaccinated",
            "sputnikv",
            "कोविड टीका",
            "completamente vacunado",
            "novaccinepassports",
            "sinovac"  
        ]
        loop = 0;
                   
        while  len(tweet_ids[poi['id']]) < 500 or len(poi_tweet_ids[poi['id']]) < 50:
            loop = loop +1;
            print(len(tweet_ids[poi['id']]) < 500 or len(poi_tweet_ids[poi['id']]) < 50)
            print("Let's go>>>>>>>")
            print('remaining>>'+poi['screen_name'])
            print(500 - len(tweet_ids[poi['id']]))
            print(len(tweet_ids[poi['id']]))
            print('keyword tweets remaining>>')
            print(50 - len(poi_tweet_ids[poi['id']]))
  
            for data in tweepy.Cursor(self.api.user_timeline, screen_name = poi['screen_name'], count = poi['count'], tweet_mode='extended', include_rts=False).items(poi['count']):
                if data._json['id'] not in poi_tweet_ids[poi['id']] and any(keyword in data._json['full_text'] for keyword in keywords) and len(poi_tweet_ids[poi['id']]) < 50:
                    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<NEW>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>');
                    matching = [keyword for keyword in keywords if keyword in data._json['full_text']]
                    print(matching)

                    print('tweet added')
                    tweets.append(data)
                    data._json['full_text']
                    if poi['id'] not in poi_tweet_ids[poi['id']]:
                        poi_tweet_ids[poi['id']].append(data._json['id'])
                        tweet_ids[poi['id']].append(data._json['id'])
                        # max_id = data._json['id']

                elif data._json['id'] not in tweet_ids and len(tweet_ids[poi['id']]) < 1000:    
                        tweets.append(data)
                        tweet_ids[poi['id']].append(data._json['id'])

            if(len(poi_tweet_ids[poi['id']]) < 50 or loop >= 10):
                    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< NOT COLLECTED ENOUGH KEYWORD TWEETS FOR '+poi['screen_name'])
                    print(len(poi_tweet_ids[poi['id']]))
                    break;
        print('done')
        print('Total tweets collected>>>>')
        print(len(tweet_ids[poi['id']]))
        print('Total KEYWORD tweets collected>>>>')
        print(len(poi_tweet_ids[poi['id']]))

        return tweets;

    def get_tweets_by_lang_and_keyword(self,keywords):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        tweets = []
        print('keyword')
        print(keywords['name'])
        for data in tweepy.Cursor(self.api.search,q = keywords['name']+ "-filter:retweets",lang = keywords['lang'],count = keywords['count'],tweet_mode='extended').items(keywords['count']):
            tweets.append(data)
 
        return tweets        

    def get_replies(self,tweet_id,poi):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        replies=[]
        for tweet in tweepy.Cursor(self.api.search,q='to:'+poi, result_type='recent', ).items(1000):
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if (tweet.in_reply_to_status_id_str==tweet_id):
                    replies.append(tweet)
        
        return replies
