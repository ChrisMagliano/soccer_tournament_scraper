#!/usr/bin/env python
# coding: utf-8

# # Import needed libraries

# In[4]:


import tkinter as tk
from tkinter import ttk, messagebox
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# # Core script

# In the `webscrape_diretta_tutorial.ipynb` notebook we have seen how selenium allows to scrape the standings of tournaments by the [diretta.it](www.diretta.it) website.
# 
# In this notebook, we want to put that notebook in a Graphical User Interface by using the `Tkinter` package.
#  
# When the user launches the script, a GUI will appear with a dropdown menu and a label "Select the tournament:". This menu contains all the major soccer tournaments spread all over the world. Once a country has been chosen, it is sufficient to click the "Download data" to scrape data, visualize it on `Tkinter` and store it into the computer.

# In[5]:


# Path to your ChromeDriver executable
chromedriver_path = os.getcwd() + os.sep + 'chromedriver-win64\\chromedriver.exe'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if you don't need a GUI

# Set up the ChromeDriver service
service = Service(chromedriver_path)

# Dictionary of tournament links
link_tournaments = {
    'Italy - Serie A': 'https://www.diretta.it/serie-a/classifiche/#/zDpS37lb/table/overall',
    'Italy - Serie B': 'https://www.diretta.it/serie-b/#/E3qW2R34/table/overall',
    'England - Premier League': 'https://www.diretta.it/calcio/inghilterra/premier-league/#/lAkHuyP3/table/overall',
    'Spain - La Liga': 'https://www.diretta.it/calcio/spagna/laliga/#/dINOZk9Q/table/overall',
    'Germany - Bundesliga': 'https://www.diretta.it/calcio/germania/bundesliga/#/8l1ZdrsC/table/overall',
    'France - Ligue 1': 'https://www.diretta.it/calcio/francia/ligue-1/#/WYO1P5ch/table/overall',
    'Portugal - Primeira Liga': 'https://www.diretta.it/calcio/portogallo/liga-portugal/classifiche/#/0d7EBBWo/table/overall',
    'Netherlands - Eredivise': 'https://www.diretta.it/calcio/olanda/eredivisie/#/KCMrEcSo/table/overall',
    'Belgium - Jupiler League':'https://www.diretta.it/calcio/belgio/jupiler-league/classifiche/',
    'Turkey - Super Lig': 'https://www.diretta.it/calcio/turchia/super-lig/#/jy5jZF2o',
    'Argentina - Liga Profesional':'https://www.diretta.it/classifiche/fyaNEkG1/UwflyvqC/#/UwflyvqC/table/overall',
    'Brasil - Serie A':'https://www.diretta.it/calcio/brasile/serie-a/classifiche/#/Klz7n21m/table/overall',
    'Saudi Arabia - Saudi Professional League':'https://www.diretta.it/classifiche/tKRzyaE3/v5VHH4vs/#/v5VHH4vs/table/overall',
    'Denmark - Superliga':'https://www.diretta.it/calcio/danimarca/superliga/classifiche/#/CCjlHSnr/table/overall',
    'Ireland - Premier Division':'https://www.diretta.it/calcio/irlanda/premier-division/classifiche/#/dxrviyLi',
    'Scotland - Premiership':'https://www.diretta.it/calcio/scozia/premiership/classifiche/',
    'Switzerland - Super League':'https://www.diretta.it/calcio/svizzera/super-league/classifiche/',
    'USA - MLS':'https://www.diretta.it/calcio/usa/mls/classifiche/#/0hDNWqLM/table/overall'
}


# In[6]:


def scrape_data(tournament_url):
    """ Function to scrape data for a selected tournament URL """
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open the webpage
        driver.get(tournament_url)

        # Wait until the table is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-table__body'))
        )

        # Find the table body
        table_body = driver.find_element(By.CSS_SELECTOR, '.ui-table__body')

        # Find all rows in the table body
        rows = table_body.find_elements(By.CSS_SELECTOR, '.ui-table__row')

        all_data = []

        # Loop through each row and extract the data
        for row in rows:
            try:
                spans = row.find_elements(By.TAG_NAME, 'span')  # Store spans once
                divs = row.find_elements(By.TAG_NAME, 'div')    # Store divs once
                
                # Extract text from specific elements within the current row
                row_data = {
                    'Position': int(divs[1].text.split('.')[0]),
                    'TeamName': divs[3].text,
                    'Played': spans[0].text,
                    'W': spans[1].text,
                    'D': spans[2].text,
                    'L': spans[3].text,
                    'G scored': int(spans[4].text.split(':')[0]),
                    'G conceded': int(spans[4].text.split(':')[1]),
                    'GD': spans[5].text,
                    'Points': spans[6].text,
                }

                # Extract Last Matches dynamically
                num_spans = len(spans)

                for i in range(8, num_spans):
                    row_data[f'LastMatch{i - 7}'] = spans[i].text

                # Append the extracted row data to the list
                all_data.append(row_data)
            
            except Exception as e:
                print(f"Error processing row: {e}")

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(all_data)
        df.to_csv(os.getcwd() + os.sep+'standings.csv',index=False)
        return df
    
    finally:
        # Close the browser
        driver.quit()

def display_dataframe(dataframe):
    """ Function to display DataFrame in a new Tkinter window """
    df_window = tk.Toplevel(root)
    df_window.title("DataFrame Display")

    # Create a Treeview widget
    tree = ttk.Treeview(df_window)
    tree.pack(fill='both', expand=True)

    # Define columns
    tree["columns"] = list(dataframe.columns)
    tree["show"] = "headings"

    # Create columns with column names and set the column widths
    for column in dataframe.columns:
        tree.heading(column, text=column)
        tree.column(column, anchor='center', width=100)

    # Insert DataFrame rows into the Treeview
    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

def on_button_click():
    """ Function to be called when button is clicked """
    selected_tournament = dropdown_var.get()  # Get the selected tournament
    if selected_tournament in link_tournaments:
        tournament_url = link_tournaments[selected_tournament]
        df = scrape_data(tournament_url)  # Scrape data and create DataFrame
        display_dataframe(df)  # Display the DataFrame in a new window
    else:
        messagebox.showerror("Error", "Invalid Tournament Selected!")
        
def update_dropdown_menu():
    """ Function to update the dropdown menu options """
    menu = dropdown_menu["menu"]
    menu.delete(0, "end")
    for tournament in link_tournaments.keys():
        menu.add_command(label=tournament, command=tk._setit(dropdown_var, tournament))

# Create the main application window
root = tk.Tk()
root.title("Soccer Tournament Scraper")

# Set the window size
root.geometry('200x200')

# Use ttk style for a modern look
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TOptionMenu', font=('Helvetica', 12))

# Add a frame for better layout
frame = ttk.Frame(root, padding="20 20 20 20")
frame.pack(fill=tk.BOTH, expand=True)

# Center the frame in the window
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Add a label above the dropdown menu, centered
label = ttk.Label(frame, text="Select the tournament:")
label.pack(pady=(0, 10), anchor="center")

# Create a dropdown menu, centered
dropdown_var = tk.StringVar(root)
dropdown_var.set(list(link_tournaments.keys())[0])  # Set default value

dropdown_menu = ttk.OptionMenu(frame, dropdown_var, *link_tournaments.keys())
dropdown_menu.pack(pady=(0, 20), anchor="center")

# Create a button to start the scraping, centered
scrape_button = ttk.Button(frame, text="Download Table", command=on_button_click)
scrape_button.pack(pady=(0, 20), anchor="center")

# Update the dropdown menu if necessary
update_dropdown_menu()

# Start the GUI event loop
root.mainloop()

