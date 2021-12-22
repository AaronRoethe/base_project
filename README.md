# Project Skeleton

# Ojective 
The goal is to create an easy-to-use template based on my experience developing analytic-based automation and reporting.

# Setup
Change venv and project variables inside 
- run.bat
- setup.bat

Once you've installed all dependencies for the project run:
``` cmd
call conda env export > environment.yml
```
Now when someone else wants to try out your project they can run:
```cmd
setup.bat
```