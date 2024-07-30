import streamlit as st
from simple_salesforce import Salesforce, SFType
import json
from openai import OpenAI
import requests

# Salesforce credentials
SF_USERNAME = "your_salesforce_username"
SF_PASSWORD = "your_salesforce_password"
SF_SECURITY_TOKEN = "your_salesforce_security_token"

# OpenAI API key
OPENAI_API_KEY = st.secrets["openai_api_key"]

def connect_to_salesforce():
    try:
        sf = Salesforce(
            username = st.secrets["sf_username"],
            password = st.secrets["sf_password"],
            security_token = st.secrets["sf_security_token"],
            domain = st.secrets["sf_domain"]  # Use 'test' for sandbox
        )
        return sf
    except Exception as e:
        st.error(f"Failed to connect to Salesforce: {str(e)}")
        return None

def fetch_metadata(sf, metadata_type):
    try:
        sf_instance_url = 'https://canbsdo.my.salesforce.com'
        metadata_url = f'{sf_instance_url}/services/data/v52.0/tooling/query/?q=SELECT+Id,+Metadata+FROM+SecuritySettings'

        response = requests.get(
            metadata_url,
            headers={'Authorization': f'Bearer {sf.session_id}'}
        )

        if response.status_code == 200:
            security_settings = response.json()

            return security_settings;
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"Failed to fetch metadata: {str(e)}")
        return None

def analyze_metadata(metadata, metadata_type):
    # openai.api_key = OPENAI_API_KEY
    client = OpenAI(api_key=st.secrets["openai_api_key"])
    prompt = f"Analyze the following Salesforce {metadata_type} metadata and provide recommendations for improvement:\n\n{metadata}"

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful Salesforce system administrator and security expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message
    except Exception as e:
        st.error(f"Failed to analyze metadata: {str(e)}")
        return None

st.title("AI Security Scanner (beta)")
st.caption("This auto scan function uses generative AI to scan Salesforce metadata, identifying issues like code inefficiencies and security vulnerabilities. It provides tailored recommendations for remediation, enhancing performance and reliability. Users can interactively select metadata components and receive real-time insights for improved system optimization and security.")


sf = connect_to_salesforce()
if sf:
    st.success("Connected to metadata successfully!")

    metadata_types = ["SecuritySettings", "Profile", "PermissionSet", "Role"]
    selected_type = st.selectbox("Select metadata type", metadata_types)

    if st.button("Start Scan"):
        with st.spinner("Analysing metadata ..."):
            metadata = fetch_metadata(sf, selected_type)
            if metadata:
                st.subheader(f"{selected_type} Metadata")
                st.json(metadata, expanded= False)

                analysis = analyze_metadata(metadata, selected_type)
                st.subheader("OpenAI Analysis")
                st.write(analysis.content)
else:
    st.error("Failed to connect to Salesforce. Please check your credentials.")

# if __name__ == "__main__":
#     main()




# # import json
# import streamlit as st
# from openai import OpenAI

# from deepgram import (
#     DeepgramClient,
#     PrerecordedOptions,
#     FileSource,
# )

# def transcribe(uploaded_file):
#     try:
#         deepgram = DeepgramClient(st.secrets["deepgram_id"])

#         payload: FileSource = {
#             "buffer": uploaded_file.getvalue(),
#         }

#         options = PrerecordedOptions(
#             model="nova-2",
#             language="en",
#             summarize="v2", 
#             smart_format=True, 
#             diarize=True, 
#         )

