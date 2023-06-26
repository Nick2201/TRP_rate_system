# TRP_rate_system

### JupyterNotebook по [ссылке](https://github.com/Nick2201/TRP_rate_system/blob/main/TRP_rate_system/src/data_show.ipynb)

## Tasks

### Task 1
- [x] Задача          : понять, выполняется ли в каждой кампании плановый объём TRP ,где перевыполнение на одном канале **может** компенсировать недовыполнение на другом
      Ответ           : исходя из данных да, исходя из предложенной клиентом системой рейтинга можно присудить значение 6
      Имя переменной  : general_rating
### Task 2     
![image](https://github.com/Nick2201/TRP_rate_system/assets/71185932/1d4cf376-e2f7-4037-88f8-377327d621cc)

- [x] Задача          : понять, выполняется ли в каждой кампании плановый объём TRP , перевыполнение по одной кампании **не может** компенсировать перевыполнение по другой
      Ответ           : см.вложение ниже
      Имя переменной  : rating_analog   
![image](https://github.com/Nick2201/TRP_rate_system/assets/71185932/c4919996-a43d-409d-800c-af0e3785adda)

### Task 3  
-  Еще один вариант как компании можно соотнести друг к другу
- [x] Задача          : На основе чего еще могут быт присвоены рейтинги
      Ответ           : .quantile(0.1) .quantile(0.9)
      Имя переменной  : rating_each_company
         
![image](https://github.com/Nick2201/TRP_rate_system/assets/71185932/bd8a981a-bd87-42b9-b7f5-4e6d90b39008)

### Гистограмма по аудитории накаждом из каналов
![5ea81cf1-9e82-4900-a2fc-0d1aaa07a12c](https://github.com/Nick2201/TRP_rate_system/assets/71185932/45fe6149-075f-4c5c-8984-be85b07369bb)

### График целевой аудитории по месяцам

![image](https://github.com/Nick2201/TRP_rate_system/assets/71185932/62590536-09fd-405a-9b5f-e6dbc5907337)


