# Dashboard
# Setup Environment - Shell/Terminal

mkdir Submission
cd Submission

mkdir Dashboard
cd Dashboard

pipenv install
pipenv shell

pip install -r ../requirements.txt


# Run streamlit app

streamlit run dashboard.py
