FROM python:3.8.10
WORKDIR /web_influencer_analysis
COPY requrements.txt requrements.txt
RUN pip3 install requrements.txt
COPY . .