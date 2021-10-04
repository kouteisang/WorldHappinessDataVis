#!/bin/bash
FROM python:3.9
WORKDIR /app
RUN pip3 install pandas
RUN pip3 install dash
RUN pip3 install dash-html-components
RUN pip3 install dash-core-components
RUN pip3 install dash-table
RUN pip3 install statsmodels

COPY . .
EXPOSE 8080
ENTRYPOINT [ "python3" ]
CMD ["main.py"]