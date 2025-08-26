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
RUN usermod -aG docker jenkins

# Create a script to fix Docker socket permissions
RUN echo '#!/bin/bash\n\
chown root:docker /var/run/docker.sock\n\
chmod 660 /var/run/docker.sock\n\
exec "$@"' > /usr/local/bin/fix-docker-socket.sh && \
    chmod +x /usr/local/bin/fix-docker-socket.sh

# Switch back to Jenkins user
USER jenkins

# Use tini as entrypoint and fix socket permissions
ENTRYPOINT ["/usr/local/bin/fix-docker-socket.sh"]
CMD ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]