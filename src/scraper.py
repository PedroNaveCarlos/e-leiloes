import requests
import os
import json
import logging
import time

# Setting up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_save_json(referencia, folder='json_responses'):
    try:
        url = f'https://www.e-leiloes.pt/api/Eventos/{referencia}'
        response = requests.get(url)
        response.raise_for_status()

        # Ensure folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save JSON response to file
        with open(os.path.join(folder, f'{referencia}.json'), 'w') as file:
            json.dump(response.json(), file, indent=4)

        logging.info(f"Successfully saved data for referencia {referencia}")
    except Exception as e:
        logging.error(f"Error fetching data for referencia {referencia}: {e}")

def main():
    try:
        # Fetch all auctions from Lisbon
        for index in range(0, 204, 12):
            initial_url = f'https://www.e-leiloes.pt/api/Eventos/?tableParams=%7B%22first%22%3A{index}%2C%22rows%22%3A12%2C%22sortField%22%3A%22dataFim%22%2C%22sortOrder%22%3A1%2C%22filters%22%3A%7B%22tipo%22%3A%7B%22value%22%3A1%2C%22matchMode%22%3A%22equals%22%7D%2C%22distrito%22%3A%7B%22value%22%3A%22Lisboa%22%2C%22matchMode%22%3A%22equals%22%7D%7D%7D'
            response = requests.get(initial_url)
            response.raise_for_status()

            data = response.json()
            for item in data['list']:
                fetch_and_save_json(item['referencia'])
                time.sleep(2)  # Sleep for 2 seconds between requests

            logging.info(f"Processed page with start index {index}")

    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()