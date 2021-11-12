ECHO OFF

set mypath=%cd%
start java -jar selenium-server-4.0.0.jar hub
start java -jar selenium-server-4.0.0.jar node --session-timeout 60
start python main.py