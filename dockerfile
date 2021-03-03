FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout app.log \
	&& ln -sf /dev/stderr app.log

CMD [ "python", "./main.py" ]