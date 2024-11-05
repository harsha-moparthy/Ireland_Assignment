# Project Title: Global Weather Data Dashboard

## Project Description
This project involves building a comprehensive web application to display and update global weather data. The application is divided into two main sections:

1. **Data Dashboard**: This section displays the cleaned global weather dataset with various filters such as date, region, and other relevant metrics.
2. **Live Data Updates**: This section shows live weather updates being streamed via Kafka, with a real-time plot of the data points.

## Technologies Used
- **Flask**: Used to build a REST API that serves the cleaned data and streams updated global weather data via Kafka.
- **Streamlit**: Used to build the web application that interacts with the Flask API.
- **Kafka**: Used for streaming live weather updates.

## Deployment
The Streamlit app is deployed on the free Streamlit cloud platform. You can access the hosted app using the following link:

[Hosted Streamlit App](#)

## How to Run the Project Locally

   **Clone the repository**

  **Install the required dependencies**
  ```sh 
  pip install -r requirements.txt
  ```
  **Run the Flask API server**
  ```sh
  sudo systemctl start kafka
  sudo systemctl start zookeeper
  sudo /opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
  sudo /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties
  ```
  If the kafka folder is in /opt/kafka you require sudo else you can run without sudo and respective folder
  **Run the Streamlit app**
  ```sh
  python kafka_producer.py --country India
  python server.py
  streamlit run streamlit/app.py
  ```
    You can change the country by passing the argument to kafka_producer.py
## Repository Structure
- `server.py`: Contains the Flask API code.
- `streamlit/app.py`: Contains the Streamlit web application code.
- `kafka_producer.py`: Contains the kafka producer code.
- `weather.csv`: Contains the cleaned global weather dataset.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, please contact [Your Name] at [Your Email].
