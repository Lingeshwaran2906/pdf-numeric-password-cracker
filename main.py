import pikepdf
from pikepdf import PasswordError
import time
import os
import tkinter as tk
from tkinter import filedialog
from datetime import timedelta

# --- 1. FILE SELECTION ---
root = tk.Tk()
root.withdraw() 
selected_pdf = filedialog.askopenfilename(title="Select your locked PDF", filetypes=[("PDF files", "*.pdf")])

if not selected_pdf:
    print("No file selected. Exiting...")
    exit()

# --- 2. USER CONFIGURATION ---
digit_choice = int(input("How many digits (e.g., 11 or 12): "))
start_num = int(input(f"Enter starting number (Check resume_checkpoint.txt for last number): "))

# Calculate the end based on digits
end_num = (10 ** digit_choice) - 1

print(f"\nTargeting: {selected_pdf}")
print(f"Range: {start_num:0{digit_choice}d} to {end_num:0{digit_choice}d}")
print("Press Ctrl+C to stop and save progress.\n")

current_num = start_num
start_time = time.time()
update_interval = 100  # Updates the screen every 100 attempts for a 'Live' feel

# --- 3. MAIN LOOP ---
try:
    while current_num <= end_num:
        password = f"{current_num:0{digit_choice}d}"
        
        try:
            with pikepdf.open(selected_pdf, password=password) as pdf:
                print(f"\n\n[SUCCESS] Password: {password}")
                with open("found_password.txt", "w") as f:
                    f.write(f"Password: {password}")
                exit()
        except (PasswordError, pikepdf.PdfError):
            pass
        
        current_num += 1

        # LIVE UPDATE LOGIC
        if current_num % update_interval == 0:
            now = time.time()
            elapsed = now - start_time
            
            # Avoid division by zero
            if elapsed > 0:
                speed = int(update_interval / elapsed)
                remaining = end_num - current_num
                seconds_left = remaining / speed
                time_left = str(timedelta(seconds=int(seconds_left)))
                
                # Update the line instantly
                print(f"Guessing: {password} | Speed: {speed}/sec | Time Left: {time_left}   ", end="\r")
            
            start_time = time.time() # Reset timer for next live update

except KeyboardInterrupt:
    print(f"\n\nStopped. Last tried: {current_num:0{digit_choice}d}")
    with open("resume_checkpoint.txt", "w") as f:
        f.write(str(current_num))
    print("Progress saved to 'resume_checkpoint.txt'.")