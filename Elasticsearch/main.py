from kafka_cosumer import ElasticSearchKafkaConsumer
import logging

def main():
    with open('Logs/elk.log', mode="w") as file:
        file.write("\n") # erase the log file
    logging.basicConfig(filename='Logs/elk.log', level=logging.INFO)
    consumer = ElasticSearchKafkaConsumer()
    consumer.getMessages()

if __name__ == "__main__":
    main()