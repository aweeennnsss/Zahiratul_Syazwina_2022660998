import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class TrainTicketSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Train Ticket Receipt System")

        # Variables
        self.username_var = tk.StringVar()
        self.user_ic_var = tk.StringVar()
        self.user_date_var = tk.StringVar()
        self.user_time_var = tk.StringVar()
        self.user_coach_var = tk.StringVar()
        self.user_seat_var = tk.StringVar()
        self.original_location_var = tk.StringVar()
        self.destination_var = tk.StringVar()

        # Labels
        tk.Label(root, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Label(root, text="IC Number:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Label(root, text="Date:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Label(root, text="Time:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        tk.Label(root, text="Coach:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        tk.Label(root, text="Seat:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        tk.Label(root, text="From:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        tk.Label(root, text="To:").grid(row=7, column=0, sticky="e", padx=5, pady=5)

        # Entry widgets
        tk.Entry(root, textvariable=self.username_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(root, textvariable=self.user_ic_var).grid(row=1, column=1, padx=5, pady=5)
        tk.Entry(root, textvariable=self.user_date_var, validate="all", validatecommand=(root.register(self.validate_date), "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")).grid(row=2, column=1, padx=5, pady=5)
        tk.Entry(root, textvariable=self.user_time_var).grid(row=3, column=1, padx=5, pady=5)
        tk.Entry(root, textvariable=self.user_date_var, validate="focusout", validatecommand=self.validate_date).grid(row=2, column=1, padx=5, pady=5)
        tk.Entry(root, textvariable=self.user_seat_var).grid(row=5, column=1, padx=5, pady=5)
        tk.Entry(root, textvariable=self.original_location_var).grid(row=6, column=1, padx=5, pady=5)
        tk.Entry(root, textvariable=self.destination_var).grid(row=7, column=1, padx=5, pady=5)

        # Combobox for time selection
        times = [f"{hour:02d}:00" for hour in range(8, 23)] 
        self.time_combobox = ttk.Combobox(root, values=times, state="readonly")
        self.time_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.time_combobox.set(times[0])  

        # Combobox for coach selection
        coaches = ["Coach A", "Coach B", "Coach C", "Coach D", "Coach E", "Coach F"]
        self.coach_combobox = ttk.Combobox(root, values=coaches, state="readonly")
        self.coach_combobox.grid(row=4, column=1, padx=5, pady=5)
        self.coach_combobox.set(coaches[0]) 

        # Combobox for seat selection
        seats = [f"{row}{seat}" for row in range(1, 17) for seat in ["A", "B"]]
        self.seat_combobox = ttk.Combobox(root, values=seats, state="readonly")
        self.seat_combobox.grid(row=5, column=1, padx=5, pady=5)
        self.seat_combobox.set(seats[0]) 

        # Button to generate receipt
        tk.Button(root, text="Generate Receipt", command=self.generate_receipt).grid(row=8, column=0, columnspan=2, pady=10)

    def validate_date(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if trigger_type == "focusout" or trigger_type == "key":
            try:
                if value_if_allowed:
                    # Validate the date format
                    datetime.strptime(value_if_allowed, "%Y-%m-%d")
                return True
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use yyyy-mm-dd.")
                return False
        return True
    
    def generate_receipt(self):
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Train Ticket Receipt")

        selected_time = self.time_combobox.get()
        selected_coach = self.coach_combobox.get()
        selected_seat = self.seat_combobox.get()

        # Determine the base price based on the selected coach
        if selected_coach == "Coach A":
            base_price = 50
        else:
            base_price = 30

        # Check if the user purchases a ticket before 12 pm
        purchase_time = datetime.strptime(selected_time, "%H:%M")
        if purchase_time < datetime.strptime("12:00", "%H:%M"):
            base_price = 50 

        # Calculate the total price
        total_price = base_price  

        receipt_text = f"""
        Username: {self.username_var.get()}
        IC Number: {self.user_ic_var.get()}
        Date: {self.user_date_var.get()}
        Time: {selected_time}
        Coach: {selected_coach}
        Seat: {selected_seat}
        From: {self.original_location_var.get()}
        To: {self.destination_var.get()}
        Total Price: RM {total_price:.2f} 
        """

        tk.Label(receipt_window, text=receipt_text, justify="left").pack(padx=10, pady=10)

            # Insert data into the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ticket_train"
            )
        cursor = mydb.cursor()

        sql = "INSERT INTO `ticket_info` (user_name, user_ic, user_date, user_time, user_coach, user_seat, user_origin, user_destination, user_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.username_var.get(), self.user_ic_var.get(), self.user_date_var.get(), selected_time, selected_coach, selected_seat, self.original_location_var.get(), self.destination_var.get(), total_price)

        try:
            cursor.execute(sql, val)
            mydb.commit()
            print("Data inserted successfully!")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            mydb.rollback()

        cursor.close()
        mydb.close()

def quit_application():
    root.destroy()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = TrainTicketSystem(root)
    root.protocol("WM_DELETE_WINDOW", quit_application)  # Handle window close
    root.mainloop()
