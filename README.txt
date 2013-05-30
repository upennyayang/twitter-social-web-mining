CIS630 Project TwitterAffect
Copyright (c) 2013 by - Tao Feng, Yayang Tian, Chun Chen

--------------------------------------------------------------------
Introduction

A fine-grained classifier that determines people’s sentiment on Twitter.
http://twitteraffect.co.nf

-------------------------------------------------------- ------------
File Organization

crawler folder: It contains code that used to crawl data from tweeter.
You can read the readme inside the crawler folder in order to use the crawler

web-application folder: It is used to run the sample website. You can read the readme inside

data folder: It contains the training data and testing data set. Also, contains the training data and testing data processed by birdy.

machine-learning folder: It contains two sub-folders, preprocessing and generally classifier

There are many pre-trained models inside the classifier folder, you can use it directly
Liblinear and libsvm are also included.

-------------------------------------------------------------------
Installation

(1)Install httplib2	   $ sudo python setup.py install
(2)Install oath2	   $ sudo python setup.py install
(3)Install Django          $ sudo pip install Django

--------------------------------------------------------------------
Usage

(1)Create a site 	        $ django-admin.py startproject twitteraffect
(2)Run server                   $ python manage.py runserver
(3)See effect in browser        http://127.0.0.1:8000
	
--------------------------------------------------------------------
Reference

(1)How to use httplib2		 http://code.google.com/p/httplib2/wiki/Examples
(2)How to use oauth2		 https://github.com/simplegeo/python-oauth2
(3)How to use Django	         https://docs.djangoproject.com/en/1.5/intro/tutorial01/






