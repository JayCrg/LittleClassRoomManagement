# LittleClassRoomManagement
## Application developed in Python using the PySimpleGUI library with the purpose of manage a high school  

In this little project we'll treat a little data base, based on the following structure  
![image](https://user-images.githubusercontent.com/97992506/203162431-3708f4a1-f013-453c-9d1d-6e624a99ea82.png)  

We'll be able to look up the registered students  
![image](https://user-images.githubusercontent.com/97992506/203162847-6baf9d0d-f111-4d45-a229-226f1e135e57.png)

As well as insert new ones  
![image](https://user-images.githubusercontent.com/97992506/203162885-9c2807a0-5b24-4e60-8e34-7e382aad3924.png)  

Or import the data from a text file  
![image](https://user-images.githubusercontent.com/97992506/203163021-2309ac7d-fec4-4883-b708-0770bc8c9a3a.png)  

We can also insert new teachers and subjects, but no options to look for them have been added yet  
![image](https://user-images.githubusercontent.com/97992506/203163409-67bec2c9-bb9f-4f77-9388-bc901d233bdb.png)

DataBase controllers can be messy, specially the YearDBController. This is due to the lack of functionality the 
rest of the classes have, making the year (which is already who creates all the other objects) the main class and
center of all.
In case that more functionality is added to the rest of the classes (for example, charging the information for only
1 teacher it should be added in it respective class and DB controller
