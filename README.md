# SHOULD YOU MINE BITCOIN BTC? CAPSTONE PROJECT

## Distinctiveness and Complexity:

The django websites that we built in the course were a wiki, a commerce, an email, and a social media website. And although 
the previous homework assignments were complex, from building databases to having javascript control the entire website. My 
final project used a simple Models database and some javascript to let the site viewer know if they should mine bitcoin in
the state they chose.


## Description of the website:

In the website the user will visit the one page and select what state they would want to see if they should mine bitcoin. The
user will then be showed a "yes" or a "no" along with a description on how much bitcoin costs now and how much a rough
estimate would be to mine the one bitcoin. I have taken data from a website on what the average price per kwh is in each
state including the District of Columbia. If the price of the bitcoin is higher than the price it would cost to mine it the
user will be provided with a "yes" and the same for the opposite. The price of bitcoin is updated every minute so the user 
might get a different result to the question after a minute.


## Models

In the models file I made one named "States" for the storing the price of each kwh in each state including the District of
Columbia. In the Model I used "name" for storing the name of the state, "abrv" as abbreviation of the state, and
"avg_price_per_kwh" for storing the average price per kwh of the state.


## Views

I only used two functions in views.py: "home" and "get_price". The "home" function is the entire website, pulling each of the
state's data and pushing it into the html file. And the "get_price" function is used for POST method to update the price of
BTC to USD, using the requests module in python, pulling the data from the website:
"https://api.coindesk.com/v1/bpi/currentprice.json"


## HTML page

"Index.html" is the only html page I made. Inside it uses a javascript function to pull the data selected from the drop down
And does the calculation instantly.


## Javascript file

"Index.js" is the only javascript file, and all it does is submit a post request to "get_price" url on django.