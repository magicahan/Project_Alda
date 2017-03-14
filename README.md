# Project ALDA

CAPP 30122: Computer Science with Applications-2

The University of Chicago | Winter 2017

## About this repository:
This repository contains the final course project for CAPP 30122. 

## About all sub-directories:
* <code>AldaCourse</code>: contains all individual components of Project ALDA 
listed below together with a Django interface.

* <code>CourseCrawler</code>: contains all scripts necessary to complete the 
tasks of logging in to <my.uchicago.edu> and scrapping all course informations.

* <code>CourseEvaluation</code>: contains all scripts necessary to scrap 
course evalations.

* <code>NLTK</code>: contains python scripts used to select the top 6 positive
 and negative words from each evaluation comments.

* <code>ScheduleVisualization</code>: contains python scripts and 
template.xlms file used to create all possible combinations of non-conflict 
courses schedules based on user input. 

* <code>Project_Info</code>: contains project description files and 
the presentation slides.

## Packages that we used:
* Selenium (v3.3.1)
* PhantomJS (v2.1)
* Openpyxl (v2.4.5)
* Django (v1.10.6)

## How to use our program:
* 1. Open your terminal and direct to the directory called **Project_ALDA**
* 2. In your terminal, type in <code>sh alda_prep.sh</code>. 
    + After typing in this line of code, you might be asked to input your 
      password.
    + After inputting your password, it would start to install all required
      packages so as to ensure Project ALDA would run successfully and 
      smoothly.
* 3. **Open a new terminal**, and type in <code>sh alda_init.sh</code>. It 
     would automatically open your default web browser and you will see our 
     interface, powered by Django, in front of you. 
* 4. Lay back, relax, and lets fly! 

## Contributors
**Alice Mee Seon Chung** [Alicechung](https://github.com/Alicechung)

**Luxi Luke Han** [magicahan](https://github.com/magicahan)

**Dongping Gabriel Zhang** [dpzhang](https://github.com/dpzhang)

**Ningyin Ariel Xu** [sixisxu](https://github.com/sixisxu)

We would like to express our sincere gratitude to **Dr. Matthew Wachs** and 
**Dr. Amitabh Chaudhary** for your teaching, guidance, and support throughout the
quarter.
