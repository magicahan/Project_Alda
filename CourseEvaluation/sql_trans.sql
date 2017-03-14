CREATE TABLE course
	(course_num varchar(50),
	course_id int,
	course_title varchar(100),
	dept varchar(50)
);
.import course_table.csv course
.separator |


CREATE TABLE instructor
	(last_name varchar(50),
	first_name varchar(50),
	instructor_id int,
	dept varchar(50)
);
.import instructor_table.csv instructor

CREATE TABLE ins_class
	(instructor_id int,
	course_id int,
	year int,
	class_section int,
	quarter int
);
.import link_table.csv ins_class

CREATE TABLE ins_score_detail
	(course_id int,
	year int,s
	class_section int,
	quarter int,
	instructor_id int,
	score_term varchar(100),
	avg_score float,
	num_response float
);
.import instructor_score.csv ins_score_detail
DELETE FROM ins_score_detail WHERE avg_score = 'No score';

CREATE TABLE ins_avgscore
	(course_id int,
	year int,
	class_section int,
	quarter int,
	instructor_id int,
	avg_score float,
	num_response float
);
.import instructor_avgscore.csv ins_avgscore
DELETE FROM ins_avgscore WHERE avg_score = 'No score';
ALTER TABLE ins_avgscore ADD tot_score float;
UPDATE ins_avgscore SET tot_score = avg_score * num_response;

.output score_combine.csv
SELECT b.dept, b.last_name, b.first_name, b.instructor_id, SUM(c.num_response) AS num_response, SUM(c.avg_score * c.num_response) / SUM(c.num_response) AS avg_score
FROM ins_avgscore AS c JOIN course AS a ON(a.course_id = c.course_id) JOIN instructor AS b ON(c.instructor_id = b.instructor_id)
GROUP BY c.instructor_id;
.output stdout

.output score_combine_course.csv
SELECT a.course_num, a.course_id, a.course_title, a.dept, b.last_name, b.first_name, b.instructor_id, SUM(c.num_response) AS num_response, SUM(c.avg_score * c.num_response) / SUM(c.num_response) AS avg_score
FROM ins_avgscore AS c JOIN course AS a ON(a.course_id = c.course_id) JOIN instructor AS b ON(c.instructor_id = b.instructor_id)
GROUP BY c.instructor_id, c.course_id;
.output stdout
