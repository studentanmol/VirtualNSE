# Virtual NSE Stockmarket

## Video Demo

<https://youtu.be/-XhRjF8cUBI>

## Description

This website allows users to virtually buy and sell shares of companies listed on the National Stock Exchange, India. All prices given and used are real-time prices which were obtained by importing nsetools in my code. The website will maintain each individual user's portfolio and provide information about their current profit or loss based on real-time prices. This site will be useful for people who want to learn about stockmarket without risking their money. New and young investors can use this site to get an idea about how NSE by using virtual money to buy stocks before risking actually money. I was searching for a virtual stock market website for Indian stockmarkets but was unable to find good free websites. That's when i got the idea to make this website as it also combined my 2 interests-coding and stockmarket.

### **helpers.py**

This file contains some helper functions that will be used in the application.py file for my website. In this file I am importing [nsetools](https://nsetools.readthedocs.io/en/latest/index.html) which is a library that allows me to find the current price of any stock on the National Stock Exchange.
Then there is a login_required function that checks if the user has logged into the website and if they have not then redirects them to the login page. This function is used for pages where it is required  to login in order to view them.
There is a rupees function that inputs a value and returns the value formatted to 2 decimal places with an Indian Rupee sign before it. This function will be required since the website will be dealing with a lot of figures in Indian rupees.
Next is the lookup function which inputs a stock symbol from the user and returns the stock quote of that company in the form of a python dictionary.It has 7 keys:

1) **name** which stores the name of the company.
2) **price** which stores the latest price of the stock whose symbol the user entered.
3) **symbol** stores the capitalized symbol of the stock.
4) **dayHigh** which stores the highest price the stock reached on that day.
5) **dayLow** which stores the lowest price the stock reached on the day.
6) **yearHigh** which stores the highest price the stock reached in the year till that time.
7) **yearLow** which stores the lowest price the stock reached in the year till that time.

If there is any error in the value returned then this function returns None.
Lastly is the apology function. This function takes a message as an input and returns a stock market themed apology image, stored in static folder, with the message at the bottom of the image and error code 400 at the top.

### **requirements.txt**

That file simply prescribes the packages on which this app will depend, namely cs50, Flask, Flask-Sessions and requests.

### **finance.db**

This is a SQLite database that stores various tables which will be required for this website. The tables are:

- **Users** : This table will store user details. It has columns *id* which is PRIMARY KEY to store user_id and is INTEGER type, *username* which will store username and is TEXT type and has constraint NOT NULL, *hash* which will store hash of the user's password and is TEXT and has NOT NULL constraint, *email* which stores user's email and is data type TEXT and *cash* which will store the user's cash is NUMERIC type and has constraint NOT NULL and DEFAULT value of 100000.
- **usernames** : This table will store the username of users who are currently logged into the site. It only has one column *username* which is TEXT.
- **portfolio** : This table will store the current portfolio for each user. It's columns are *id* INTEGER which will store user_id of each user, *symbol* of data type TEXT which will store the stock symbol, *name* of type TEXT which stores the username of the user, *company* whose data type is TEXT which stores the name of the stock they have, *number* of INTEGER type which stores the number of shares they have bought for that particular company, *price* with data type NUMERIC which stores the price at which they bought that stock and *total* whose data type is NUMERIC which stores the total amount they have spent for that stock, i.e. number*price.
- **shares** : This table stores all the transactions a user made on the website. It is used to display a history of which shares the user bought and sold. This table has the columns *name* of type TEXT which stores the username, *company* whose data type is TEXT and has constraint NOT NULL which stores the name of the stock, *number* with data type INTEGER which contains the number of shares bought or sold, *price* of NUMERIC type which contains the price of the share when it was bought or sold, total of data type NUMERIC which contains the total amount spent or gained for that transaction, *symbol* of type TEXT which stores the symbol of the stock, *id* of type INTEGER which stores the user_id of the user, *status* of type TEXT and with constraint NOT NULL which stores what happened to the share i.e. whether it was bought or sold and *time* whose data type is DATETIME which stores the date and time of when the transaction happened.

