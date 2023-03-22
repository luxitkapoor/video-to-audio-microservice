
# Video to Audio Converter Microservice

This project consists of a basic Microservice architecture application that converts a given video file to audio.


## Installation

### Dependencies

For this application, the following dependencies are required
- Docker
- Minikube

### Running the microservice

Each part of the microservice consits of its on yaml deployment files that need to be deployed individually to bring up the respective service.

First and foremost, after starting docker run the following command for starting a minikube local cluster.

```shell
    minikube start
```
Next step is to enable ingress in Minikube

```shell
    minikube addons enable ingress
    minikube addons list

```
After enabling ingress you should see a green check mark next to ingress in the minikube addons list.

Next thing we need to do is to route the traffic on localhost to the minikube ingress we just enabled by adding the following configurations to the /etc/hosts 

```shell
    sudo vim /etc/hosts
```
Now in the hosts file add the following lines

```
    127.0.0.1       mp3converter.com
    127.0.0.1       rabbitmq-manager.com

```
This would allow us to send the curl requests to mp3converter.com and also allow us to use the rabbitmq-manager gui to manage our queues.

Next step is to log in to the rabbitmq-manager.com using credentials guest/guest and go to the queue sections and create 2 durable queues namely 
- video
- mp3 

After creating the queues we are ready to start bringing up the pods.

For bringing up the pods with the service, all that you have to do is to cd into the manifests directory in each service and run the following command

```shell
    kubectl apply -f ./
```

This would apply all the yaml files and create the respective resources necessary.
To delete the created resources, you can run

```shell
    kubectl delete -f ./
```

The first service that should be created is the mysql service.
Once the service is up and running exec into the mysql pod and run the following commands to create the initial database. The template for initializing the database can be found at ../auth/init.sql

```sql
    mysql -uroot -p
```
After this enter the default password which is defined in the ../mysql/manifests/mysql-deployment.yaml . The default value for this is password
Next run the following sql statements to initialize the db.

```sql


    CREATE USER 'auth_user'@'%' IDENTIFIED BY 'Auth123';

    CREATE DATABASE auth;

    GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'%';

    USE auth;

    CREATE TABLE user (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );

    INSERT INTO user (email,password) VALUES (<email>, <password>);
```

If you are changing the user password for the database, also make sure to update the secrets in ../auth/manifests/secret.yaml 

Also keep in mind the email and the password that you are inserting into the database as this would be used to send the curl requests to the service.

Now you can start bringing up the other services by first bringing up the mongodb and the rabbitmq services followed by the other services.


## Demo

To send requests to the service, you first need to send a curl request to the 
login endpoint using the following curl request. In the response you would recieve a JWT that would be used for making the following requests.

```shell
    curl -X POST http://mp3converter.com/login -u <email>:<password>
```

Here again the email and password combo should be the same as the one we inserted into the table.
Once you recieve a JWT, we can make requests to the upload endpoint using the JWT token and the video file to be converted.

```shell
    curl -X POST -F '<file_name>' -H 'Authorization: Bearer <JWT Token recieved from the login endpoint>' http://mp3converter.com/upload
```

At the time of writing this, the notification service is not up and running so to get the converted audio file, you would have to check for the file id in the mongodb and then make a request to the download endpoint.


## Roadmap

- Simplifying the download process till the notification service is complete

- Completing the notification service

- Adding a signup option in the auth service

