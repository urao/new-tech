FROM centos:centos7
MAINTAINER urao

# Install required pkgs
RUN yum update -y && \
    yum install -y \
    java-1.8.0-openjdk \
    wget \
    net-tools \
    tcpdump \
    wireshark && \
    yum clean all

# Copy required shell scripts
COPY pre_flight.sh /tmp/
RUN /tmp/pre_flight.sh

ARG SCALA_VERSION=1.00
ARG KAFKA_VERSION=1.0.0

# Download and install Kafka 
RUN curl -v -o /tmp/kafka_${SCALA_VERSION}_${KAFKA_VERSION}.tgz "http://apache.mirrors.pair.com/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" && \
    su -l kafka && cd /home/kafka/kafka && tar -xzvf /tmp/kafka_${SCALA_VERSION}_${KAFKA_VERSION}.tgz --strip 1

# metadata
EXPOSE 9092

CMD tail -f /dev/null
