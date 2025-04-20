@echo off
echo Running migration to add profile fields...
python migrations/add_profile_fields.py
echo.
pause