#         response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
#         deepgramResult = response;
#         # deepgramResult = { "metadata": { "transaction_key": "deprecated", "request_id": "88ed10db-7897-46a5-903c-b122a637d9ef", "sha256": "abb0ca185f406e41a8200b8ec23cecec00e5a8044f17e6a9eded28540eeaf6f8", "created": "2024-07-22T05:55:35.076Z", "duration": 58.73, "channels": 1, "models": [ "30089e05-99d1-4376-b32e-c263170674af" ], "model_info": { "30089e05-99d1-4376-b32e-c263170674af": { "name": "2-general-nova", "version": "2024-01-09.29447", "arch": "nova-2" } }, "summary_info": { "input_tokens": 186, "output_tokens": 50, "model_uuid": "67875a7f-c9c4-48a0-aa55-5bdb8a91c34a" } }, "results": { "channels": [ { "alternatives": [ { "transcript": "What is your favorite character from the James and the Giant Peach? My favorite character is ladybird. Do you like ladybird? It's your turn. What is your favorite character? I I don't like the show. I don't like the book. Why? Because it's for kids. Well I would like to watch Star War. That doesn't make sense. Okay. That's it. I think you should watch it later. Unless I'm not sure you will like it. Okay. I'll give it a go. Bye bye. Bye.", "confidence": 0.9955413, "words": [ { "word": "what", "start": 2.1599998, "end": 2.56, "confidence": 0.99376607, "punctuated_word": "What", "speaker": 0, "speaker_confidence": 0.5019531 }, { "word": "is", "start": 2.56, "end": 2.72, "confidence": 0.99975556, "punctuated_word": "is", "speaker": 0, "speaker_confidence": 0.5019531 }, { "word": "your", "start": 2.72, "end": 3.04, "confidence": 0.99973565, "punctuated_word": "your", "speaker": 0, "speaker_confidence": 0.5019531 }, { "word": "favorite", "start": 3.04, "end": 3.54, "confidence": 0.9996519, "punctuated_word": "favorite", "speaker": 0, "speaker_confidence": 0.5019531 }, { "word": "character", "start": 3.6799998, "end": 4.18, "confidence": 0.99891376, "punctuated_word": "character", "speaker": 0, "speaker_confidence": 0.5019531 }, { "word": "from", "start": 5.3599997, "end": 5.8599997, "confidence": 0.99478674, "punctuated_word": "from", "speaker": 0, "speaker_confidence": 0.48388672 }, { "word": "the", "start": 6.48, "end": 6.64, "confidence": 0.48104936, "punctuated_word": "the", "speaker": 0, "speaker_confidence": 0.48388672 }, { "word": "james", "start": 6.64, "end": 6.96, "confidence": 0.98852134, "punctuated_word": "James", "speaker": 0, "speaker_confidence": 0.48388672 }, { "word": "and", "start": 6.96, "end": 7.12, "confidence": 0.9848081, "punctuated_word": "and", "speaker": 0, "speaker_confidence": 0.48388672 }, { "word": "the", "start": 7.12, "end": 7.2799997, "confidence": 0.983996, "punctuated_word": "the", "speaker": 0, "speaker_confidence": 0.48388672 }, { "word": "giant", "start": 7.2799997, "end": 7.7799997, "confidence": 0.7588355, "punctuated_word": "Giant", "speaker": 0, "speaker_confidence": 0.48388672 }, { "word": "peach", "start": 7.9199996, "end": 8.42, "confidence": 0.67191076, "punctuated_word": "Peach?", "speaker": 0, "speaker_confidence": 0.48388672 }, { "word": "my", "start": 8.804999, "end": 9.045, "confidence": 0.99183965, "punctuated_word": "My", "speaker": 1, "speaker_confidence": 0.51904297 }, { "word": "favorite", "start": 9.045, "end": 9.545, "confidence": 0.98768103, "punctuated_word": "favorite", "speaker": 1, "speaker_confidence": 0.51904297 }, { "word": "character", "start": 10.004999, "end": 10.325, "confidence": 0.994422, "punctuated_word": "character", "speaker": 1, "speaker_confidence": 0.51904297 }, { "word": "is", "start": 10.325, "end": 10.825, "confidence": 0.99860185, "punctuated_word": "is", "speaker": 1, "speaker_confidence": 0.51904297 }, { "word": "ladybird", "start": 12.724999, "end": 13.224999, "confidence": 0.7187136, "punctuated_word": "ladybird.", "speaker": 1, "speaker_confidence": 0.21972656 }, { "word": "do", "start": 15.125, "end": 15.365, "confidence": 0.6418298, "punctuated_word": "Do", "speaker": 0, "speaker_confidence": 0.2548828 }, { "word": "you", "start": 15.365, "end": 15.445, "confidence": 0.99635506, "punctuated_word": "you", "speaker": 0, "speaker_confidence": 0.2548828 }, { "word": "like", "start": 15.445, "end": 15.684999, "confidence": 0.9975768, "punctuated_word": "like", "speaker": 0, "speaker_confidence": 0.2548828 }, { "word": "ladybird", "start": 15.684999, "end": 16.185, "confidence": 0.98778987, "punctuated_word": "ladybird?", "speaker": 0, "speaker_confidence": 0.2548828 }, { "word": "it's", "start": 21.279999, "end": 21.52, "confidence": 0.78007644, "punctuated_word": "It's", "speaker": 1, "speaker_confidence": 0.28808594 }, { "word": "your", "start": 21.52, "end": 21.76, "confidence": 0.7648008, "punctuated_word": "your", "speaker": 1, "speaker_confidence": 0.28808594 }, { "word": "turn", "start": 21.76, "end": 22.0, "confidence": 0.9888787, "punctuated_word": "turn.", "speaker": 1, "speaker_confidence": 0.28808594 }, { "word": "what", "start": 22.0, "end": 22.24, "confidence": 0.9955413, "punctuated_word": "What", "speaker": 1, "speaker_confidence": 0.28808594 }, { "word": "is", "start": 22.24, "end": 22.4, "confidence": 0.9991604, "punctuated_word": "is", "speaker": 1, "speaker_confidence": 0.28808594 }, { "word": "your", "start": 22.4, "end": 22.56, "confidence": 0.99948776, "punctuated_word": "your", "speaker": 1, "speaker_confidence": 0.28808594 }, { "word": "favorite", "start": 22.56, "end": 22.96, "confidence": 0.99979097, "punctuated_word": "favorite", "speaker": 1, "speaker_confidence": 0.28808594 }, { "word": "character", "start": 22.96, "end": 23.46, "confidence": 0.9997407, "punctuated_word": "character?", "speaker": 1, "speaker_confidence": 0.28808594 }, { "word": "i", "start": 23.68, "end": 24.18, "confidence": 0.99423236, "punctuated_word": "I", "speaker": 0, "speaker_confidence": 0.13867188 }, { "word": "i", "start": 26.164999, "end": 26.404999, "confidence": 0.999877, "punctuated_word": "I", "speaker": 0, "speaker_confidence": 0.44970703 }, { "word": "don't", "start": 26.404999, "end": 26.725, "confidence": 0.99795043, "punctuated_word": "don't", "speaker": 0, "speaker_confidence": 0.44970703 }, { "word": "like", "start": 26.725, "end": 26.965, "confidence": 0.99983656, "punctuated_word": "like", "speaker": 0, "speaker_confidence": 0.44970703 }, { "word": "the", "start": 26.965, "end": 27.125, "confidence": 0.9425509, "punctuated_word": "the", "speaker": 0, "speaker_confidence": 0.44970703 }, { "word": "show", "start": 27.125, "end": 27.625, "confidence": 0.99852645, "punctuated_word": "show.", "speaker": 0, "speaker_confidence": 0.44970703 }, { "word": "i", "start": 27.925, "end": 28.085, "confidence": 0.99863976, "punctuated_word": "I", "speaker": 0, "speaker_confidence": 0.26708984 }, { "word": "don't", "start": 28.085, "end": 28.325, "confidence": 0.9997995, "punctuated_word": "don't", "speaker": 0, "speaker_confidence": 0.26708984 }, { "word": "like", "start": 28.325, "end": 28.564999, "confidence": 0.9998566, "punctuated_word": "like", "speaker": 0, "speaker_confidence": 0.26708984 }, { "word": "the", "start": 28.564999, "end": 28.725, "confidence": 0.99950993, "punctuated_word": "the", "speaker": 0, "speaker_confidence": 0.26708984 }, { "word": "book", "start": 28.725, "end": 29.225, "confidence": 0.9998039, "punctuated_word": "book.", "speaker": 0, "speaker_confidence": 0.26708984 }, { "word": "why", "start": 30.164999, "end": 30.664999, "confidence": 0.99989635, "punctuated_word": "Why?", "speaker": 1, "speaker_confidence": 0.28955078 }, { "word": "because", "start": 32.165, "end": 32.565, "confidence": 0.99959785, "punctuated_word": "Because", "speaker": 0, "speaker_confidence": 0.17333984 }, { "word": "it's", "start": 32.565, "end": 32.805, "confidence": 0.9998423, "punctuated_word": "it's", "speaker": 0, "speaker_confidence": 0.17333984 }, { "word": "for", "start": 32.805, "end": 33.045, "confidence": 0.9941486, "punctuated_word": "for", "speaker": 0, "speaker_confidence": 0.17333984 }, { "word": "kids", "start": 33.045, "end": 33.545, "confidence": 0.99944603, "punctuated_word": "kids.", "speaker": 0, "speaker_confidence": 0.17333984 }, { "word": "well", "start": 35.25, "end": 35.57, "confidence": 0.9975049, "punctuated_word": "Well", "speaker": 1, "speaker_confidence": 0.20019531 }, { "word": "i", "start": 35.89, "end": 36.13, "confidence": 0.9997398, "punctuated_word": "I", "speaker": 0, "speaker_confidence": 0.51416016 }, { "word": "would", "start": 36.13, "end": 36.29, "confidence": 0.99933356, "punctuated_word": "would", "speaker": 0, "speaker_confidence": 0.51416016 }, { "word": "like", "start": 36.29, "end": 36.53, "confidence": 0.9996985, "punctuated_word": "like", "speaker": 0, "speaker_confidence": 0.51416016 }, { "word": "to", "start": 36.53, "end": 37.03, "confidence": 0.99863523, "punctuated_word": "to", "speaker": 0, "speaker_confidence": 0.51416016 }, { "word": "watch", "start": 37.57, "end": 38.07, "confidence": 0.9989654, "punctuated_word": "watch", "speaker": 0, "speaker_confidence": 0.51416016 }, { "word": "star", "start": 38.37, "end": 38.77, "confidence": 0.90898836, "punctuated_word": "Star", "speaker": 0, "speaker_confidence": 0.51416016 }, { "word": "war", "start": 38.77, "end": 39.27, "confidence": 0.89751065, "punctuated_word": "War.", "speaker": 0, "speaker_confidence": 0.51416016 }, { "word": "that", "start": 40.21, "end": 40.61, "confidence": 0.9992244, "punctuated_word": "That", "speaker": 1, "speaker_confidence": 0.4814453 }, { "word": "doesn't", "start": 40.61, "end": 41.09, "confidence": 0.9980961, "punctuated_word": "doesn't", "speaker": 1, "speaker_confidence": 0.4814453 }, { "word": "make", "start": 41.09, "end": 41.41, "confidence": 0.9755123, "punctuated_word": "make", "speaker": 1, "speaker_confidence": 0.4814453 }, { "word": "sense", "start": 41.41, "end": 41.91, "confidence": 0.99916494, "punctuated_word": "sense.", "speaker": 1, "speaker_confidence": 0.4814453 }, { "word": "okay", "start": 42.715, "end": 43.215, "confidence": 0.99961066, "punctuated_word": "Okay.", "speaker": 0, "speaker_confidence": 0.26513672 }, { "word": "that's", "start": 43.355, "end": 43.515, "confidence": 0.9887495, "punctuated_word": "That's", "speaker": 0, "speaker_confidence": 0.26513672 }, { "word": "it", "start": 43.515, "end": 44.015, "confidence": 0.99364626, "punctuated_word": "it.", "speaker": 0, "speaker_confidence": 0.26513672 }, { "word": "i", "start": 44.235, "end": 44.315, "confidence": 0.999752, "punctuated_word": "I", "speaker": 1, "speaker_confidence": 0.47460938 }, { "word": "think", "start": 44.315, "end": 44.555, "confidence": 0.999861, "punctuated_word": "think", "speaker": 1, "speaker_confidence": 0.47460938 }, { "word": "you", "start": 44.555, "end": 44.635002, "confidence": 0.99506605, "punctuated_word": "you", "speaker": 1, "speaker_confidence": 0.47460938 }, { "word": "should", "start": 44.635002, "end": 44.955, "confidence": 0.9998242, "punctuated_word": "should", "speaker": 1, "speaker_confidence": 0.47460938 }, { "word": "watch", "start": 44.955, "end": 45.275, "confidence": 0.9952572, "punctuated_word": "watch", "speaker": 1, "speaker_confidence": 0.47460938 }, { "word": "it", "start": 45.275, "end": 45.595, "confidence": 0.99315876, "punctuated_word": "it", "speaker": 1, "speaker_confidence": 0.47460938 }, { "word": "later", "start": 45.595, "end": 46.095, "confidence": 0.9256414, "punctuated_word": "later.", "speaker": 1, "speaker_confidence": 0.47460938 }, { "word": "unless", "start": 47.915, "end": 48.415, "confidence": 0.9934248, "punctuated_word": "Unless", "speaker": 1, "speaker_confidence": 0.18554688 }, { "word": "i'm", "start": 50.91, "end": 51.23, "confidence": 0.88582134, "punctuated_word": "I'm", "speaker": 0, "speaker_confidence": 0.19433594 }, { "word": "not", "start": 51.23, "end": 51.31, "confidence": 0.6907201, "punctuated_word": "not", "speaker": 0, "speaker_confidence": 0.19433594 }, { "word": "sure", "start": 51.31, "end": 51.81, "confidence": 0.69481903, "punctuated_word": "sure", "speaker": 0, "speaker_confidence": 0.19433594 }, { "word": "you", "start": 52.27, "end": 52.43, "confidence": 0.85587895, "punctuated_word": "you", "speaker": 1, "speaker_confidence": 0.48339844 }, { "word": "will", "start": 52.43, "end": 52.670002, "confidence": 0.74841183, "punctuated_word": "will", "speaker": 1, "speaker_confidence": 0.48339844 }, { "word": "like", "start": 52.670002, "end": 52.91, "confidence": 0.9992193, "punctuated_word": "like", "speaker": 1, "speaker_confidence": 0.48339844 }, { "word": "it", "start": 52.91, "end": 53.41, "confidence": 0.9960742, "punctuated_word": "it.", "speaker": 1, "speaker_confidence": 0.48339844 }, { "word": "okay", "start": 53.47, "end": 53.97, "confidence": 0.9995591, "punctuated_word": "Okay.", "speaker": 0, "speaker_confidence": 0.45751953 }, { "word": "i'll", "start": 54.11, "end": 54.27, "confidence": 0.8809688, "punctuated_word": "I'll", "speaker": 0, "speaker_confidence": 0.45751953 }, { "word": "give", "start": 54.27, "end": 54.510002, "confidence": 0.97301537, "punctuated_word": "give", "speaker": 0, "speaker_confidence": 0.45751953 }, { "word": "it", "start": 54.510002, "end": 54.59, "confidence": 0.7255243, "punctuated_word": "it", "speaker": 0, "speaker_confidence": 0.45751953 }, { "word": "a", "start": 54.59, "end": 54.67, "confidence": 0.50758153, "punctuated_word": "a", "speaker": 0, "speaker_confidence": 0.45751953 }, { "word": "go", "start": 54.67, "end": 54.91, "confidence": 0.9953402, "punctuated_word": "go.", "speaker": 0, "speaker_confidence": 0.45751953 }, { "word": "bye", "start": 54.91, "end": 55.07, "confidence": 0.9993956, "punctuated_word": "Bye", "speaker": 0, "speaker_confidence": 0.45751953 }, { "word": "bye", "start": 55.07, "end": 55.57, "confidence": 0.99861395, "punctuated_word": "bye.", "speaker": 0, "speaker_confidence": 0.45751953 }, { "word": "bye", "start": 57.31, "end": 57.81, "confidence": 0.99461305, "punctuated_word": "Bye.", "speaker": 1, "speaker_confidence": 0.4248047 } ], "paragraphs": { "transcript": "\nSpeaker 0: What is your favorite character from the James and the Giant Peach?\n\nSpeaker 1: My favorite character is ladybird.\n\nSpeaker 0: Do you like ladybird?\n\nSpeaker 1: It's your turn. What is your favorite character?\n\nSpeaker 0: I I don't like the show. I don't like the book.\n\nSpeaker 1: Why?\n\nSpeaker 0: Because it's for kids.\n\nSpeaker 1: Well\n\nSpeaker 0: I would like to watch Star War.\n\nSpeaker 1: That doesn't make sense.\n\nSpeaker 0: Okay. That's it.\n\nSpeaker 1: I think you should watch it later. Unless\n\nSpeaker 0: I'm not sure\n\nSpeaker 1: you will like it.\n\nSpeaker 0: Okay. I'll give it a go. Bye bye.\n\nSpeaker 1: Bye.", "paragraphs": [ { "sentences": [ { "text": "What is your favorite character from the James and the Giant Peach?", "start": 2.1599998, "end": 8.42 } ], "start": 2.1599998, "end": 8.42, "num_words": 12, "speaker": 0 }, { "sentences": [ { "text": "My favorite character is ladybird.", "start": 8.804999, "end": 13.224999 } ], "start": 8.804999, "end": 13.224999, "num_words": 5, "speaker": 1 }, { "sentences": [ { "text": "Do you like ladybird?", "start": 15.125, "end": 16.185 } ], "start": 15.125, "end": 16.185, "num_words": 4, "speaker": 0 }, { "sentences": [ { "text": "It's your turn.", "start": 21.279999, "end": 22.0 }, { "text": "What is your favorite character?", "start": 22.0, "end": 23.46 } ], "start": 21.279999, "end": 23.46, "num_words": 8, "speaker": 1 }, { "sentences": [ { "text": "I I don't like the show.", "start": 23.68, "end": 27.625 }, { "text": "I don't like the book.", "start": 27.925, "end": 29.225 } ], "start": 23.68, "end": 29.225, "num_words": 11, "speaker": 0 }, { "sentences": [ { "text": "Why?", "start": 30.164999, "end": 30.664999 } ], "start": 30.164999, "end": 30.664999, "num_words": 1, "speaker": 1 }, { "sentences": [ { "text": "Because it's for kids.", "start": 32.165, "end": 33.545 } ], "start": 32.165, "end": 33.545, "num_words": 4, "speaker": 0 }, { "sentences": [ { "text": "Well", "start": 35.25, "end": 35.57 } ], "start": 35.25, "end": 35.57, "num_words": 1, "speaker": 1 }, { "sentences": [ { "text": "I would like to watch Star War.", "start": 35.89, "end": 39.27 } ], "start": 35.89, "end": 39.27, "num_words": 7, "speaker": 0 }, { "sentences": [ { "text": "That doesn't make sense.", "start": 40.21, "end": 41.91 } ], "start": 40.21, "end": 41.91, "num_words": 4, "speaker": 1 }, { "sentences": [ { "text": "Okay.", "start": 42.715, "end": 43.215 }, { "text": "That's it.", "start": 43.355, "end": 44.015 } ], "start": 42.715, "end": 44.015, "num_words": 3, "speaker": 0 }, { "sentences": [ { "text": "I think you should watch it later.", "start": 44.235, "end": 46.095 }, { "text": "Unless", "start": 47.915, "end": 48.415 } ], "start": 44.235, "end": 48.415, "num_words": 8, "speaker": 1 }, { "sentences": [ { "text": "I'm not sure", "start": 50.91, "end": 51.81 } ], "start": 50.91, "end": 51.81, "num_words": 3, "speaker": 0 }, { "sentences": [ { "text": "you will like it.", "start": 52.27, "end": 53.41 } ], "start": 52.27, "end": 53.41, "num_words": 4, "speaker": 1 }, { "sentences": [ { "text": "Okay.", "start": 53.47, "end": 53.97 }, { "text": "I'll give it a go.", "start": 54.11, "end": 54.91 }, { "text": "Bye bye.", "start": 54.91, "end": 55.57 } ], "start": 53.47, "end": 55.57, "num_words": 8, "speaker": 0 }, { "sentences": [ { "text": "Bye.", "start": 57.31, "end": 57.81 } ], "start": 57.31, "end": 57.81, "num_words": 1, "speaker": 1 } ] } } ] } ], "summary": { "result": "success", "short": "Speaker 1 asks Speaker 0 about their favorite character from the James and the Giant Peach show, but Speaker 1 doesn't like the show and doesn't like the book. They ultimately decide to watch a Star War after realizing they didn't like the book." } } }
#         # STEP 4: Print the response
#         st.subheader("Transcript:")
#         transcript = deepgramResult['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']
#         st.write(transcript)
        
