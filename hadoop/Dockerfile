FROM ubuntu:latest

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV HIVE_HOME=/opt/hive
ENV HIVE_CONF_DIR=/opt/hive/conf
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin:$HIVE_HOME/bin

RUN apt update
RUN apt upgrade -y  # --fix-missing
RUN apt install openjdk-8-jdk -y
RUN apt install wget -y
RUN apt install ssh -y
RUN apt install sudo -y

RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz && \
    tar zxvf hadoop-3.4.1.tar.gz && \
    mv hadoop-3.4.1 ${HADOOP_HOME} && \
    rm hadoop-3.4.1.tar.gz

RUN wget https://archive.apache.org/dist/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz && \
    tar zxvf apache-hive-3.1.3-bin.tar.gz && \
    mv apache-hive-3.1.3-bin ${HIVE_HOME} && \
    rm apache-hive-3.1.3-bin.tar.gz

RUN wget https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/9.3.0/mysql-connector-j-9.3.0.jar && \
    mv mysql-connector-j-9.3.0.jar ${HIVE_HOME}/lib

#hadoop setting
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh && \
    echo "export YARN_RESOURCEMANAGER_USER=root" >> ${HADOOP_HOME}/etc/hadoop/yarn-env.sh && \
    echo "export YARN_NODEMANAGER_USER=root" >> ${HADOOP_HOME}/etc/hadoop/yarn-env.sh && \
    echo "export HDFS_DATANODE_USER=root" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_NAMENODE_USER=root" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_SECONDARYNAMENODE_USER=root" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

COPY hadoop_conf/core-site.xml ${HADOOP_HOME}/etc/hadoop/core-site.xml
COPY hadoop_conf/hdfs-site.xml ${HADOOP_HOME}/etc/hadoop/hdfs-site.xml
COPY hadoop_conf/yarn-site.xml ${HADOOP_HOME}/etc/hadoop/yarn-site.xml
RUN chmod +r ${HADOOP_HOME}/etc/hadoop/core-site.xml && \
    chmod +r ${HADOOP_HOME}/etc/hadoop/hdfs-site.xml && \
    chmod +r ${HADOOP_HOME}/etc/hadoop/yarn-site.xml

EXPOSE 8088 9870 9864 19888 8042 8888

#hive setting
COPY hive_conf/hive-site.xml ${HIVE_HOME}/conf/hive-site.xml
COPY hive_conf/hive-env.sh ${HIVE_HOME}/conf/hive-env.sh
RUN chmod +r ${HIVE_HOME}/conf/hive-site.xml && \
    chmod +xr ${HIVE_HOME}/conf/hive-env.sh
RUN mkdir ${HIVE_HOME}/logs

EXPOSE 9083 10000 10002

RUN rm ${HIVE_HOME}/lib/guava-*.jar && \
    cp ${HADOOP_HOME}/share/hadoop/common/lib/guava-*.jar ${HIVE_HOME}/lib/
COPY entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]
CMD ["bash"]
