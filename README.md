# ReLevel ReSearch functionality
ReSearch is a basic search functionality which that achieves following objectives:
1. It takes in multiple paragraphs of text
2. Assigns a unique ID To each paragraph
3. Stores the words to paragraph mappings on an inverted index. (This is similar to what elasticsearch does.
   This paragraph can also be referred to as a ‘document’)
5. Given a word to search for, it lists out the top 10 paragraphs in which the word is 
present

### ReSearch Endpoint: **https://research-relevel.herokuapp.com/search/**

## Run the Test Cases:
**$python -m unittest**

## Steps to :runner:run the code:
1. Create a virtual environment using virtualenv or venv
2. Activate the virtual environment
3. Install packages from ***requirements.txt***: **$pip install -r requirements.txt**
4. Start the server: **$python manage.py runserver**

##### If you are running locally then add "127.0.0.0" to ALLOWED_HOSTS in the ***settings.py*** file.**
