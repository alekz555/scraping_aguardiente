py -3 -m pip install --user -r .\requirements.txt

py -3 -V



Precargar/forzar descarga del ChromeDriver
py -3 -c "from webdriver_manager.chrome import ChromeDriverManager; print(ChromeDriverManager().install())"


# 1 Confirmar que requirements.txt existe
ls -Name | findstr /I requirements

# 2 Instalar global
py -3 -m pip install --user -r .\requirements.txt

# 3 Probar import
py -3 -c "import selenium,webdriver_manager,pandas,bs4,requests,openpyxl,xlsxwriter; print('OK')"

# 4 Ejecutar todo
.\02_run_all_no_venv.bat
