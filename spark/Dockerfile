FROM ubuntu:latest

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop

RUN apt update
RUN apt upgrade -y --fix-missing
RUN apt install openjdk-8-jdk -y
RUN apt install wget -y
RUN apt install ssh -y
RUN wget https://dlcdn.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz && \
    tar zxvf spark-3.5.5-bin-hadoop3.tgz && \
    mv spark-3.5.5-bin-hadoop3 ${SPARK_HOME}
RUN rm spark-3.5.5-bin-hadoop3.tgz

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin:$JAVA_HOME/bin

ENV YARN_CONF_DIR=/opt/hadoop/etc/hadoop

EXPOSE 8080 8081 18080 4040 7077 9000

RUN apt install python3 -y
RUN apt install python3-pip -y --fix-missing ; pip3 install jupyter --break-system-package
ENV PYTHONPATH=$PYTHONPATH:$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip

RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-hive_2.12/3.5.5/spark-hive_2.12-3.5.5.jar && \
    mv spark-hive_2.12-3.5.5.jar ${SPARK_HOME}/jars

RUN mkdir /tmp/spark-events

WORKDIR /root/jupyter
CMD ["jupyter", "notebook", "--allow-root", "--port", "9000", "--ip", "0.0.0.0"]
