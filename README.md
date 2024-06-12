<div align="center">

# GLUE: Recommendation Service

* GLUE 서비스의 Recommendation Service project에 대해 소개합니다*

[![Static Badge](https://img.shields.io/badge/language-english-red)](./README.md) [![Static Badge](https://img.shields.io/badge/language-korean-blue)](./README-KR.md) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FSinging-voice-conversion%2Fsingtome-model&count_bg=%23E3E30F&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

</div>

<br>

GLUE 서비스의 Recommend Service에 방문해주셔서 감사합니다. 해당 Repository는 GLUE 서비스의 추천 CRUD기능을 포함한 내용을 담고 있습니다. 
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
| <a href="https://github.com/leejuae"><img src="https://avatars.githubusercontent.com/u/51390115?v=4" height="120px"></a> | 이주애 <br> **jeri**| Restful API with Fast API with Elastic Search|

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

- **Languages**: Python
- **Libraries and Frameworks**: 
- **Tools**: vsCode

> schemas

DTO
