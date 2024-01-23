import requests
import os
import json
import logging
import time

# Setting up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def download_image(image_url, referencia, folder='images'):
    """
    Downloads an image from the given URL and saves it to the specified folder.
    """
    try:
        # Create folder for the images
        image_folder = os.path.join(folder, referencia)

        # Check if the images folder exists, if not, create it
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        # Extracting image name from URL
        image_name = image_url.split('/')[-1]

        # Full path for the image to be saved
        image_path = os.path.join(image_folder, image_name)

        # Downloading and saving the image
        response = requests.get(image_url)
        response.raise_for_status()

        with open(image_path, 'wb') as file:
            file.write(response.content)

        logging.info(f"Image saved: {image_path}")
        return image_path

    except Exception as e:
        logging.error(f"Error downloading image {image_url}: {e}")
        return None

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

        # Load JSON data
        json_data = response.json()
        json_data_items = json_data["item"]


        # Process and download images
        base_url = "https://www.e-leiloes.pt/api/"
        if "fotos" in json_data_items:
            for photo in json_data_items["fotos"]:
                image_url = base_url + photo["image"]
                download_image(image_url, referencia)

        logging.info(f"Successfully saved data for referencia {referencia}")
    except Exception as e:
        logging.error(f"Error fetching data for referencia {referencia}: {e}")

def main():    
    try:
        rows_per_page = 12
        initial_url = 'https://www.e-leiloes.pt/api/Eventos/?tableParams=%7B%22first%22%3A0%2C%22rows%22%3A12%2C%22sortField%22%3A%22dataFim%22%2C%22sortOrder%22%3A1%2C%22filters%22%3A%7B%22tipo%22%3A%7B%22value%22%3A1%2C%22matchMode%22%3A%22equals%22%7D%2C%22distrito%22%3A%7B%22value%22%3A%22Lisboa%22%2C%22matchMode%22%3A%22equals%22%7D%7D%7D'

        response = requests.get(initial_url)
        response.raise_for_status()
        data = response.json()

        total_items = data['pagination']['total']

        for index in range(0, total_items, rows_per_page):
            paginated_url = f'https://www.e-leiloes.pt/api/Eventos/?tableParams=%7B%22first%22%3A{index}%2C%22rows%22%3A{rows_per_page}%2C%22sortField%22%3A%22dataFim%22%2C%22sortOrder%22%3A1%2C%22filters%22%3A%7B%22tipo%22%3A%7B%22value%22%3A1%2C%22matchMode%22%3A%22equals%22%7D%2C%22distrito%22%3A%7B%22value%22%3A%22Lisboa%22%2C%22matchMode%22%3A%22equals%22%7D%7D%7D'
            paginated_response = requests.get(paginated_url)
            paginated_response.raise_for_status()

            paginated_data = paginated_response.json()
            for item in paginated_data['list']:
                fetch_and_save_json(item['referencia'])
                time.sleep(2)  # Sleep for 2 seconds between requests

            logging.info(f"Processed page with start index {index}")
        
        rows_per_page = 12
        initial_url = f'https://www.e-leiloes.pt/api/Eventos/?tableParams=%7B%22first%22%3A0%2C%22rows%22%3A12%2C%22sortField%22%3A%22dataFim%22%2C%22sortOrder%22%3A1%2C%22filters%22%3A%7B%22tipo%22%3A%7B%22value%22%3A1%2C%22matchMode%22%3A%22equals%22%7D%2C%22distrito%22%3A%7B%22value%22%3A%22Set%C3%BAbal%22%2C%22matchMode%22%3A%22equals%22%7D%7D%7D'

        response = requests.get(initial_url)
        response.raise_for_status()
        data = response.json()

        total_items = data['pagination']['total']

        for index in range(0, total_items, rows_per_page):
            paginated_url = f'https://www.e-leiloes.pt/api/Eventos/?tableParams=%7B%22first%22%3A{index}%2C%22rows%22%3A{rows_per_page}%2C%22sortField%22%3A%22dataFim%22%2C%22sortOrder%22%3A1%2C%22filters%22%3A%7B%22tipo%22%3A%7B%22value%22%3A1%2C%22matchMode%22%3A%22equals%22%7D%2C%22distrito%22%3A%7B%22value%22%3A%22Set%C3%BAbal%22%2C%22matchMode%22%3A%22equals%22%7D%7D%7D'
            paginated_response = requests.get(paginated_url)
            paginated_response.raise_for_status()

            paginated_data = paginated_response.json()
            for item in paginated_data['list']:
                fetch_and_save_json(item['referencia'])
                time.sleep(2)  # Sleep for 2 seconds between requests

            logging.info(f"Processed page with start index {index}")

    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()