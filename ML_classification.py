import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB,GaussianNB,BernoulliNB,ComplementNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestCentroid
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
import pickle
from collections import defaultdict


#categories = ['0','אזרחות, תושבות וכניסה לישראל','בחירות','ביטחון','ביטחון הפנים','בינוי ושיכון','בנקאות וכספים', 'בריאות','8', 'דתות','הגנת הסביבה','חוץ' , 'חוקי הסדרים', 'חוק-יסוד' ,'חינוך','חקלאות','כנסת','מדע', 'מועדים',
#                    'מיסוי','מסחר ותעשייה', 'מעמד אישי', 'מקצועות הבריאות', 'מקרקעין' , 'משפט אזרחי' ,  'משפט מינהלי' , 'משפט פלילי'  , 'ניהול נכסים', 'ספורט', 'ספנות', 'ערכות שיפוטיות' , 'פיתוח והשקעות' , 'פנסיה, ביטוח ושוק ההון',
#                    'צרכנות','קליטת עלייה','ראיות וסדרי דין','ראשי המדינה','רווחה','רשויות מקומיות','שירות הציבור' ,'תאגידים' , 'תחבורה ובטיחות בדרכים' , 'תיירות', 'תכנון ובנייה','תעופה','תעסוקה','תקציב', '47', 'תקשורת','תרבות',
#                    'תשתיות','מילווה למדינה','טכנולוגיה וסייבר' ]
categories = range(0,52)
print('getting files')
file_names = os.listdir('./Israel_Law_post_parse/')
file_names = ['./Israel_Law_post_parse/' + name for name in file_names]
print('reading csv')
df = pd.read_csv('./file.csv')
print('filtering ids not in csv')
df = df[~df.id.isin(file_names)]
df_toxic = df.drop(['id'], axis=1)
print(df_toxic)
counts=[]


#number of laws per category
categories = list(df_toxic.columns.values)
for i in categories:
    counts.append((i,df_toxic[i].sum()))
df_stats=pd.DataFrame(counts,columns=['category','number_of_laws'])
print(df_stats)

df_stats.plot(x='category', y='number_of_laws', kind='bar', legend=False, grid=True, figsize=(8, 5))
plt.title("Number of laws per category")
plt.ylabel('# of Occurrences', fontsize=12)
plt.xlabel('category', fontsize=12)
plt.show()


#number of laws with multiple categories
rowsums = df.iloc[:,2:].sum(axis=1)
x=rowsums.value_counts()

#plot
plt.figure(figsize=(8,5))
ax = sns.barplot(x.index, x.values)
plt.title("number of laws with Multiple categories")
plt.ylabel('# of Occurrences', fontsize=12)
plt.xlabel('# of categories', fontsize=12)
plt.show()


with open('heb_stopwords.txt', 'r',encoding='utf-8') as f:
    heb_stopwords = f.readlines()
    heb_stopwords = [x.strip() for x in heb_stopwords]

txts = []
for file_ in file_names:
    with open(file_, 'r', encoding='utf-8') as f:
        txt = f.readlines()
        txt = [x.strip() for x in txt]
        txt = ' '.join(txt)
        txts.append(txt)



PATH_classifier = "classifiers\\"

if os.listdir('./classifiers/').__len__() != 53:

    print('splitting data')
    x_train, x_test, y_train, y_test = train_test_split(txts, df, random_state=42, test_size=0.1, shuffle=True)

    #print(x_train.shape)
    #print(x_test.shape)
    print(y_train.shape)
    print(y_test.shape)
    print('creating pipeline')
    # Define a pipeline combining a text feature extractor with multi lable classifier
    NB_pipeline = Pipeline([
                    ('tfidf', TfidfVectorizer(stop_words=heb_stopwords)),
                    #('clf', OneVsRestClassifier(RandomForestClassifier(n_estimators=10)    #this is shit
                    ('clf', OneVsRestClassifier(MultinomialNB(alpha=.001,fit_prior=True, class_prior=None) #this is best
                    #('clf', OneVsRestClassifier((GaussianNB() )     # not working , requeires dense data
                    #('clf', OneVsRestClassifier(BernoulliNB(alpha=.5, fit_prior=True, class_prior=None)  # this is meh
                    #('clf', OneVsRestClassifier(ComplementNB(alpha=.005,fit_prior=True, class_prior=None) #this is good
                    #('clf', OneVsRestClassifier(NearestCentroid() #not working
                    #('clf', OneVsRestClassifier(SGDClassifier(alpha=.0001, max_iter=50, penalty="elasticnet") #this is good
                    #('clf', OneVsRestClassifier(LinearSVC( dual=False,tol=1e-3)   # meh

                                    )),
                ])

    cur_file='Israel_Law_post_parse\\law_2144696.txt'
    cur_file2= 'Israel_Law_post_parse\\law_2000020.txt'


    with open(cur_file, 'r', encoding='utf-8') as f:
        txt = f.readlines()
        txt = [x.strip() for x in txt]
        txt = ' '.join(txt)

    with open(cur_file2, 'r', encoding='utf-8') as f:
        txt2 = f.readlines()
        txt2 = [x.strip() for x in txt2]
        txt2 = ' '.join(txt2)

    classifiers = [0]*53;


    for i,category in enumerate(categories):
        #if category == '0' :
        #    continue
        print('processing {}'.format(category))
        NB_pipeline.fit(x_train,y_train[category])
        prediction = NB_pipeline.predict(x_test)
        pickle.dump(NB_pipeline,open(PATH_classifier + "classifier_{}".format(category),'wb'))
        print('Test Accuracy is {}'.format(accuracy_score(y_test[category].values,prediction)))
        print('Test Accuracy is {}'.format(confusion_matrix(y_test[category].values, prediction)))
        if(NB_pipeline.predict([txt])):
            print("--------------------------yoav , file law_2144696 was found to be in category {}".format(category))
        if(NB_pipeline.predict([txt2])):
            print("----------------------------yoav , file law_2000020 was found to be in category {}".format(category))

