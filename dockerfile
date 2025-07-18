FROM apache/airflow:2.8.1-python3.11

USER root

# Install Java and required Linux tools
RUN apt-get update && \
    apt-get install -y default-jdk procps && \
    echo "export JAVA_HOME=$(readlink -f /usr/bin/java | sed 's:/bin/java::')" >> /etc/profile

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Switch back to airflow user to install Python packages
USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
