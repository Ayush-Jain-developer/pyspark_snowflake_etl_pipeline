# Stage 1: Build Stage
FROM python:3.10-buster AS builder

# Set working directory
WORKDIR /app

# Install Java, Hadoop, and other build dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Spark and Hadoop
ENV SPARK_VERSION=3.5.4
ENV HADOOP_VERSION=3
RUN wget https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /usr/local \
    && mv /usr/local/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /usr/local/spark \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Set Spark and Hadoop environment variables
ENV SPARK_HOME=/usr/local/spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin:$JAVA_HOME/bin

# Copy the application code
COPY ./pyspark_redshift_etl_pipeline pyproject.toml /app

# Install Python dependencies using Poetry
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Stage 2: Final Stage
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install minimal dependencies
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# Copy Java, Spark, and application from the builder stage
COPY --from=builder /usr/lib/jvm/java-11-openjdk-amd64 /usr/lib/jvm/java-11-openjdk-amd64
COPY --from=builder /etc/java-11-openjdk /etc/java-11-openjdk
COPY --from=builder /usr/local/spark /usr/local/spark
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

RUN mkdir -p /root/.conf/kaggle
COPY kaggle.json /root/.config/kaggle/kaggle.json
RUN chmod 600 /root/.config/kaggle/kaggle.json

# Set environment variables for Java, Spark, and Hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$JAVA_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin

ENTRYPOINT ["spark-submit", "--conf","spark.executor.memory=6g", "--conf", "spark.executor.cores=6", "local:///app/main.py"]




