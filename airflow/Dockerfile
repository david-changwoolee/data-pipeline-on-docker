FROM ubuntu:latest

ENV AIRFLOW_HOME=/opt/airflow
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt upgrade -y --fix-missing
RUN apt install python3 -y 
RUN apt install python3-pip -y
RUN apt install pkg-config -y
RUN pip3 install apache-airflow==2.11.0 --break-system-packages
RUN pip3 install pymysql --break-system-packages
RUN pip install apache-airflow-providers-apache-spark --break-system-packages
#RUN pip3 install psycopg2-binary --break-system-packages
#RUN pip3 install asyncpg --break-system-packages

COPY conf/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY conf/entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh

ENTRYPOINT ["/root/entrypoint.sh"]
#CMD ["bash"]

ENV HADOOP_HOME=/opt/hadoop

RUN apt install openjdk-8-jdk -y
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

RUN apt install wget -y
ENV SPARK_HOME=/opt/spark
RUN wget https://dlcdn.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz && \
    tar zxvf spark-3.5.5-bin-hadoop3.tgz && \
    mv spark-3.5.5-bin-hadoop3 ${SPARK_HOME}
RUN rm spark-3.5.5-bin-hadoop3.tgz
RUN pip3 install virtualenv --break-system-packages

ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV YARN_CONF_DIR=/opt/hadoop/etc/hadoop
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin:$JAVA_HOME/bin

EXPOSE 8082
