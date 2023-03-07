# enable virtual environment
    python -m venv venv
# activate running scripts
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# Go into virtual environment(to have all the packages imported)
    venv\Scripts\Activate.ps1
# leave virtual environment
    deactivate
# install requirements
    (pip freeze > requirements.txt)
    pip install -r requirements.txt

a