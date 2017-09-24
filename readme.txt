#Log_analysis

1.Install Vagrant and vrtual machine .
2.Place the downloaded 'newsdata.sql' in the vagrant directory .
3.Open git bash terminal .
4.Change directory to the downloaded FSND-Virtual-Machine/vagrant/ using cd command . 
5.use vagrant up and then vagrant ssh(to log in to your virtual machine) .
6.change the directory to vagrant/ .
7.load the database using the command 'psql -d news -f newsdata.sql' .
8.Use 'psql -d news' to connect to database 'news' .
9.Create view v1 using :
  
    create view v1 as select title, views from articles,
    (select path as path, count(*) as views from log where status = '200 OK' group by path) as log 
    where log.path like concat('%',articles.slug) order by views desc;
	
10.then run python3 index.py .
11.index_output.txt conatins the output .
