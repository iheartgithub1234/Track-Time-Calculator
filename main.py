import tkinter as tk
from tkinter import ttk

# Conversion factors
YARDS_TO_METERS = 0.9144
METERS_TO_YARDS = 1 / YARDS_TO_METERS
MPS_TO_MPH = 2.23694

# Event distances in meters (converted from yards where needed)
EVENT_DISTANCES = {
    "MPH": None,  # Special case
    "10yd": 10 * YARDS_TO_METERS,
    "10m": 10,
    "40yd": 40 * YARDS_TO_METERS,
    "60m": 60,
    "100m": 100,
    "200m": 200,
    "400m": 400,
    "800m": 800,
    "1600m": 1600,
    "1 mile": 1609.34,
    "3200m": 3200,
    "2 mile": 3218.68,
    "5000m": 5000,
    "10000m": 10000,
    "half marathon": 21097.5,
    "marathon": 42195,
    "50000m": 50000,
    "100 mile": 160934
}

def calculate_paces():
    try:
        # Get input values
        hours = float(hours_entry.get() or 0)
        minutes = float(minutes_entry.get() or 0)
        seconds = float(seconds_entry.get() or 0)
        
        # Get selected event
        selected_event = event_var.get()
        
        # Calculate total time in seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
        
        # Get distance for selected event in meters
        event_distance = EVENT_DISTANCES[selected_event]
        
        if selected_event == "MPH":
            # For MPH, we need to know the distance (can't calculate from MPH alone)
            # So we'll skip this case in input
            return
        
        # Calculate speed in m/s
        speed_mps = event_distance / total_seconds
        
        # Calculate MPH
        mph = speed_mps * MPS_TO_MPH
        
        # Prepare results
        results = {}
        
        for event, distance in EVENT_DISTANCES.items():
            if event == "MPH":
                results[event] = mph
            else:
                if distance == 0:
                    continue
                time_seconds = distance / speed_mps
                results[event] = time_seconds
        
        # Update output
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        
        # Format and display results
        for event, value in results.items():
            if event == "MPH":
                output_text.insert(tk.END, f"{event}: {value:.2f}\n")
            else:
                # Format time as h:m:s.d
                hours_out = int(value // 3600)
                remaining = value % 3600
                minutes_out = int(remaining // 60)
                seconds_out = remaining % 60
                
                if hours_out > 0:
                    time_str = f"{hours_out}:{minutes_out:02d}:{seconds_out:06.3f}"
                elif minutes_out > 0:
                    time_str = f"{minutes_out}:{seconds_out:06.3f}"
                else:
                    time_str = f"{seconds_out:.3f}"
                
                output_text.insert(tk.END, f"{event}: {time_str}\n")
        
        output_text.config(state=tk.DISABLED)
    
    except ValueError:
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Invalid input. Please enter numbers.")
        output_text.config(state=tk.DISABLED)

# Create main window
root = tk.Tk()
root.title("Track Time Calculator")
root.configure(bg='black')

# Set window size and make it resizable
root.geometry("800x800")
root.minsize(700, 700)

# Set larger fonts
large_font = ('Arial', 18)  # Increased from 14 to 18
input_font = ('Arial', 16)   # Font for input boxes
dropdown_font = ('Arial', 16) # Font for dropdown

# Input frame
input_frame = tk.Frame(root, bg='black', padx=15, pady=15)  # Increased padding
input_frame.pack(fill=tk.X)

# Time input
time_label = tk.Label(input_frame, text="Time (h:m:s.d):", fg='white', bg='black', font=large_font)
time_label.grid(row=0, column=0, sticky=tk.W)

# Hours entry
hours_entry = tk.Entry(input_frame, width=6, font=input_font, bg='grey', fg='white')  # Increased width
hours_entry.grid(row=0, column=1, padx=5)
tk.Label(input_frame, text=":", fg='white', bg='black', font=large_font).grid(row=0, column=2)

# Minutes entry
minutes_entry = tk.Entry(input_frame, width=6, font=input_font, bg='grey', fg='white')  # Increased width
minutes_entry.grid(row=0, column=3, padx=5)
tk.Label(input_frame, text=":", fg='white', bg='black', font=large_font).grid(row=0, column=4)

# Seconds entry
seconds_entry = tk.Entry(input_frame, width=10, font=input_font, bg='grey', fg='white')  # Increased width
seconds_entry.grid(row=0, column=5, padx=5)

# Event selection
event_label = tk.Label(input_frame, text="For Event:", fg='white', bg='black', font=large_font)
event_label.grid(row=1, column=0, sticky=tk.W, pady=(15, 0))  # Increased padding

event_var = tk.StringVar()
event_dropdown = ttk.Combobox(input_frame, textvariable=event_var, 
                             values=list(EVENT_DISTANCES.keys()), 
                             font=dropdown_font, state='readonly')
event_dropdown.grid(row=1, column=1, columnspan=5, sticky=tk.W+tk.E, pady=(15, 0))  # Increased padding
event_dropdown.set("100m")

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_paces, 
                           bg='grey', fg='white', font=large_font, padx=20, pady=10)
calculate_button.pack(pady=15)  # Increased padding

# Output frame
output_frame = tk.Frame(root, bg='black', padx=15, pady=15)  # Increased padding
output_frame.pack(fill=tk.BOTH, expand=True)

output_label = tk.Label(output_frame, text="Calculated Times:", fg='white', bg='black', font=large_font)
output_label.pack(anchor=tk.W)

output_text = tk.Text(output_frame, height=25, width=40, bg='grey', fg='white', font=large_font,
                     wrap=tk.NONE, state=tk.DISABLED)
output_text.pack(fill=tk.BOTH, expand=True)

# Add scrollbar
scrollbar = tk.Scrollbar(output_text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_text.yview)

# Run the application
root.mainloop()