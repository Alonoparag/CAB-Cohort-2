from kafka import KafkaClient, KafkaProducer
import json,requests

# Creating Kafka client
kafka = KafkaClient(bootstrap_servers='localhost:9092')

#Creating a Kafka producer instance
meetup_producer = KafkaProducer(bootstrap_servers='localhost:9092')

r = requests.get("https://stream.meetup.com/2/rsvps",stream=True)

# Sending messages to Consumer.
for line in r.iter_lines():
    meetup_producer.send('meetup',value=line)
    obj = json.loads(line.decode('utf-8'))
## printing the cities on console
    rsvps= (obj['group']['group_city'])
    print(rsvps)

kafka.close()
