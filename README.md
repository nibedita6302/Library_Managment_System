# Library_Managment_System
This is a Linux based application for Online Library System including both User and Librarian functionalities. 

> [!IMPORTANT]
> - Major tools used: Python Flask, SQLite, VueJS, Redis and Celery. Make sure to have all the above installed before running the application. 
> - Also read [Project Report,pdf](https://github.com/nibedita6302/Library_Managment_System/blob/main/Project%20Report.pdf) for detailed insight into dataflow and database structure. Click the link in pdf to Watch video explanation.

## Tech Stack
||**Backend**| <img alt="Static Badge" src="https://img.shields.io/badge/Python-blue?style=plastic&logo=python&logoColor=yellow" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/SQLite_3-brightgreen?style=plastic&logo=sqlite&logoColor=white" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/SQLAlchemy-%23eb3a1f?style=plastic&logo=SQLAlchemy&logoColor=black" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/Flask-white?style=plastic&logo=flask&logoColor=black" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/Flask_Security_too-black?style=plastic&logo=flask&logoColor=white" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/Redis-red?style=plastic&logo=redis&logoColor=white" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/REST_API-%23f4f8af?style=plastic&logo=academia&logoColor=purple" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/Celery-brightgreen?style=plastic&logo=celery&logoColor=black" height="25"> ||
|------|:-------:|:-----------------------------------------------------------------------------------------------------------------------:|-----|
||**Frontend**| <img alt="Static Badge" src="https://img.shields.io/badge/NPM-magenta?style=plastic&logo=npm&logoColor=white" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/Javascript-yellow?style=plastic&logo=Javascript&logoColor=black" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/HTML5-orange?style=plastic&logo=HTML5&logoColor=white" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/VueJS-grey?style=plastic&logo=vue.js&logoColor=green" height="25"> ||
||**Tools**| <img alt="Static Badge" src="https://img.shields.io/badge/Git-%23ae1710?style=plastic&logo=git&logoColor=white" height="25"> <img alt="Static Badge" src="https://img.shields.io/badge/Postman-white?style=plastic&logo=postman&logoColor=red" height="25"> ||
||**Operating System**|<img alt="Static Badge" src="https://img.shields.io/badge/Linux-purple?style=plastic&logo=linux&logoColor=black" height="25"> ||

## README 

Open Linux terminal. Make sure to have __python3__ and __pip3__ installed. Follow the following command to 
start the Online Grocery Store application.

#### ------ TERMINAL 1 ------
```
$ bash local_setup.sh  ## creates environment and installs requirements 
$ bash local_run.sh		## runs main.py
```

#### ------ TERMINAL 2 ------
``` 
$ redis-server  # start redis server
```

#### ------ TERMINAL 3 ------
``` 
$ bash local_workers.sh  # start celery worker
```

#### ------ TERMINAL 4 ------
``` 
$ bash local_beat.sh  # start celery worker
```

#### ------ TERMINAL 5 ------
```
$ cd frontend/
$ npm run serve  # start vue.js server
```
> [!TIP]
> - Take a look at _Project Report.pdf_ for more details on methodology and tech stack.
> - Open url *http://localhost:8080/* for Home page and explore! 
---------------------------------------------------
> [!IMPORTANT]
>There is only One Admin allowed in the application with following credentials
>- Admin Login Credentials:
>- Email: Setup your own email
>- Password: Setup your own password 

> [!NOTE]
> *For new User register with actual working email, to use the full potential of the application.*

