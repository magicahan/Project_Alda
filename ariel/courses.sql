CREATE TABLE courses
   (courseid VARCHAR(30),
   coursenumber VARCHAR(15),
   career VARCHAR(30),
   condition VARCHAR(10),
   daytime VARCHAR(50),
   description VARCHAR(5000),
   instructor VARCHAR(100),
   location VARCHAR(50),
   name VARCHAR(100),
   section VARCHAR(5),
   sectionid VARCHAR(10),
   subsections VARCHAR(5000),
   coursetype VARCHAR(5));
.import course_output.csv courses