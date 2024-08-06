import streamlit as st
import pandas as pd
from transformers import BertForSequenceClassification, AutoTokenizer
import torch
import plotly.express as px

# Load preprocessed data and model
df = pd.read_csv('preprocessed_data.csv')
model = BertForSequenceClassification.from_pretrained('saved_model')
tokenizer = AutoTokenizer.from_pretrained('saved_model')

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    return predictions.item()


st.title("Sentiment Analysis Dashboard")
st.sidebar.header("Input Text for Sentiment Analysis")
input_text = st.sidebar.text_area("Enter text here", "")

if input_text:
    sentiment = predict_sentiment(input_text)
    st.sidebar.write(f"Predicted Sentiment: {sentiment}")

# Display the dataset
st.header("Sentiment Analysis of Digikala Comments")
st.write(df)

fig = px.histogram(df, x='label', title='Sentiment Analysis of Digikala Comments')
st.plotly_chart(fig)

st.header("Model Metrics")
accuracy = df['label'].value_counts(normalize=True)
st.write(f"Accuracy: {accuracy.max() * 100:.2f}%")


if __name__ == '__main__':
    st.run()