#         st.subheader("Meting Summary:")
#         summary = deepgramResult['results']['summary']['short']
#         st.write(summary)

#         actions = get_actions(transcript, summary)
#         display_actions(actions)
        
        
#         # st.subheader("Action items:")
#         # st.write(actions)       
#     except Exception as e:
#         print(f"Exception: {e}")

# def get_actions(transcript, summary):

#     client = OpenAI(api_key=st.secrets["openai_api_key"])

#     prompt = f"""Analyze the following meeting transcript and summary, then provide action items:

#             Transcript: {transcript}
#             Summary: {summary}

#             Generate a JSON object with a single key 'action_items' containing an array of action items. Each action item should be a string. The JSON object should be the only output. For example:

#             {{
#                 "action_items": [
#                     "Schedule follow-up meeting with marketing team",
#                     "Review Q3 budget proposal",
#                     "Send project timeline to stakeholders"
#                 ]
#             }}
#             """

#     try:
#         completion = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are a helpful meeting note taker and analyst"},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         content_str = completion.choices[0].message.content
#         content_json = json.loads(content_str)
#         action_items = content_json['action_items']

#         return action_items
#     except Exception as e:
#         st.error(f"Failed to analyze metadata: {str(e)}")
#         return None
    

# def display_actions(action_items):
#     st.subheader("Action Items:")
#     for item in action_items:
#         st.write("• " + item)

# # Main Streamlit app
# def main():
#     st.logo('images/mario.png', icon_image='images/mario.png')
#     st.title("Meeting Transcription and Summary")
#     uploaded_file = st.file_uploader("Upload your meeting recording", type=["mp3", "wav", "m4a", "mp4"])
    
#     if uploaded_file is not None:
#         transcribe(uploaded_file)

# if __name__ == "__main__":
#     main()


