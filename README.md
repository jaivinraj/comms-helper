# Comms helper 🏗️ <!-- omit in toc -->

NOTE: this project is a WIP but you can still run the dashboard to see what it looks like using the quick start guide below.

- [1. What is this for?](#1-what-is-this-for)
- [2. How to use this repo ❓](#2-how-to-use-this-repo-)
- [3. ToDo](#3-todo)

## 1. What is this for?

This app aims to give a flavour of what's going on in the Twittersphere around a particular issue or topic.


## 2. How to use this repo ❓

1. Install Docker [here](https://docs.docker.com/get-docker/) (if you don't already have it) 
2. In the terminal, run `docker-compose up -d` (Note: if a new version has been released, you may need to rebuild the image. This can be done using `docker-compose build --no-cache`)
3. Once the container has built (you can check using `docker ps`), bash into it using `docker exec -it comms-helper /bin/bash`
4. Inside the container, run the dashboard using `python src/comms_helper/dashboard/main.py`
5. Follow the link to http://0.0.0.0:8050/ and you can access the dashboard
## 3. ToDo

- [x] Create scraper
- [x] Create database
- [x] Create initial dashboard
  - [ ] Sentiment analysis
  - [ ] Topic analysis
  - [ ] Network analysis
  - [x] Time series
  - [x] Wordcloud