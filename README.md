# Weather Data Analysis Project

This project involves analyzing weather data collected from different locations (Dubai, Lahore, Murree) using Python and Pandas. The objective is to preprocess the data, and generate various reports.

## Overview

The project utilizes weather data provided in separate text files organized within folders for each location. The data is loaded into Pandas DataFrames, preprocessed, and analyzed to extract meaningful insights and statistics.

## Key Steps and Techniques

### 1. Data Collection and Integration

- Loaded weather data from text files stored in folders corresponding to different locations (Dubai, Lahore, Murree).
- Created a unified Pandas DataFrame by combining data from all locations and adding a (location) column to identify the source location of each record.

### 2. Data Preprocessing
- Dropped Unnecessary columns that were not relevant to the report and analysis
- Created a separate column for time zones(PKT, GST , PKST).
- Handled missing values by imputing mean values and removed rows with significant null values to ensure data quality.

### 3. Data Analysis and Reporting

- **Yearly Weather Statistics**:
  - Identified highest and lowest temperatures recorded in a given year.
  - Determined the most humid day and corresponding humidity percentage.

- **Monthly Weather Averages**:
  - Calculated average highest temperature, lowest temperature, and humidity for specified months and years.

- **Visualization of Daily Temperatures**:
  - Generated horizontal bar charts to visualize daily highest and lowest temperatures for specific months.

## Usage

To replicate the analysis or modify the code for different datasets:

1. Ensure Python and required libraries (e.g., Pandas) are installed.
2. Download the weather data files and organize them in a similar folder structure.
3. Use the provided Python script to load, preprocess, and analyze the weather data.
4. Modify the script to customize analysis tasks or adapt it for different datasets or locations.

## Requirements

- Python 3.x
- Pandas library (pip install pandas)

