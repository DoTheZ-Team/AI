<div align="center">

# GLUE: Recommendation Service

* GLUE 서비스의 Recommendation Service project에 대해 소개합니다*

[![Static Badge](https://img.shields.io/badge/language-english-red)](./README.md) [![Static Badge](https://img.shields.io/badge/language-korean-blue)](./README-KR.md) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FSinging-voice-conversion%2Fsingtome-model&count_bg=%23E3E30F&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

</div>

<br>

GLUE 서비스의 Post Service에 방문해주셔서 감사합니다. 해당 Repository는 GLUE 서비스의 게시글 CRUD기능을 포함한 검색 쿼리에 대한 내용을 담고 있습니다. 
(#). 
<br>

<div align="center">

</div>

## Contents
1. [Members](#1-members)
2. [Introduction](#2-introduction)
3. [Swagger Page](#3-screen-planning-figma)
4. [Screen Composition](#4-screen-composition)
5. [Used Languages, Libraries, Frameworks, Tools](#5-used-languages-libraries-frameworks-tools)

## 1. Members
| Profile | Name | Role |
| :---: | :---: | :---: |
| <a href="https://github.com/anselmo228"><img src="https://avatars.githubusercontent.com/u/24919880?v=4" height="120px"></a> | 정희찬 <br> **anselmo**| Restful API with Spring Boot with GCP and Elastic Search|

## **2. Introduction**

The Sing-To-Me website is a platform where you can create new songs by overlaying different voices onto original tracks. Users can upload various voice files to train models, and then choose original songs and trained voices to blend together, creating new vocal combinations. Key features include:

- User login and management
- Uploading voice files and training models
- Blending original songs with trained voices to synthesize new songs
- Song playback
- Providing a Top100 list of popular songs

## **3. Swagger Page**

- **Voice API*: Controlls every request against Voice List(Create, Read, Modify, Delete)
- **AI Cover Song API*: Controlls every request against Voice List(Create, Read, Modify, Delete) and Checking if the RVC model is running or not.


## **4. Screen Composition**

### **4.1 Folder Structure**

The project's folder structure is as follows:
According to MVC pattern of Spring boot. We folderized every contents in to Model, Controllers and Service.
Each domain has own Model Contollers and Services.

## **5. Used Languages, Libraries, Frameworks, Tools**

The languages, libraries, frameworks, and tools used in the project are as follows:

- **Languages**: Java, Spring, SQL 
- **Libraries and Frameworks**: 
- **Tools**: Intellij


# AI

> glue 서비스의 AI service 부분

```
fast api가 첨이라 파일 구조가 엉망입니다,,
```

### 서비스 종류
- 유저 추천 서비스
- 스티커 생성 서비스

### 더미데이터
사용자 해시태그 데이터
해당 데이터 몽고디비에 먼저 올린 후 추천은 진행하였습니다.

### secrets.json
딱히 시크릿하진 않지만 참고 자료에서 이렇게 처리하길래 따라했습니다.
현재는 로컬 환경에서 만들어놔서 이렇게 처리하였ㅅ브니다.
아래 코드로 해당 json 파일 만들어주시고 내부 요소들은 각자 로컬 DB에 맞게 설정해주셔야 합니다.
```
{
    "MONGO_DB_NAME":"kea",
    "MONGO_DB_URL":"localhost:27017"
}
```

### 내가 까먹을까봐 적는 파일구조
[참고링크](https://taptorestart.tistory.com/entry/FastAPI-디렉터리-구조를-어떻게-하는-게-좋을까)

> api

말그대로 api를 정의하는 부분
controller와 비슷한 역할

> core

공통파일

> db

데이터베이스 관련 설정 파일

> models

Entity

> schemas

DTO
