# 🏆 Soccer Tournament Scraper: Web Scraping Project for diretta.it

## Table of Contents
- [Project Overview](#project-overview)
- [Project goals](#project-goals)
- [Features](#features)
- [Tools](#tools)
- [Project structure](#project-structure)
- [How it works](#how-it-works)
- [User Interface](#user-interface)
- [Error Handling and Robustness](#error-handling-and-robustness)
- [Future Enhancements](#future-enhancements)

### Project Overview
This project is a web scraping tool developed using Python's Selenium library to extract soccer tournament standings from [diretta.it](https://www.diretta.it/preferiti/), a popular website for live soccer scores and statistics. The tool enables users to select a specific tournament, such as the Premier League, Serie A, or La Liga, and automatically scrape the latest standings data for the selected tournament.

### 🎯Project Goals
The main goal of this project is to create a reliable and efficient tool that allows users to:

- Automatically access and scrape soccer tournament standings from diretta.it;
- View the scraped data in a neatly formatted table within the application;
- Export the data for further analysis, reporting, or integration into other projects.
 
### 🚀Features
- **Dynamic Web Scraping**: Utilizes `selenium` to handle JavaScript-heavy content, ensuring that the most accurate and up-to-date data is captured.
- **User-Friendly GUI**: Built with `Tkinter` to allow users to easily select a tournament and view the corresponding standings in a table format.
- **Data Export**: Provides functionality to export the scraped data into a CSV file for further analysis or record-keeping.
- **Real-Time Data**: Scrapes live and dynamically loaded content from the diretta.it website, ensuring that the data is current.
- **Error Handling**: Robust error handling mechanisms to manage potential issues during scraping, such as missing elements or network interruptions.

### 🔨Tools

- [**Python**](https://www.python.org/): The primary programming language for scripting and automation;
- [**Selenium**](https://selenium-python.readthedocs.io/): A powerful web scraping library used to interact with web pages and extract data dynamically;
- [**Tkinter**](https://docs.python.org/3/library/tkinter.html): A standard Python interface to the Tk GUI toolkit, used to create a simple and intuitive user interface;
- [**Pandas**](https://pandas.pydata.org/docs/index.html): A data manipulation library used to structure and format scraped data for easy analysis and export;
- **ChromeDriver**: A WebDriver used to automate and control Chrome browsers.


### 📚Project Structure
The project is organized into the following structure:

```plaintext
soccer_tournament_scraper/
│
├── README.md                                      # Project description and instructions
├── requirements.txt                               # Required libraries and dependencies
├── webscrape_diretta_tutorial.ipynb               # A jupyter notebook to illustrate how the core script works
├── webscrape_diretta_gui.ipynb                    # A jupyter notebook to illustrate how the GUI core script works
├── webscrape.py                                   # Script to launch the Tkinter GUI
├── standings.csv                                  # Example of exported CSV file        
├── chromedriver-win64/                            # Directory containing ChromeDriver executable
 │   └── chromedriver.exe                          # ChromeDriver executable
 │   └── LICENSE.chromedriver                      
 │   └── THIRD_PARTY_NOTICES.chromedriver          
```
**Warning** the chromedriver.exe is compatible with 128.0.6613.85 (64 bit) Chrome version. To properly run the script on your machine please assure this chromedriver.exe is compatible with your Chrome version. If not give a look at the following [webpage](https://getwebdriver.com/).

### 📋How It Works
1. **Initialize WebDriver**: The project uses Selenium with ChromeDriver to open a Chrome browser session and navigate to the selected tournament page on diretta.it;
2. **Navigate to Tournament Page**: Once the tournament is selected via the GUI, Selenium directs the browser to the appropriate URL;
3. **Scrape Standings Data**: Selenium locates the standings table on the webpage and extracts relevant information, such as team positions, points, wins, losses, draws, goals scored and conceded, and recent match results;
4. **Display Data in GUI**: The scraped data is displayed in a table format within the Tkinter GUI, allowing users to view the data directly in the application;
5. **Export Data to CSV**: Users can export the scraped data to a .csv file for further use. This functionality is particularly useful for analysts and enthusiasts who want to work with the data offline or integrate it into other tools.

### 💻User Interface
The GUI is built using `Tkinter` and provides a simple interface for users to interact with:
- `Dropdown Menu`: Allows users to select the tournament they are interested in;
- `Scrape and Export Button`: Triggers the scraping process, displays the results in the GUI and automatically download the scraped data to a .csv file.

### Error Handling and Robustness
The scraper is equipped with several error-handling features to ensure smooth operation:
- **Element Locating Errors**: Try-except blocks are used to manage exceptions if specific elements are not found on the page.
- **Network Issues**: The scraper includes retries and timeout handling to manage network-related issues.
- **Dynamic Content Handling**: Selenium waits for content to load dynamically, ensuring that JavaScript-rendered elements are fully loaded before attempting to scrape.

### 📈Future Enhancements
- **Add More Leagues**: Extend the tool to scrape additional leagues or sports available on diretta.it.
- **Advanced Data Analysis**: Integrate additional Python libraries (e.g., Matplotlib, Seaborn) to provide visual data analysis directly in the GUI.
- **User Authentication**: Add features to handle user logins and save personalized settings.
