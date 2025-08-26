# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install prerequisites and Docker
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# Add Jenkins user to the Docker group (create if it doesn't exist)
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Create the Docker socket directory and set proper permissions
RUN mkdir -p /var/run && \
    touch /var/run/docker.sock && \
    chmod 666 /var/run/docker.sock && \
    chown root:docker /var/run/docker.sock

# Create the Docker directory and volume for DinD
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to the Jenkins user
USER jenkins