# runs a complete prediction for a file,
# it does it for all files in 'path' ,
# for each file , it loads a classifier , runs it on the specific file , then switches classifier and continues to the next file.
def complete_prediction_for_file():
    path='./Bill_document_txt/'
    aaurica_counter=0;
    fail_counter =0 ;
    predicted=0



    dictionary = defaultdict()


    for cur_file in os.listdir(path) :
    #cur_file='./bill_test.txt'
        predict=False;

        bill_id=cur_file[5:-4]
        dictionary[bill_id] = [0]*53


        with open(path+cur_file, 'r', encoding='utf-8') as f:

            txt3 = f.readlines()
            txt3 = [x.strip() for x in txt3]
            txt3 = ' '.join(txt3)
        for i,category in enumerate(categories):
            prediction = pickle.load(open(PATH_classifier+"classifier_{}".format(category),'rb')).predict([txt3])
            if prediction[0]==1:
                predict=True
                #classified_list.append(i);
                #classified_list[i]=1
                dictionary[bill_id][i]= 1


        if( predict):
            print("--------aaurica--------- rule {} classified with {}".format(cur_file, dictionary[bill_id]))
        else:
            print("fail")


def write_to_csv(dictionary):
    new_column_names = ['0', 'אזרחות, תושבות וכניסה לישראל', 'בחירות', 'ביטחון', 'ביטחון הפנים', 'בינוי ושיכון',
                        'בנקאות וכספים', 'בריאות', '8', 'דתות', 'הגנת הסביבה', 'חוץ', 'חוקי הסדרים', 'חוק-יסוד',
                        'חינוך', 'חקלאות', 'כנסת', 'מדע', 'מועדים',
                        'מיסוי', 'מסחר ותעשייה', 'מעמד אישי', 'מקצועות הבריאות', 'מקרקעין', 'משפט אזרחי', 'משפט מינהלי',
                        'משפט פלילי', 'ניהול נכסים', 'ספורט', 'ספנות', 'ערכות שיפוטיות', 'פיתוח והשקעות',
                        'פנסיה, ביטוח ושוק ההון',
                        'צרכנות', 'קליטת עלייה', 'ראיות וסדרי דין', 'ראשי המדינה', 'רווחה', 'רשויות מקומיות',
                        'שירות הציבור', 'תאגידים', 'תחבורה ובטיחות בדרכים', 'תיירות', 'תכנון ובנייה', 'תעופה', 'תעסוקה',
                        'תקציב', '47', 'תקשורת', 'תרבות',
                        'תשתיות', 'מילווה למדינה', 'טכנולוגיה וסייבר']


    df1 = pd.DataFrame(dictionary).transpose().to_csv('bill_with_categories.csv', header=new_column_names)
    with open('bill_with_categories.csv', 'r', encoding='utf-8') as original:
        data = original.read()  # pandas is doing something wierd and adds comma at the start if the csv , we want the first column to also have the header = id
    with open('bill_with_categories.csv', 'w', encoding='utf-8') as modified:
        modified.write("bill_id" + data)  # so we add it here manually

#  loads a classifier with pickle, runs it for all files, then proceeds to the next classifier.
def complete_prediction_for_classifier():
    path = './Bill_document_txt/'
    dictionary=defaultdict()
    for i,category in enumerate(categories):
        print("currently working on {}".format(category))
        cur_classifier=pickle.load(open(PATH_classifier + "classifier_{}".format(category), 'rb'))
        for cur_file in os.listdir(path):
            bill_id = cur_file[5:-4]
            if(i==0):
                dictionary[bill_id] = [0] * 53
            with open(path + cur_file, 'r', encoding='utf-8') as f:
                txt3 = f.readlines()
                txt3 = [x.strip() for x in txt3]
                txt3 = ' '.join(txt3)
            prediction = cur_classifier.predict([txt3])
            dictionary[bill_id][i]=prediction[0]
            #print(bill_id)

    write_to_csv(dictionary)






complete_prediction_for_classifier()


#print('fitting data')
# train the model using X_dtm & y
#NB_pipeline.fit(x_train, y_train[categories].values)
# compute the testing accuracy
#print('predicting')
#print(x_train[2], y_train[categories].values[2])
#print('hello')
#test_prediction = NB_pipeline.predict(x_test)
#train_prediction = NB_pipeline.predict(x_train)
#print(test_prediction[0])
#print('Train accuracy is {}'.format(accuracy_score(y_train[categories].values, train_prediction)))
#print('Test accuracy is {}'.format(accuracy_score(y_test[categories].values, test_prediction)))
