import os
import base64
import requests
import prompts
import configparser
import sys
import time
import http.server
import socketserver
import threading


config = configparser.ConfigParser()
config.read('config.ini')

# Check if 'DEFAULT' and 'API_KEY' exist copy the config.ini_ as config.ini in same folder and name it to config.ini
if 'DEFAULT' in config and 'API_KEY' in config['DEFAULT']:
    api_key = config['DEFAULT']['API_KEY']
else:
    raise ValueError("API_KEY not found in the configuration file.")
# Function to encode the image

conversation_id = None  # To store the ID for follow-up context


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to send the image to the API


def save_conversation_id(conversation_id, image_name):
    with open(f"data/{image_name}_conversation_id.txt", "w") as file:
        file.write(conversation_id)


def load_conversation_id(image_name):
    try:
        with open(f"data/{image_name}_conversation_id.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def send_image(image_path, follow_up=False):
    global conversation_id
    base64_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
# Form the payload with the nested structure for the image
    user_content = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "high"
            }
        },
        {
            "type": "text",
            "text": prompts.OPENAI_USER_PROMPT if not follow_up else prompts.OPENAI_USER_PROMPT_WITH_PREVIOUS_DESIGN
        }
    ]

    # Form the payload
    messages = [
        {
            "role": "system",
            "content": prompts.OPEN_AI_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_content
        }
    ]

    if follow_up and conversation_id:
        # Include the conversation ID to maintain the context
        messages.append({
            "role": "system",
            "content": f"session: {conversation_id}"
        })

    payload = {
        "model": "gpt-4-vision-preview",
        "max_tokens": 4096,
        "temperature": 0,
        "messages": messages
    }
    print("Sending API call...")  # Indicate that the API call is being sent
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()
    print("API call sent, processing response...")
    if response.status_code == 200:
        print("API call successful.")
        # Extract the HTML content from the response
        html_content = response_data['choices'][0]['message']['content']

        # Ensure the /data directory exists
        data_directory = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_directory, exist_ok=True)

        # Create the output file name based on the input file name
        input_filename_without_extension = os.path.splitext(
            os.path.basename(image_path))[0]
        output_filename = f"{input_filename_without_extension}.html"
        html_file_path = os.path.join(data_directory, output_filename)

        # Save the HTML content to the file
        with open(html_file_path, 'w') as file:
            file.write(html_content)

        print(f"HTML content saved to {html_file_path}")
        # Save the new ID for future follow-ups
        conversation_id = response_data.get('id')
        # Save the ID based on image name
        save_conversation_id(conversation_id, image_name)
    else:
        print("Failed to call API.")
        print("Response:", response_data)


"""
# Path to your image
image_path = "image.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "max_tokens": 4096,
    "messages": [
        {
            "role": "system",
            "content": prompts.OPEN_AI_SYSTEM_PROMPT  # System prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    }
                },
                {
                    "type": "text",
                    "text": prompts.OPENAI_USER_PROMPT  # User prompt
                },
                # Additional text messages can be added here as needed
            ]
        }
    ]
}







#response = requests.post(
#    "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

#print(response.json())
"""


def file_has_changed(filepath, last_modified_time):
    return os.path.getmtime(filepath) > last_modified_time


def poll_file(file_path, interval=1):
    last_modified_time = os.path.getmtime(file_path)

    while True:
        try:
            if file_has_changed(file_path, last_modified_time):
                print(f"File {file_path} has changed.")
                send_image(file_path, follow_up=True)
                last_modified_time = os.path.getmtime(file_path)

            time.sleep(interval)
        except KeyboardInterrupt:
            print("File polling stopped.")
            break
        except FileNotFoundError:
            print(f"File {file_path} not found. Retrying...")
            time.sleep(interval)


if __name__ == '__main__':
    image_path = sys.argv[1]
    image_name, _ = os.path.splitext(os.path.basename(image_path))

    conversation_id = load_conversation_id(image_name)
    # Use existing context if available
    send_image(image_path, follow_up=bool(conversation_id))
    poll_file(image_path)  # Start polling the file for changes
