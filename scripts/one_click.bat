@echo off
setlocal
powershell -ExecutionPolicy Bypass -File "%~dp0one_click.ps1" %*
