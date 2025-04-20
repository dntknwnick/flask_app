@echo off
echo MySQL Setup for Jishu Backend
echo ============================

echo.
echo Step 1: Test MySQL Connection
python test_mysql.py

echo.
echo Step 2: Update MySQL Configuration
python update_mysql_config.py

echo.
echo Step 3: Create MySQL Database
python create_mysql_db.py

echo.
echo Step 4: Initialize Database Tables and Sample Data
python init_db.py

echo.
echo Setup completed!
echo You can now run the Flask application with: python run.py
echo.
pause
