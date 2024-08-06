# Digikala Comments Sentiment Analysis

This project focuses on building a sentiment analysis system for user comments on the Digikala website. The system classifies comments into three categories: positive, neutral, and negative.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Data Collection](#data-collection)
- [Model Training](#model-training)
- [Interactive Dashboard](#interactive-dashboard)

## Overview
The aim of this project is to scrape user comments from the Digikala website, preprocess the data, convert text to numeric vectors using pre-trained models like ParsBERT, fine-tune the model for sentiment classification, and finally, present the results through an interactive dashboard.

## Features
- **Web Scraping**: Scrape comments, user names, and ratings from Digikala.
- **Data Preprocessing**: Clean and normalize text data.
- **Text Embedding**: Convert text into numeric vectors using ParsBERT.
- **Model Fine-Tuning**: Fine-tune the ParsBERT model for sentiment analysis.
- **Visualization**: Display results using interactive charts and dashboards.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/digikala-sentiment-analysis.git
    cd digikala-sentiment-analysis
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the web scraper:
    - Navigate to the `digikala-crawler` directory and follow the instructions in `digikala_spider.py` to start scraping data.

## Data Collection
The data collection is done using a custom Scrapy spider (`digikala_spider.py`) that scrapes comments, ratings, and sentiments from the Digikala website.

## Model Training

The model training process involves fine-tuning the ParsBERT model on the preprocessed Digikala comments data. Please follow these steps to train the model:

1. **Preprocess the Data**:
   - Ensure that you have preprocessed the data using the provided notebook or script. The preprocessed data should be saved as `preprocessed_data.csv`.

2. **Fine-Tune the ParsBERT Model**:
   - Use the provided code in the notebook to fine-tune the ParsBERT model. The fine-tuning process will involve training the model on the preprocessed data and saving the fine-tuned model in the `dashboard/saved_model` directory.
   
   - Due to the large size of the trained model (625 MB), the model is not included in this repository. You will need to train the model yourself using the provided code.

3. **Save the Fine-Tuned Model**:
   - Once the model is trained, save it to the `dashboard/saved_model` directory. This saved model will be used in the Streamlit dashboard for sentiment analysis.

## Interactive Dashboard
An interactive dashboard is built using Streamlit to visualize the sentiment analysis results. The dashboard allows users to:
- View the dataset.
- Input custom text to predict sentiment.
- Visualize sentiment distribution.

To run the dashboard:
```bash
cd dashboard
streamlit run streamlit_dashboard.py


