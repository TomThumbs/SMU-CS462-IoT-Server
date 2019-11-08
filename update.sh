# /bin/bash

# Copy all the supervisor conf files
scp -r -i ~/Desktop/TomThumbsMacbook2.pem supervisor/*.conf ubuntu@3.132.83.5:/etc/supervisor/conf.d/

# Copy all the app files
scp -r -i * ubuntu@3.132.83.5:/home/ubuntu/app/