### **static folder**

This folder contains:

- The icon that will be used in the heading of the website. I really liked this emoticon so decided to go with it.

- The photo that will be used to display error messages. Since my website is stock market themed i decided to go with a similar photo for error   messages.

- styles.css, the CSS file that contains all the design modifications used in this website.
  - The website is designed using the dark and light theme. Each page of the website has a dark navabar. The leftmost part of the navbar contains the name of the website which is multicolored and is also a link to the index page. Then from left to right there are several links that the user can click to visit different routes like About, Quote, Buy, Sell, History. At the extreme right are the links for either login and register, if they have not logged in, or logout change_username, password and add cash if they have. There is no background for most of the web pages making the website feel simple yet efficient. The input fields for all forms in the website and rounded with a border. The submit buttons are blue which darken when user hovers their mouse on them. The tables are all black and white themed which makes it easier to read data given in them. Thus the entire website looks elegant and soothing to the eyes.

### **templates**

This folder contains all the html files used in building the website. All html files 'extend' layout.html. Thus they have the same layout and only differ in their individual functionalities.

- add.html : This file contains a form whose method is post. It only contains one input field that accepts a numeric value from the user and a submit button.

- apology.html : This file contains the apology that will be shown to users in case of a programming error or user error. It contains an image taken from the static folder. The image will have some text on the top and the bottom. These text messages will be taken from application.py.

- buy.html : This html page will be shown to user when they want to buy a stock. It contains a form with method post. The form has 2 input fields and a submit button. The first input field will accept the symbol of the stock and the second input field will accept the number of shares the user wants to buy.

- change_email.html : This file contains a form with method post. It will be displayed to the user for when they want to change their email. It consists of a single input field for the user to enter their new email address and a submit button.

- change_password.html : This file has a form where users will be able to change their password. It consists of an input field to take password and a submit button.

- change_username.html : This file contains a form with method post. It will be displayed to the user for when they want to change their username. It consists of a single input field for the user to enter their new username and a submit button.

- history.html : This file will display to the user all the transactions that they have performed. It consists of a table with 6 columns. There is a for loop that is used to show table data. The curly braces are a placeholder for data. Thus for each transaction in dict history the various attributes in it are printed.

- index.html : This is the home page that users will see when they log into the site. This page contains their current portfolio. It consists of a table with 5 columns. The table headers are: symbol, name, share, price and total. For the table data, the portfolio dict is taken from _application.py_. A for loop is used to get each value in dict and put it in table. After the for loop, a cash row is placed to show the amount of cash left for each user. Users total and grand total is also displayed. At the end of the table the net earnings of a user is shown, i.e. their net profit or loss.

- layout.html : This file contains the basic structure of the webpage that will be present throughout. The head contains the various links and scripts from bootstrap used in the website. The _styles.css_ that contains the css styles for the website is also linked here along with the icon that will be seen in the head of the webpage. The title contains a block that will change according to the page. The body of the page starts with a navbar which will be at the top of the webage which is dark themed. The name, 'Virtual StockMarket' is in the left hand side of the navbar and is multicolored. The name is also a link that will redirect user to homepage when clicked. An if-else statement is used using curly braces that shows different items in the navbar depending on whether session_id is there for a user or not. This will ensure that if a user has not logged in then they will only see login and register options in the navbar,while a logged in user can view all the options in the website. These items are also links to their respective pages. Next in layouts there are alerts. This will flash a message to the user. Whatever is in double quotes in flash will be displayed as an alert to user. Then there is another block that is there as a placeholder. All of the other html pages will extend this block for their main content. At the end there is a footer that gives credit to where the API was used from an to CS50 without whom this website would not have been possible.

- login.html : It has title login. This page will e shown to user for them to login to the site. The body consists of a form with method post. It has 2 input fields that take username and password from user and a submit button.

- quote.html : This page has title Quote. It will be shown to the user when they want to quote a stock. This page consists of a form with method post and has 1 input field that takes symbol of stock and a submit button.

