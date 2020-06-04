$env:FLASK_APP = "wsgi.py"
$env:FLASK_DEBUG=1
$env:APP_CONFIG_FILE="config.py"
flask run

Read-Host -Prompt "Press Enter to exit"