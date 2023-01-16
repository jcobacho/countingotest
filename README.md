# countingotest
A django project for Countigo course

## STEPS
1. create virtual environment
<code>virtualenv venv</code>
2. activate virtual environment
<code>source venv/bin/activate </code>
3. install requirements 
<code>pip install -r requirements/base.txt</code>
4. migrate db 
<code>python manage.py migrate</code>
5. load technologies data 
<code>python manage.py loaddata technologies</code>
6. Run server <code> python manage.py runserver</code>
7. Run Tests <code> python manage.py test </code>
7. Access 127.0.0.1:8000
