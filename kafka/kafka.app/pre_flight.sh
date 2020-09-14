#!/bin/bash
# Preconfigure before Kafka installation

echo "create kafka user"
username="kafka"
passwd="kafka"
useradd -p "$passwd" -d /home/"$username" -s /bin/bash -G wheel "$username"

echo "create directory"
su -l kafka && mkdir /home/kafka/kafka

exit 0
