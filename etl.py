# documentacao oficial site para concelhos: https://api.adviceslip.com/#endpoint-random

import pandas as pd
import requests
import json

df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()

# print(user_ids)

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for user_id in user_ids if (user := get_user(user_id)) is not None]

def generate_ai_advice(user):
  response = requests.get(f'https://api.adviceslip.com/advice')

  if response.status_code != 200:
    return None
  return response.json()['slip']['advice']

for user in users:
  news = generate_ai_advice(user)
  print(news)
  user['news'].append({
    "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
    "description": news
  })

def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}")