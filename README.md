# emotion_tracker_django

Django equivalent of EmotionTracker, my RoR CRUD demonstrator<br> 
Refer to: https://github.com/sshakil<br>
No OAuth+PKCE, yet; uses the same DB as above.<br>
No need for migrations to be run to get up and running.<br>
Do need `ENABLE_OAUTH=false` in command for front-end

## Start Django Server
```commandline
python manage.py runserver 8000
```
## Start Front End
```commandline
ENABLE_OAUTH=false npx webpack --watch --config ./webpack.config.js
```
