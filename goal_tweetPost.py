import requests
from requests_oauthlib import OAuth1
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#add credentials
API_KEY = ''
API_SECRET_KEY = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

def create_tweet(text):

    url = "https://api.twitter.com/2/tweets"

    auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    payload = {
        "text": text
    }

    response = requests.post(url, auth=auth, json=payload)

    if response.status_code == 201:
        print("Tweet posted successfully!")
        print("Response:", response.json())
    else:
        print(f"Failed to post tweet: {response.status_code}")
        print("Response:", response.json())

def check_goal(match_url):
    driver.get(match_url)
    driver.minimize_window()
    time.sleep(5)

    previous_events = set()

    while True:
        try:
            board = driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant')
            events = driver.find_elements(By.CSS_SELECTOR,
                                          'div.smv__participantRow')

            current_events = set([event.text for event in events])

            #check for new events
            new_events = current_events - previous_events

            #find only the goal events, (the goal events ex: Messi (1-0)) the hint for goal events is -
            goal_events = []

            for event in new_events:
                if '-' in event:
                    goal_events.append(event)
            print(f'Goal events: {goal_events}')
            if goal_events:
                for event in goal_events:
                    print(f"New event: {event}")
                    lines = event.split('\n')
                    player_name = lines[2]
                    create_tweet(f'Gooaaaaal by: {player_name}')
                    print(f'Gooaaaaal by: {player_name}')

            previous_events = current_events
        except Exception as e:
            print(f"Error: {e}")

        #check if the match ended or its half time
        if "Final" in board.text:
            break
        #if half time pause for 15 minutes
        elif "Pauză" in board.text:
            time.sleep(900)

        #check every 15 seconds
        time.sleep(15)

if __name__ == "__main__":
    tweet_text = "GOOAAAAL by"
    url='https://www.flashscore.ro/meci/na927pNt/#/sumar-meci/sumar-meci'
    check_goal(url)
