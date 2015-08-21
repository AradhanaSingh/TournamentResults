# TournamentResults
Full Stack Web Developer Nanodegree Udacity Project

Steps to run this project

1. Install Virtual Box 

2. Install vagrant

3. Install git

4. Open Command prompt

5. Clone git repo, this creates folder fullstack folder in current directory

    git clone http://github.com/udacity/fullstack-nanodegree-vm fullstack
    
6. Go to vagrant folder

    cd fullstack/vagrant

7. To launch virtual machine

    vagrant up

8. To log into vagrant machine

    vagrant ssh
    
9. Go to vagrant directory

    cd /vagrant/tournament
    
10. Running sql script
    
    psql -f tournament.sql
    
11. To run given unit testcases

    python tournament_test.py
    