- quoted.html : This page has title Quote. It will be used to show the user the quote of the stock they requested. It consists of a text that has the share name, symbol and current price. It will be taking these values from the tuple shared by application.py. This webpage will also show an unordered list of the day and year high and low prices of that stock.

- register.html : This page has title Register. It will be used to register the users. It consists of a form with method post. It has 3 input fields for username, email, password and also has another input field for user to confirm password. There is also a submit button.

- sell.html : This page will be shown to the user when they want to sell their stock. It consists of a form with method post. It consists of a dropdown list which will only contain those shares which the user owns as they can only sell stocks that they own. The default disabled option will be 'select shares' and the other options will be taken from application.py and inserted in this list. There is also a submit button.

- welcome.html : This page consists of information about the website and what its various features are. It welcomes the user by taking their name from application.py. This is followed by a list stating the various features of the website and how the user can navigate and use the website.

### **application.py**

SQL is imported from cs50. Flask is used to generate the website so flask library is also imported along with sessions. Werkzeug security is imported to generate password hash for user. All functions from helpers.py have been imported.
Flask app is configured and then caching of responses is disabled to ensure that the browser knows if some change is made to a file when a session is on. Then I configured Jinja with a custom function rupees made in the helpers.py file which makes it easier to format values in rupees. Then I configure flask to store sessions on the local filesystem instead of the default cookies. Then I configure cs50's sql module to use finance.db, a SQLite database I made for this website. A list called portfolio is declared. This list will be used in index to display the user's portfolio. I used a list since it would not be possible to create a table for each user and on refreshing the page the latest price and valuation are easily displayed and there is no repetition. The login_required decorator is used for all routes other than register and login. This will ensure that only those users who have registered and logged in can access the features of the website.

#### **about**

Route about is created, that will have the description about the website. The login required decorator is used that means only those users who have logged in can visit this route. The username of the logged in user is stored in a variable called username. Welcome.html template is rendered and this username is passed to it.

#### **index**

Next the index route is configured, which will show users their portfolio of stocks. The users remaining cash is stored in 'remaining'. The variable shares stores the contents of the portfolio table for that user, total stores the total amount user has in shares and cash stores their remaining cash. The list portfolio is emptied and sum_price is initialized to 0. For each share that the user owns, the following actions are done:

- the lookup function is called on the share symbol and the value returned is stored in quote.
- 'quote' has the current price of the share which is stored in a variable.
- The stock symbol, name, number of shares, latest price of the stock and the total(number of shares*current price) are all appended to the portfolio list.
- The sum_price variable maintains the total amount that all the users stocks are worth.

After the loop the index.html template is rendered and the username, portfolio list, cash, amount in shares, grand total and the users net profit or loss are all passed to it.

#### **buy**

The buy route is where the user can buy stocks to add to their portfolio. It accepts two methods - GET and POST.
If the POST method is returned, i.e. the user submitted a form to buy, then I first check if the users input if any was correct and return the  appropriate error message if it was not.Next I store the users portfolio in 'index'. I check if the user has enough cash to buy that number of shares and return an error message if they do not.Next for each row in index, I check if the user already owns some number of the shares they want to buy and if they do then I UPDATE the portfolio table for that user and add the new shares they bought to their existing ones along with the updated total.However, if they do not own that share then a new row is INSERTED in the portfolio table with the required details about the stock. This new buy is also added in the shares table that stores the users history. Finally the users cash in the 'users' table is reduced by the total amount they spent to buy the stocks.The user then sees a message saying Bought on their screen and are redirected to the index page of the website.
However if the route is called via GET method then the buy.html template is rendered.

#### **history**

Next the history route is created which shows the user their transaction history. It is only called via default GET.The users history is taken from 'shares' sql table and is ordered such that the most recent transaction is shown at the top and is stored in history variable. Then the history.html template is returned and the variable history is passed to it.

#### **login**

