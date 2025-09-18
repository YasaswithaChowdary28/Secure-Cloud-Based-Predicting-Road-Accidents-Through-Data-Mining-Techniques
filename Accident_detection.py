"""
Accident Detection Django Views

This module contains Django view functions for an accident detection system.
It includes functionality for:
- Service provider login
- Road accident positioning analysis
- Data visualization with charts
- Machine learning model training and testing
- Data export functionality

Note: This file requires proper Django model imports to function correctly.
The models (ClientRegister_Model, RoadAccidents_prediction, detection_ratio, 
detection_accuracy) need to be imported from the appropriate Django app.
"""

from django.db.models import Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse
import xlwt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn import svm

# Create your views here.
# Note: The following models need to be imported from your Django app:
# from Remote_User.models import ClientRegister_Model, RoadAccidents_prediction, detection_ratio, detection_accuracy
def serviceproviderlogin(request):
    if request.method == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password == "Admin":
            return redirect('View_Remote_Users')
    return render(request, 'SProvider/serviceproviderlogin.html')


def View_RoadAccidents_Positioning_Type(request):
    obj = RoadAccidents_prediction.objects.all()
    return render(request, 'SProvider/View_RoadAccidents_Positioning_Type.html', {'objs': obj})


def View_RoadAccidents_Positioning_Type_Ratio(request):
    detection_ratio.objects.all().delete()
    
    # Calculate ratio for 'In Position'
    ratio = ""
    kword = 'In Position'
    print(kword)
    obj = RoadAccidents_prediction.objects.all().filter(Prediction=kword)
    obj1 = RoadAccidents_prediction.objects.all()
    count = obj.count()
    count1 = obj1.count()
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio.objects.create(names=kword, ratio=ratio)
    
    # Calculate ratio for 'Not In Position'
    ratio1 = ""
    kword1 = 'Not In Position'
    print(kword1)
    obj1 = RoadAccidents_prediction.objects.all().filter(Prediction=kword1)
    obj11 = RoadAccidents_prediction.objects.all()
    count1 = obj1.count()
    count11 = obj11.count()
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio.objects.create(names=kword1, ratio=ratio1)
    
    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/View_RoadAccidents_Positioning_Type_Ratio.html', {'objs': obj})


def View_Remote_Users(request):
    obj = ClientRegister_Model.objects.all()
    return render(request, 'SProvider/View_Remote_Users.html', {'objects': obj})


def charts(request, chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/charts.html", {'form': chart1, 'chart_type': chart_type})


def charts1(request, chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/charts1.html", {'form': chart1, 'chart_type': chart_type})


def likeschart(request, like_chart):
    charts = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/likeschart.html", {'form': charts, 'like_chart': like_chart})


def likeschart1(request, like_chart):
    charts = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/likeschart1.html", {'form': charts, 'like_chart': like_chart})


def Download_Trained_DataSets(request):
    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Predicted_Datasets.xls"'
    
    # creating workbook
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    
    # writer = csv.writer(response)
    obj = RoadAccidents_prediction.objects.all()
    
    # Note: This function appears incomplete - missing Excel writing logic
    return response


def Train_Test_DataSets(request):
    detection_accuracy.objects.all().delete()
    df = pd.read_csv('Datasets.csv')
    
    def apply_results(label):
        if (label == 0):
            return 0  # In Positioning
        elif (label == 1):
            return 1  # Not In Positioning
    
    df['results'] = df['Label'].apply(apply_results)
    cv = CountVectorizer(lowercase=False)
    X = df["Fid"].apply(str)
    y = df['results']
    
    print("X Values")
    print(X)
    print("Labels")
    print(y)
    
    X = cv.fit_transform(X)
    models = []
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    print("X_train shape:", X_train.shape, "X_test shape:", X_test.shape, "y_train shape:", y_train.shape)
    print("X_test")
    print(X_test)
    print("X_train")
    print(X_train)
    
    # SVM Model
    print("SVM")
    lin_clf = svm.LinearSVC()
    lin_clf.fit(X_train, y_train)
    predict_svm = lin_clf.predict(X_test)
    svm_acc = accuracy_score(y_test, predict_svm) * 100
    print("SVM Accuracy:", svm_acc)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, predict_svm))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, predict_svm))
    models.append(('svm', lin_clf))
    detection_accuracy.objects.create(names="SVM", ratio=svm_acc)
    
    return render(request, 'SProvider/Train_Test_DataSets.html')