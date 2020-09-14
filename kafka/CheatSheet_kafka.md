#### Kafka commands

```
bin/kafka-server-start.sh config/server.properties
bin/kafka-server-stop.sh config/server.properties
```

```
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

##### Create a topic
```
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1  --partitions 1 --topic uTopic
```

##### List of all the topics
```
kafka-topics.sh --list --zookeeper localhost:2181
```

#### Start kafka-producer service
```
kafka-console-producer.sh --broker-list localhost:9092 --topic uTopic
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic uTopic \
			  --from-beginning --property print.timestamp=true
```

#### Alter topic
```
bin/kafka-topics.sh —zookeeper localhost:2181 --alter --topic topic_name --partitions count
```

#### Delete topic
```
bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic topic_name
```

#### Print consumer topic based on timestamp
```
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic uTopic --from-beginning --property print.timestamp=true --property print.key=true | awk -F $'\t' 'BEGIN {OFS = FS} {if ($1 ~ /^CreateTime.*/) {a=substr($1, 12, length($1)-14); cmd = "date -d @"a" +%F-%H:%M:%S"; cmd | getline dat; close(cmd); $1=""} else {dat = ""}; print dat $0}'
```

```
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic uTopic --from-beginning --property print.timestamp=true | awk -F $'\t' 'BEGIN {OFS = FS} {if ($1 ~ /^CreateTime.*/) {a=substr($1, 12, length($1)-14); cmd = "date -d @"a" +%F-%H:%M:%S"; cmd | getline dat; close(cmd); $1=""} else {dat = ""}; print dat $0}'
```

#### Debug, capture packets
```
tcpdump -n -v -i eno1 dst port 9092
```
