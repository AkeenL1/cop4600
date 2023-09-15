# cop4600
steps for local development

Make sure git is installed 
if on linux use whatever package manager you prefer
```npm install git```
if on mac use homebrew
```brew install git```
You can check it's installed by going
```git -v```

1. Clone the repo
   ```git clone https://github.com/AkeenL1/cop4600.git```
2. change to your local directory
  ```cd cop4600```
3. switch to the correct branch
  to view all available branches
  ```git branch```
  to select the main branch
  ```git checkout main```

Steps to push changes once finished w/ code
1. to view all changed files
  ```git status```
2. If everything looks good, to stage the files for commit do
   ```git add .```
   otherwise if you want to only do a specific file or folder do
   ```git add /path/to/file```
3.then commit your changes (NOTE: this does not push your changes to the online repository just readies them locally )
  ```git commit -m "your commit message here"```
4. finally to update the repository do
   ```git push origin```
   you may be asked to set an upstream origin when trying to do this the first time. Simply copy and paste the command git recommends you
