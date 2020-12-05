# Final_Project

Final Project - JHU EN.640.635

Cam & Cam's Harbor Bike Rentals

Team Members: Cameron Carter & Cameron Guernsey

This project consists of a single python code: Bike_Rental_System.py.

This python code, when entered in a terminal, runs a program that functions as a bike rental system.
The program allows users to create their own accounts and login securely to what would be considered our "database."
Users are then able to rent and return bikes similar to the services Bird and Lime offer with electric scooter rentals.
The code will document the real time that users rent the bike and charge the user when they return the bike.
The total cost will be a base fee of $4.00 plus 10 cents per minute they spend renting.
The python code is based on the main User class that tracks user attributes, including name, username, password, rental status, bike being rented, and the user's personal encryption key.
A list of bikes also exists to track the bikes in the system and which bikes are available for rent.
There are several functions that mirror the actions users can take within the rental system.
For example, a user starts by either creating an account or logging in to their existing account. 
Then to rent a bike, they would simply input the bike number into to the terminal.
Once a user has completed their use and is ready to return the bike, they start at the main screen by entering their bike number.
The terminal will return the user's total cost to rent the bike, at which point payment would be made to the nearest Cam.
Many non-visible functions allow users to create and encrypt their own passwords with randomly generated personalized keys.
Error handling has also been heavily implemented to return users to main screens or previous functions/actions if their input is invalid. 

In order to run the code itself, the file simply needs to be run in the terminal.
The main function rent_or_return() is executed inside an infinite while loop, which simulates the program running as a user is inside the rental app/program.
This function returns the master list of users as well as the running list of available bikes for rent.
The functions to rent, return, create an account, and login are all called within the rent_or_return() function.
In order to navigate these options the user will need to input either a number or a string that matches the directions output in the terminal.

For example, the main function will output: Would you like to 'Rent' (1) or 'Return' (2)? Or enter 'Exit' (0) to exit the program.

The user can then type either "Rent" or the number 1 in order to call the rent function. The functionality is the same for the other input options.

When creating an account or logging in, the user will have to manually input their desired information and press enter.
As a note, the input for the password is hidden from the user so that the password will never be physically displayed in the code or the terminal.
It will be saved as an encrypted string in the master list.
Once the user is finished and closes the programs, the create_excel() function is called which turns the master list into an Excel database.
This spreadsheet holds all of the users' information to identify them (including the encrypted password, not the password itself) and display their current rental status.