The login route accepts both GET and POST method.
If the method is POST,i.e. the user submitted a login form then I first check if the users input if any was correct and return the appropriate error message if it was not.I check if the username exists in the 'users' sql table. If it does exist then the check_password_hash function is used to see if the corresponding password is correct. If the username and password are correct then the user id is added to session. The username is also added to the username table which stores all logged in users. Then users are redirected to index page.
If the route is called via GET then the login.html template is returned.

#### **logout**

The logout route only accepts default GET method.First the session is cleared of user id. Then the users username is removed from username table.Finally, the user is redirected to index page but since they are not logged in they will reach the login page.

#### **quote**

This route is used to accept a stock symbol and show its quote. It can be called via both GET and POST.
If the method is POST, then the user should see a quote of the stock they entered. However, first I check if the user has entered a symbol and if they have then if it is a correct symbol. The appropriate error messages are displayed if there is any user error. If the symbol is correct then quoted.html template is rendered and the value returned when the lookup function is called on the symbol is passed to it.
If the method is GET then the quote.html template is rendered which shows the user a form to enter the stock symbol.

#### **register**

The register route is used to register a new user in the database. It can be called via two methods GET and POST.
If the method is POST then the user has submitted the form to register themselves. First I must check if the user has filled all the input fields correctly and must show appropriate error messages if they have failed to do so. I check the users sql table to see if the username and email they have entered is already in use by another user,If it so then the correct apology is returned. If there are no errors then the users details are entered into the 'user' table and the password entered is first hashed using the generate_password_hash function. Thus the user has now been entered into the system and are registered. This successful registration message is flashed on their screen before they are redirected to the login page.
If the user reached this route via GET then the register.html page is rendered, which is a form for them to register themselves.

#### **sell**

This route is used if the user wants to sell a stock they own.It takes two methods GET and POST.
If the route is called via POST method, it means the user submitted a form to sell their stock by selecting a symbol. First I check if the user entered a symbol or number of shares to sell. Then I must check if they entered a positive number greater than 0. Next I must check if the user owns the stock or has the number of shares they have input for that stock. If all these cases arise then the appropriate error message is returned. If none of these cases are true then the latest price of the stock is found by using lookup function. The details of the shares are INSERTED into the shares table which stores transaction history for users. Next the users table is UPDATED by adding the cash gained from the selling of the stock. The portfolio table is then UPDATED by subtracting the number of shares sold of that stock. If the quantity of that stock is sold then that stock is DELETED from the portfolio table. A message is flashed telling the user that the shares were sold successfully and the user is redirected to the home page.
However, if the route is called via GET method then the user is shown a form with the stocks they own already present on a dropdown list and an input field to enter the number of shares. The sell.html template is rendered and the stock symbols the user owns are passed to it.

#### **change_username**

This route accepts both GET and POST and is used if the user wants to change their username.
If the method is POST then it means the user has submitted the form to with the new username. First I check if the user has input a username and if it is unique. If it they are unable to satisfy the above conditions then an appropriate error message is displayed. If the new username is acceptable then the users table is UPDATED with it and the username changed message is flashed to the user before they are redirected to the login page.
However if the GET method is called then the change_username.html page is returned.

#### **change_password**

This route accepts both GET and POST methods and is used by the user to change their password.
If the POST method is used it means the user submitted a form to change their password. If an empty field was submitted then an error message is returned. If not then the new password is hashed and stored in the users table for that user. A password changed message is flashed to the user and they are redirected to the login page.
If the method is GET then change_password.html template is returned.

#### **add_cash**

This route is used if the user wants to add more cash to their default amount of 1,00,000 rupees. It has two methods GET and POST.
If the method is POST meaning if the user submitted a form to add cash then it is checked is the number user entered is greater than 0 and not None.If it is then the appropriate message is returned and if it is not then the extra cash is added by UPDATING the cash column in the users table for that particular user. A message of Cash Added is flashed and the user is redirected to the index page.
If the method requested is float then the add.html template is rendered and returned.
The last two functions are to handle error in the code.
This is my final project for CS50, hope you like it.

**Thank You!!**
