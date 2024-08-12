# WA ChatBot for Recipe Management

## Tools Required
- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/)

## Usage
### WA Web
#### Install Dependencies
From the root of the project
```bash
cd wweb
npm install
```
It will install all the dependencies in node_modules folder.
#### Start Bot
```bash
npm run start
```
Then, you can link your WhatsApp account by scanning 
the QR code.
### Rasa
#### Setup Rasa
```bash
pip3 install rasa
```
Rasa will installed globally.
#### Add Virtual Environment
```bash
# create virtual environment
python3 -m venv ./rasa/venv
# activate virtual environment
./venv/Scripts/activate
```
#### Run Rasa Core Server
From the root of the project
```bash
cd rasa
rasa run --enable-api
```
#### Run  Rasa Actions Server
```bash
rasa run actions
```

Thats it.