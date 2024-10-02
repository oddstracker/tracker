import pytesseract
from PIL import Image
import os
import requests

# Tesseract OCR setup
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define folder for screenshots
screenshot_folder = r'C:\Users\luigi\Downloads\TT Odds Tracker\screenshots'

# Function to extract match data from screenshots
def extract_match_data():
    match_data = []
    for filename in os.listdir(screenshot_folder):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            file_path = os.path.join(screenshot_folder, filename)
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)

            # Extract relevant data like player names and odds from text
            players, odds, match_time, tournament = parse_text(text)
            
            # Store the extracted information for API query
            match_data.append({
                'players': players,
                'odds': odds,
                'match_time': match_time,
                'tournament': tournament
            })
    return match_data

# Function to parse text extracted by OCR
def parse_text(text):
    # Dummy function: you need to implement this based on the patterns in your text
    players = ['Player A', 'Player B']  # Example extraction of player names
    odds = '-120'  # Example of extracting opening odds
    match_time = '2023-10-02T12:00:00Z'  # Example match time in ISO 8601 format
    tournament = 'TT Elite Series'  # Example of extracting tournament name
    return players, odds, match_time, tournament

# Function to get the match result from Sportradar API
def get_winner_from_sportradar(players, match_time):
    # Your Sportradar API endpoint (replace with actual endpoint)
    url = "https://api.sportradar.com/table-tennis/matches/{match_id}/results.json"
    
    # Use players and match_time to query Sportradar and find the correct match
    # This is an example; you'll need to find the right API call for Sportradar
    params = {
        'api_key': '90hMRhlFnA5lKGA41bb3d7tYyjJJGA3kO8XSGKqa',
        'player1': players[0],
        'player2': players[1],
        'match_time': match_time
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        match_data = response.json()
        # Extract the winner from the API response
        winner = match_data['results']['winner']
        return winner
    else:
        return None

import streamlit as st

def display_data(match_data):
    # Create collapsible tabs for each tournament
    tournaments = ['TT Elite Series', 'TT Cup', 'Czech Liga Pro']
    
    for tournament in tournaments:
        with st.expander(tournament):
            for hour in range(24):
                st.write(f"Matches for hour: {hour}")
                for match in match_data:
                    if match['tournament'] == tournament and int(match['match_time'].split('T')[1][:2]) == hour:
                        st.write(f"{match['players'][0]} vs {match['players'][1]}")
                        st.write(f"Opening Odds: {match['odds']}")
                        st.write(f"Winner: {match['winner']}")
                        st.write(f"Category: {match['category']}")
                        st.write("---")

