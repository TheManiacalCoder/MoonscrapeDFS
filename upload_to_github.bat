@echo off
REM Batch file to upload project to GitHub

REM Set your GitHub repository URL
set GITHUB_REPO_URL=https://github.com/TheManiacalCoder/MoonscrapeDFS.git

REM Initialize Git repository
echo Initializing Git repository...
git init

REM Add all files to staging
echo Adding files to staging...
git add .

REM Commit changes
echo Committing changes...
git commit -m "Initial project upload"

REM Add remote repository
echo Adding remote repository...
git remote add origin %GITHUB_REPO_URL%

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin master

REM Completion message
echo Project successfully uploaded to GitHub!
pause 