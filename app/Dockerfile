# Get python base image
FROM python:3.9.1

# User setup
RUN groupadd -g 1000 www && useradd -r -u 1000 -g www www

# Add app dir and change own
RUN mkdir /app && chown www:www /app

# Copy config
COPY / /app/

# Determine the workdir
WORKDIR /app

# Install requirements
RUN pip install -r requirements.txt

# Determina listening port
EXPOSE 5000

# Change user
USER www

# Determine the entrypoint
ENTRYPOINT [ "python" ]

# Determine CMD for default
CMD [ "app.py" ]