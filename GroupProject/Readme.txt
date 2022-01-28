 Coding Bootcamp - Assignment 
-Title:  Assignment GroupProject Python
-Last name : Pantelakis
-First Name: Ioannis
-Team: Dikas Giorgos - Nikolaou Ioannis - Patralis Athanasios - Pantelakis Ioannis - Sakapetis Andreas
-Advisors: Tyrovola Sarantia, Nikolaos Avgeros
-Python ver:3.9.2
-win: win10 64bit

-Info:   This package is about a django project.

-Manual: You can access the pages by running the server. To do so, find the path (...\Group_Project\env\GroupProject) right after you activate the V.E.
	 Then run "python manage.py runserver". Finally, copy this link to your browser:
	 http://127.0.0.1:8000/pcp/home/ 

	 If you want to procceed to payment, you can press the Checkout button from the cart, then fill your personal info and shipping information.
	 After that press the Continue Button and choose the Paypal method. To make a payment please feel free to use the following Sandbox Account 
	 created from my paypal account for making transactions without real money.
	 SandboxAccount(Use in Paypal login) : Email: Gpuser@hotmail.com   , Password: Groupproject.
	 
	 If you need to connect as admin you can create a new superuser or use an existing one with credentials:
	 Username: admin , Password: admin

	 Every already existing customer account has the following password: Groupproject


-Notes:  
	 
	-For the rest Api it has been created an internal circle of Api. Only admin can have access by typing in browser:
	 http://127.0.0.1:8000/pcp/login_api/  . This 'api login' page works only for admin. Any other role will be redirected home after trying to 
	 log in. After admin's log in he will be redirected to http://127.0.0.1:8000/pcp/api/ where he is able to see info about customers in a table
	 that parse data from an api. Only customer's endpoint is being revealed.
	 RestApi has been constructed for local use. We are going to construct automatic procedure for cookie, as future upgrade.
	 Because of this, if you want to test the api via the above links you need to set the cookie inside
	 views.py, and replace it with the cookie of your session.
	 Instructions for cookie set up:
	 1)Open the following link in your browser : http://localhost:8000/pcp/customer/ (Django-rest control panel)
	 2)Inspect the page
	 3)Press Network tab in inspection
	 4)Press the GET button in the page
	 5)In the list of column name you will see a Http response with name : 'customer/' 
	 6)Right click with the mouse and press copy --> copy request headers
	 7)Paste in an empty editor
	 8)Copy the cookie information and paste it in line 357 in views.py, inside the valuePair of key 'Cookie' of the dictionary.
	 9)Save views.py
	 10)Go to http://127.0.0.1:8000/pcp/login_api/ and login as admin.
	 11)Now you can have access to the information of the api.

	-Inside PcPeripherals app, there is a utils.py. It has been created for store some functions for repetitive use.

	 Thank you for your time. In advance, 
	   Pantelakis Ioannis

	
