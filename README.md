# Sabin-Porofolio
Details of personal and professional projects

## Personal Projects

### Website
* Code in branch: cicc_website

Developed a simple website (for civil engineering consultant) based on Django with use of Wagtail CMS. 

### Logistic Management System
* Code in branch: logistic

A web application based on Django where a vendor can place his/her parcel to get it delivered and the admin will assign rider to deliver the parcel and rider gets it delivered to the customer. 

### Attendance management System
* Code in branch: attendance

The attendance management system is web application based on Django. The system is based on facial data of employee.
The application uses face-recognition library for the identification of the employee and with identification customer is given for checkin and checkout.


### Video Broadcast Platform
* Code in branch broadcast
This is and web application based on Django. Here the admin uploads videos on various channels.
Users are able to subscribe to the channel and watch videos of subscribed channel.


### Machine Learning Practice
* Code in branch machinelearning
Here is the implementation basic machine learning to detect spammail and fake news.


### Restaurant Ordering System
* Code in branch restautant
This is backend api for restaurant ordering management system based on Django Rest Framework. APIs required for restaurant ordering system such as
      - item creation, update, list, delete
      - table creation, update, list, delete
      - order creation
are developed. This application is yet to be completed.


## Official Projects

### Online KYC System
  This is an online KYC and visitor log management system. Customer details with their facial and biometric data are saved in the system on next visit, they are identified from their facial and biometric data. This application is based on Django Rest Framework.

### Log Management System
  This is Django based application which includes the implemantation of Elasticsearch, RabbitMQ and Logstash. Logs from an existing database are transfered to the elasticsearch with the help of logstash. And for new data, api is developed to send data to RabbitMQ server (thus made asynchronous) and then as RabbitMQ gets data it pushes the data to elasticsearch database.
 
### Data Extraction Application
   This is django rest framework based application which implements azure cognitive services. With the help of azure cognitive services data is extracted from ID cards and then supplied as response to the request.
