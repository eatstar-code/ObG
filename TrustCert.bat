@echo off
certutil -addstore Root "%~dp0EATSTAR_CodeSign.cer"
pause