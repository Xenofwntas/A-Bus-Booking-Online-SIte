# Projects summary
In this project, I have created a travel site where you can book seats, choose destinations and enjoy your trip with the luxurious electric CS50express busses.

# Distinctiveness and Complexity
In this project you will find:
- Register/login/logout operations with error checks
- Fetch with csrf token when input fields are selected and appending inputs in real time
- The ability to save multiple routes with one submit
- The ability to choose from and book multiple seats
- Search for destinations
- User restrictions
- Models for users, places, booking seats and routes
- Bootstrap and css beautification

# What is contained in each file created
#### on capstone/static
- **img** file has some images used on the site
- **js** file has the JavaScript files for different html files
    - **create_routes.js** | has a function to hide the option that is selected in the "select" html tag and the function for flatpickr (a datepicker)
    - **set_seats.js** | has enable/disable submit button, change color of buttons if pressed or unpressed and update the total price
    - **tickets.js** | has a function to print the contents of the purchase information
    - **travel.js** | has the same functions as create_routes + get csrf token, when destination/departure/date are selected we fetch the time choices and append them to the input and check if there are no routes for that date
- **style.css** has the css for our site

#### on capstone/templates/capstone
- **create_routes.html** | This is the page where the staff user can create multiple routes with one submit and it is linked with create_routes.js.
- **destinations.html** | Here we display all destinations , a link to places.html and a link to travel.html.
- **index.html** | Our index page with a carousel and a link to create account or link to travel page if logged in.
- **layout.html** | The header of our site + navbar with links to our pages based on user authentication and a searchbar for destinations + messages.
- **login.html** | Basic login page with a link to the sign in page.
- **messages** | Messages that we include in layout.html.
- **place.html** | Display of all images for that place and some information about the place + a link back to destinations
- **profile.html** | Display the routes that we have purchased tickets with a link to see the purchase information for that route.
- **register.html** | Basic register page with a button linked to the sign up page
- **set_seats.html** | Here we check if a seat is already taken for that route and we disable/change color it. A submit button to complete the purchase and a display in card format of destination and departure info. This file is linked with set_seats.js
- **tickets.html** | Purchase information with a button to print them out. This file is linked with tickets.js
- **travel.html** | Inputs to select route, the time choices are automatically inserted when user selects destination/departure/date. A submit button and if directed here from destinations a link back to destinations. This file is linked with travel.js
#### on capstone/models.py
Here we have our models
- **User** | Basic user model.
- **Places** | Model for places.
- **Route** | Model for routes with foreign key to places and user with serialize for our fetch.
- **Images** | Extra images for our places model.
- **Ticket** | The model for tickets/seats with foreign keys to user and route.
#### on capstone/urls.py
Our paths.
#### on capstone/views.py
- **loginPage** | Sign up with error checking.
- **registerPage** | Register with error checking.
- **logoutUser** | Logout.
- **index** | Get all places from database for our carousel display in index.html.
- **destinations** | Get all places from database and display them in destinations.html.
- **place** | Get the specific place and its images and display them in place.html.
- **searchDestination** | Get the user's input and search places that contain the user's input.
- **createRoutes** | Get user's input, iterate them through the dates he selected and save them to the database.
- **getTime** | Get destination/departure/date and pass the available times of the route on that specific day.
- **travel** | Get places and display them in select tags on travel.html.
- **getRoutes** | Get user's inputs, find the specific route that he is interested in and pass him the seats so he can chooce on set_seats.html.
- **tickets** | Find the seats the user wants and add them to the database on his name. Display seats/total price/route on tickets.html.
- **profile** | Get the routes that the user has seats in and display them in profile.html.
- **view_tickets** | Find the seats the user has on that specific route and display seats/total price/route on tickets.html.

# How to run the application
- Create a staff user and press on Create Repeated Route
- Fill in the inputs and create multiple routes
- Register as a user
- Hit travel and choose departure/destination/date and time then submit
- Choose one or more seats to book and submit
- You can print your purchase now or visit your profile later to see it


