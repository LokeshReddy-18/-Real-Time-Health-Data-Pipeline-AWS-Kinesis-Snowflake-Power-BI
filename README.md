# Real-Time Health Data Pipeline | AWS Kinesis, Snowflake, Power BI

This project demonstrates a real-time data pipeline for processing and analyzing smartwatch data, including metrics such as step count, blood pressure (BP), heartbeat, and glucose rate. The pipeline processes over 500,000 records per day, leveraging AWS services to enable real-time ingestion, transformation, storage, and visualization of health data.

![Screenshot 2024-09-21 at 9 10 59 PM](https://github.com/user-attachments/assets/fcc9b126-14df-4047-b866-d0ab619ed533)


## Table of Contents

* Project Overview       
* Architecture
* Features
* Tech Stack
* Contributing
* License

## Project Overview
This project simulates real-time smartwatch data, processes it using AWS Kinesis, transforms the data with AWS Lambda, and stores it in an S3 Data Lake. The data is further loaded into Snowflake for warehousing, and Power BI is used for real-time health trend visualizations.

## Architecture
* Python Simulation: Python is used to simulate smartwatch data records such as step count, BP, heartbeat, and glucose rate.
* AWS Kinesis Firehose: The simulated data is streamed in real-time to AWS Kinesis Firehose.
* AWS Lambda: Lambda functions transform and enrich the data.
* S3 Data Lake: The processed data is stored in an AWS S3 bucket for long-term storage.
* Snowflake: Data is loaded into Snowflake using Snowpipe for warehousing and analysis.
* Power BI: Data is visualized in Power BI to provide real-time insights into health metrics.

## Features
Real-Time Ingestion: Processes over 500,000 smartwatch records per day with a latency of under 10 seconds.
Automated Data Loading: Uses Snowpipe and Snowflake external stages for continuous data ingestion and transformation.
Interactive Visualizations: Power BI dashboards provide up-to-date health analytics and trends.

## Tech Stack
AWS Kinesis Firehose for real-time data streaming
AWS Lambda for data transformation and enrichment
AWS S3 for data storage
Snowflake for data warehousing
Power BI for visualization
Python for simulating smartwatch data

## Visualization

This project integrates with Power BI to visualize key health metrics such as:
* Step count
* Blood pressure
* Heartbeat
* Glucose rate
The interactive dashboards help track health trends and make data-driven decisions.
![Screenshot 2024-09-21 at 3 41 43 PM](https://github.com/user-attachments/assets/9eec3ec2-415c-4722-a932-ef149aefa374)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
