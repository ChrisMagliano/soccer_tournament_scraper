#!/usr/bin/env python
# coding: utf-8

# # Import needed libraries

# In[1]:


import tkinter as tk
import logging
from tkinter import ttk, messagebox
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# # Functions
def scrape_data(tournament_url):
    """ Function to scrape data for a selected tournament URL """
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(tournament_url)

        # Wait until the table is loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="league-table"]/div[2]')))
        table_body = driver.find_element(By.XPATH, '//*[@id="league-table"]/div[2]')
        
        # Split the text into lines and process it
        lines = table_body.text.split('\n')
        indexes = [0, len(lines) - 1]
        for index in sorted(indexes, reverse=True):
            del lines[index]
        
        # Initialize an empty list to hold the data
        data = []

        # Parse the lines
        i = 0  # Start from the first team position
        while i < len(lines):
            # Extract position, team name, and stats
            if i + 2 < len(lines):
                position = lines[i].strip()  # Get position
                team = lines[i + 1].strip()  # Get team name
                stats = lines[i + 2].strip().split()  # Get stats as list

                # Append the combined row of data
                data.append([position, team] + stats)

                # Move to the next team's data (increment by 3 lines)
                i += 3
            else:
                print(f"Skipping incomplete data at line {i}")
                break

        # Define column names
        columns = ['Position', 'TeamName', 'Played', 'W', 'D', 'L', 'G scored', 'G conceded', 'GD', 'PTS']
        
        # Create the DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        # Convert numeric columns to integers
        numeric_columns = ['Position', 'Played', 'W', 'D', 'L', 'G scored', 'G conceded', 'GD', 'PTS']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
        df.to_csv(os.path.join(os.getcwd(), 'standings_livescore.csv'), index=False)
        return df
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        # Close the browser
        driver.quit()
# In[2]:


def scrape_data(tournament_url):
    """ Function to scrape data for a selected tournament URL """
    
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize WebDriver and scrape data
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(tournament_url)

        # Wait until the table is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="league-table"]/div[2]'))
        )
        table_body = driver.find_element(By.XPATH, '//*[@id="league-table"]/div[2]')

        # Split the text into lines and process it
        lines = table_body.text.split('\n')[1:-1]  # Skip the first and last lines directly
        
        # Initialize a list comprehension to collect data
        data = [
            [lines[i].strip(), lines[i + 1].strip()] + lines[i + 2].strip().split()
            for i in range(0, len(lines), 3) if i + 2 < len(lines)
        ]

        # Check if data was correctly parsed
        if not data:
            logging.warning("No data extracted from the page.")
            return None
        
        # Define column names
        columns = ['Position', 'TeamName', 'Played', 'W', 'D', 'L', 'G scored', 'G conceded', 'GD', 'PTS']
        
        # Create the DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        # Convert numeric columns to integers
        numeric_columns = ['Position', 'Played', 'W', 'D', 'L', 'G scored', 'G conceded', 'GD', 'PTS']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
        
        # Save DataFrame to CSV
        output_file = os.path.join(os.getcwd(), 'standings_livescore.csv')
        df.to_csv(output_file, index=False)
        logging.info(f"Data saved to {output_file}")
        
        return df
    
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return None
    
    finally:
        # Ensure the browser is closed
        try:
            driver.quit()
        except Exception as e:
            logging.error(f"Failed to close WebDriver: {e}")


# In[3]:


def on_button_click():
    """ Function to be called when button is clicked """
    selected_tournament = dropdown_var.get()  # Get the selected tournament
    if selected_tournament in link_tournaments:
        tournament_url = link_tournaments[selected_tournament]
        df = scrape_data(tournament_url)  # Scrape data and create DataFrame
        if df is not None:
            display_dataframe(df)  # Display the DataFrame in a new window
        else:
            messagebox.showerror("Error", "Failed to scrape the data!")
    else:
        messagebox.showerror("Error", "Invalid Tournament Selected!")

def update_dropdown_menu():
    """ Function to update the dropdown menu options """
    menu = dropdown_menu["menu"]
    menu.delete(0, "end")
    for tournament in link_tournaments.keys():
        menu.add_command(label=tournament, command=tk._setit(dropdown_var, tournament))
        
def on_closing():
    """Handle GUI window closing to ensure proper shutdown"""
    try:
        driver.quit()
    except:
        pass
    root.destroy()




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



# # Core script

# In the `webscrape_diretta_tutorial.ipynb` notebook we have seen how selenium allows to scrape the standings of tournaments by the [diretta.it](www.diretta.it) website.
# 
# In this notebook, we want to put that notebook in a Graphical User Interface by using the `Tkinter` package.
#  
# When the user launches the script, a GUI will appear with a dropdown menu and a label "Select the tournament:". This menu contains all the major soccer tournaments spread all over the world. Once a country has been chosen, it is sufficient to click the "Download data" to scrape data, visualize it on `Tkinter` and store it into the computer.

# In[4]:


# Path to your ChromeDriver executable
chromedriver_path = os.getcwd() + os.sep + 'chromedriver-win64\\chromedriver.exe'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if you don't need a GUI

# Set up the ChromeDriver service
service = Service(chromedriver_path)

#Definition of a link dictionary.
link_tournaments = {
    'Italy - Serie A': 'https://www.livescore.com/en/football/italy/serie-a/table/',
    'Italy - Serie B': 'https://www.livescore.com/en/football/italy/serie-b/table/',
    'England - Premier League': 'https://www.livescore.com/en/football/england/premier-league/table/',
    'Spain - La Liga': 'https://www.livescore.com/en/football/spain/laliga/table/',
    'Germany - Bundesliga': 'https://www.livescore.com/en/football/germany/bundesliga/table/',
    'France - Ligue 1': 'https://www.livescore.com/en/football/france/ligue-1/table/',
    'Portugal - Primeira Liga': 'https://www.livescore.com/en/football/portugal/primeira-liga/table/',
    'Netherlands - Eredivise': 'https://www.livescore.com/en/football/netherlands/eredivisie/table/',
    'Belgium - Jupiler League':'https://www.livescore.com/en/football/belgium/belgian-pro-league/table/',
    'Turkey - Super Lig': 'https://www.livescore.com/en/football/turkiye/super-lig/table/',
    'Argentina - Liga Profesional':'https://www.livescore.com/en/football/argentina/primera-division/table/',
    'Brasil - Serie A':'https://www.livescore.com/en/football/belgium/belgian-pro-league/table/',
    'Saudi Arabia - Saudi Professional League':'https://www.livescore.com/en/football/saudi-arabia/saudi-professional-league/table/',
    'Denmark - Superliga':'https://www.livescore.com/en/football/denmark/superliga/table/',
    'Ireland - Premier Division':'https://www.livescore.com/en/football/ireland/premier-division/table/',
    'Scotland - Premiership':'https://www.livescore.com/en/football/scotland/scotland-premiership/table/',
    'Switzerland - Super League':'https://www.livescore.com/en/football/switzerland/super-league/table/',
    'USA - MLS':'https://www.livescore.com/en/football/usa/major-league-soccer/table/'
}


# In[5]:


# Create the main application window
root = tk.Tk()
root.title("Soccer Tournament Scraper")

# Set the window size
root.geometry('200x150')

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

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI event loop
root.mainloop()


# In[ ]:




