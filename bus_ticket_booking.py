"""This is bus ticket booking system in Python, using MySQL to store ticket data for passengers. 
The code allows a user to book bus tickets, view their ticket details, and cancel tickets, while keeping track of available seats in the system."""

import mysql.connector
import datetime

#Connecting to database
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="practice"
)
mycursor = mydb.cursor()

# Create table if it doesn't already exist
try:
    mycursor.execute("create table passenger_data(passenger_id varchar(10), passenger_name varchar(40), seat_number int, city varchar(40), Ticket_price int)")
    print("Table created successfully")
except:
    print("Table already created")

#list of cities    
city_list=["Hosur", "Krishnagiri", "Dharmapuri", "Salem", "Erode", "Coimbatore"]

# Fetch already booked tickets
mycursor.execute("select seat_number from passenger_data")
result = mycursor.fetchall()
booked_tickets=[i[0] for i in result]
remaining = 15 - len(booked_tickets)
total = 0

# Store ticket details
details = []

# Function to write ticket details to a text file
def write_ticket_to_file():
    with open("ticket_details.txt", "a") as file:
        file.write(f"Bus Ticket Booking\n")
        time = datetime.datetime.now()
        file.write(f"\nDate:{time}\n")
        file.write(f"\nBooking details:\n\n")
        for j in details:
            file.write(f"{j}\n")
        file.write(f"Total amount: Rs.{total}/-\n\n")
        file.write("Thanks for booking the tickets")
        
# Function to show ticket details
def show():
    for data in details:
        print(data)
    print(f"Total amount : {total}")

# Function to get the price based on the city
def ticket_price(city):
    price_map = {
        "Hosur": 40,
        "Krishnagiri": 100,
        "Dharmapuri": 150,
        "Salem": 180,
        "Erode": 220,
        "Coimbatore": 250
    }
    return price_map.get(city, 0)

# Function to verify customer in the database
def verify_customer(passenger_id, passenger_name):
    verify_sql= "SELECT * FROM passenger_data WHERE passenger_id = %s AND passenger_name = %s"
    mycursor.execute(verify_sql, (passenger_id, passenger_name))
    result = mycursor.fetchall()
    return result

# Function to book a ticket
def book_ticket():
    sql = "INSERT INTO passenger_data (passenger_id, passenger_name, seat_number, city, Ticket_price) VALUES(%s, %s, %s, %s, %s)"    
    city = input("Select your city: ")
    if city in city_list:
        selected_seat = (input(f"Select your seat number => "))    
        seat_numbers = selected_seat.split(",")
        count=len(seat_numbers)
        try:
            for i in seat_numbers:
                seat = int(i)
                if seat not in booked_tickets:
                    passenger_id = "BTN" + str(seat).zfill(2)
                    passenger_name=input("Enter Passenger name: ")  
                    global total   
                    amount = ticket_price(city)
                    total = count*amount 
                    try:               
                        val = (passenger_id, passenger_name, seat, city, amount)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        booked_tickets.append(seat) # Update the booked seats list
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")           
                    details.append(f"Passgenger id: {passenger_id} - Passenger name: {passenger_name} - Booked seat number: {seat} - Amount: {amount}")                    
                    print("Data added successfully") 
                    print("Your tickets got booked successfully")                                 
                else:
                    print("sorry, your selected seat are already booked, please select another seat")            
        except ValueError:
            print("Invalid seat number format. Please provide a list of seat numbers separated by commas.")
            return        
    else:
        print("Please mention correct city")    
    view = input("Do you want to view your ticket? (yes/no): ").lower()
    if view=="yes":
        show()
    else:
        print("Thanks for booking!")  
        
# Function to view a ticket   
def view_ticket():
    passenger_id = input("Enter your Passenger ID:  ")
    passenger_name = input("Enter your Name:  ") 
    result = verify_customer(passenger_id, passenger_name)
    if result:
        your_ticket = result[0]
        print(f"Your ticket details is \n {your_ticket}") 
    else:
        print("Invalid ID and Name")

# Function to cancel a ticket
def cancel_ticket():
    passenger_id = input("Enter your Passenger ID:  ")
    passenger_name = input("Enter your name:  ") 
    result = verify_customer(passenger_id, passenger_name)
    if result:
        print(f"Please find the ticket details {result}")
        sql = "DELETE FROM passenger_data WHERE passenger_id = %s AND passenger_name = %s"
        try:
            mycursor.execute(sql, (passenger_id, passenger_name))
            mydb.commit()
            print(f"ticket cancelled successfully")
            booked_tickets.remove(result[0][2])  # Remove the seat from booked tickets list
            print(f"Ticket cancelled successfully.")
        except mysql.connector.Error as err:
            print(f"Error cancelling ticket: {err}")
    else:
        print("Invalid ID and Name")

# Main function to display menu and handle user input
def main():    
    print(f"Press 1 for Booking tickets")
    print(f"Press 2 for Veiw the tickets")
    print(f"Press 3 for Cancel the ticets")
    print(f"Available ticket count is {remaining}")         
    try:               
        num = int(input("Please provide your option --> 1 or 2 or 3: ")) 
        if num==1:
            print(f"Already booked seats list: {booked_tickets}")
            if remaining>0:
                book_ticket()
            else:
                print("Sorry, Ticket are sold out")
        elif num==2:
            view_ticket()
        elif num==3:
            cancel_ticket()
        else:
            print("Provide valid options -> 1 or 2 or 3")
    except ValueError:
        print("Invalid input")
    
# Run the program
if __name__ == "__main__":
    main()

#Generating bill
bill = input("Would you like to print your bill? yes/no: ").lower()
if bill=="yes":
    write_ticket_to_file()
    print("Your bill has been generated")
else:
    print("Bill has not generated")
