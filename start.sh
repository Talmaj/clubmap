#!/bin/bash

venv='ENV'

function new_tab () {
    osascript -e 'tell application "Terminal" to activate' -e 'tell application "System Events" to tell process "Terminal" to keystroke "t" using command down'
    osascript -e 'tell application "Terminal" to do script "cd ~/Projects/idivun/clubmap" in selected tab of the front window'
    osascript -e 'tell application "Terminal" to do script "source ~/Projects/idivun/clubmap/ENV/bin/activate" in selected tab of the front window'
}


function django_shell {
    osascript -e 'tell application "Terminal" to do script "python ~/Projects/idivun/clubmap/clubmap/manage.py shell" in selected tab of the front window'
    }
function django_server {
    osascript -e 'tell application "Terminal" to do script "python ~/Projects/idivun/clubmap/clubmap/manage.py runserver" in selected tab of the front window'
    }
function mysql_shell {
    osascript -e 'tell application "Terminal" to do script "mysql -u talmaj -p" in selected tab of the front window'
    }
 
mysql.server start 
mysql_shell

new_tab
clear
django_server

new_tab
clear
django_shell

new_tab
clear

