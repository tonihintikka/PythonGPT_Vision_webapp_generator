# OpenAI Vision API Project

## Demo
![image](https://github.com/tonihintikka/PythonGPT_Vision_webapp_generator/assets/6028261/04712481-96ba-490c-8b04-35bb0beed039)

### source image
![image](https://github.com/tonihintikka/PythonGPT_Vision_webapp_generator/assets/6028261/ed3774d8-982a-4858-bb9a-06cf926c21e8)

### end result

[![demo about the created application](!(https://github.com/tonihintikka/PythonGPT_Vision_webapp_generator/assets/6028261/3c1237a0-fb85-4cd8-bfef-fc7106416da1)
)]((https://youtu.be/BLkM-TRjPzs))
https://github.com/tonihintikka/PythonGPT_Vision_webapp_generator/blob/main/demo/image.html


This project integrates OpenAI's GPT-4 Vision API to generate HTML/JavaScript code from images and descriptions.

## Installation

Ensure Python 3 and required packages (`requests`, `base64`, `configparser`, etc.) are installed.

```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `config.ini` file in the project root with your OpenAI API key:
   [DEFAULT]
   API_KEY = Your_OpenAI_API_Key

2. Place images in the `/data` directory.

## Usage

Run the script with the image filename as an argument:
python3 testvision.py /path/to/your/image.jpg

The script will:

- Encode the image.
- Send it to the OpenAI API.
- Save the generated HTML/JavaScript code in the `/data` directory with a timestamp.
- Print the generated code to the console.

## File Monitoring

The script continuously monitors the specified image file for changes and re-sends it to the API if modified.

## Notes

- The script handles conversation context for follow-up queries.
- Make sure the image path is correct and the API key is valid.
