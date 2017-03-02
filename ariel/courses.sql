CREATE TABLE courses
   (coursenumber VARCHAR(10),
   career VARCHAR(50),
   condition VARCHAR(10),
   daytime VARCHAR(50),
   description VARCHAR(1000),
   instructor VARCHAR(30),
   location VARCHAR(100),
   name VARCHAR(30),
   section VARCHAR(10),
   sectionid VARCHAR(10),
   subsections VARCHAR(100),
   type VARCHAR(10));
.import course_output_sql.csv courses