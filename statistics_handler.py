import tkinter as tk
import pandas as pd

class Statistics:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.distance_threshold_var = tk.StringVar()  
        # EDIT: Changed from tk.IntVar() to tk.StringVar() to manually validate input and avoid crashes

    def show_statistics(self):
        """Displays statistics in the provided frame."""
        for widget in self.parent.winfo_children():
            widget.destroy()

        self.df = pd.DataFrame(self.data_handler.data)  
        # EDIT (Bug 6): Load the DataFrame once here and store as self.df to reuse later (better performance)

        self.df['Distance'] = pd.to_numeric(self.df['Distance'], errors='coerce')  
        self.df['Age'] = pd.to_numeric(self.df['Age'], errors='coerce')
        # EDIT (Bug 4): Also convert 'Age' to numeric safely, so we can calculate median age later

        input_frame = tk.Frame(self.parent)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Enter the distance threshold (km):").pack(side="left")
        # EDIT: Improved label text for clarity ("(km)")

        distance_entry = tk.Entry(input_frame, textvariable=self.distance_threshold_var)
        distance_entry.pack(side="left")

        tk.Button(input_frame, text="Update", command=self.update_statistics).pack(side="left")

        self.stats_frame = tk.Frame(self.parent)
        self.stats_frame.pack(fill="both", expand=True)

        self.update_statistics()  
        # EDIT: Initial statistics display loads automatically

    def update_statistics(self):
        """Updates the statistics based on the distance threshold."""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        try:
            threshold = int(self.distance_threshold_var.get())
            valid_threshold = True
        except ValueError:
            valid_threshold = False
            # EDIT (Bug 1/2): Added try-except input validation to prevent app crash if user enters letters

        if valid_threshold:
            traveled_more = self.df[self.df['Distance'] > threshold]
            if len(self.df) > 0:
                percentage_traveled_more = (len(traveled_more) / len(self.df)) * 100
            else:
                percentage_traveled_more = 0
            # EDIT: Added a check to avoid division by zero if no data

            tk.Label(
                self.stats_frame,
                text=f"📍 {percentage_traveled_more:.2f}% traveled more than {threshold} km"
            ).pack()
            # EDIT: Updated label text for better clarity and added an icon

            # --- New Meaningful Stats (Bug 4) ---
            avg_distance = self.df['Distance'].mean()
            median_age = self.df['Age'].median()
            total_attendees = len(self.df)

            tk.Label(
                self.stats_frame,
                text=f"📈 Average distance traveled: {avg_distance:.2f} km"
            ).pack(pady=(5, 0))
            # EDIT: Added display of average distance traveled

            tk.Label(
                self.stats_frame,
                text=f"👥 Median age of attendees: {median_age:.2f} years"
            ).pack(pady=(5, 0))
            # EDIT: Added display of median age of attendees

            tk.Label(
                self.stats_frame,
                text=f"🎟 Total number of attendees: {total_attendees}"
            ).pack(pady=(5, 0))
            # EDIT: Added display of total number of attendees

        else:
            tk.Label(
                self.stats_frame,
                text="⚠️ Please enter a valid number for distance.",
                fg="red"
            ).pack()
            # EDIT: Displayed a red-colored friendly error message if the input was invalid

        # Accommodation + Ticket breakdown
        tk.Label(self.stats_frame, text="🎟 Accommodation + Ticket Type Breakdown:").pack(pady=(10, 0))
        # EDIT: Improved section heading with an icon and extra top padding

        if not self.df.empty:
            combinations = self.df.groupby(['Accommodation', 'Ticket']).size().unstack(fill_value=0)
            percentages = combinations.div(combinations.sum(axis=1), axis=0) * 100

            for accommodation in percentages.index:
                for ticket in percentages.columns:
                    percentage = percentages.loc[accommodation, ticket]
                    tk.Label(
                        self.stats_frame,
                        text=f"• {accommodation} - {ticket}: {percentage:.2f}%",
                        anchor="w"
                    ).pack(anchor="w")
                    # EDIT: Improved readability with bullet points and left-aligned text
