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

 # Add Jenkins user to the Docker group
 RUN groupadd -f docker && \
     usermod -aG docker jenkins

# Create entrypoint to chown/chmod the socket at container start
RUN printf '%s\n' \
'#!/bin/bash' \
'chown root:docker /var/run/docker.sock' \
'chmod 660 /var/run/docker.sock' \
'exec "$@"' > /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

 # Create the Docker directory and volume for DinD
 RUN mkdir -p /var/lib/docker
 VOLUME /var/lib/docker

 # Switch back to Jenkins user
 USER jenkins

# Override entrypoint so permissions are fixed before Jenkins starts
 ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
 CMD ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]
