# Hardware
- Orangepi3LTS (arm-64bits) | [Specs](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/orange-pi-3-LTS.html) | [Manual](https://drive.google.com/file/d/1jka7avWnzNeTIQFkk78LoJdygWaGH2iu/view)
- OS: Debian GNU/Linux 11 (bullseye) aarch64 (image recommended by manufacturer)

# Tecnologies
- Web (HTTP, python, Flask) - Client - web_server.py
- Timelapses (python, ffmpeg) - Devices - timelapse_core.py
- HTTP server python - Resources - [Timelapses saved](./resources)

## Initialize app (linux) on root of the project
```python3 -m venv web && pip install -r requierements.txt```

## Start app
[example to initialize](./automation/timelapse_start.sh) - nohup

## Timelapses-sevice started when power-up (optional)
1. Change your path info on the templates of the scripts of the service

[template-start](./automation/timelapse_start.sh)

[template-stop](./automation/timelapse_stop.sh)

2. Change and save the script paths on the service file

[template-service settings](./automation/timelapses-server.service)

```
sudo nano /etc/systemd/system/timelapses-server.service
```

3. Execute the next instructions

```
sudo systemctl daemon-reload
sudo systemctl enable timelapses-server.service
sudo systemctl start timelapses-server.service
```

5. Test the service on power-up check
[Resources with python http.server](http://ip-server:8000) | [Client web](http://ip-server:5000)
