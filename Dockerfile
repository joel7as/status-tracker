FROM python:3.11-slim

# Install Apache and mod_wsgi
RUN apt-get update && apt-get install -y apache2 apache2-dev libapache2-mod-wsgi-py3 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Apache config
COPY docker/apache-flask.conf /etc/apache2/sites-available/000-default.conf

# Link logs to stdout
RUN ln -sf /dev/stdout /var/log/apache2/access.log \
 && ln -sf /dev/stderr /var/log/apache2/error.log

EXPOSE 80

# Create logs directory and give ownership to www-data
RUN mkdir -p /app/logs && chown -R www-data:www-data /app/logs

CMD ["apache2ctl", "-D", "FOREGROUND"]
