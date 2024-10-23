from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import hashlib
import re
from datetime import datetime
app = Flask(__name__,static_url_path='/static')
app.secret_key = "your_secret_key"

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['surya']
users_collection = db['student']

@app.route('/')
def index():
    if 'username' in session:
        return render_template("index.html")
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_message=None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return "Please fill out all the fields."
        
        # Validate the username (email) format using a regular expression
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', username):
             return render_template("signup.html",error_message="Please provide a valid email address.")

        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return render_template("signup.html",error_message="Username already exists.") 

        # Hash the password before storing it in the database
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
        # Save the user information in the database
        user_data = {'username': username, 'password': hashed_password}
        users_collection.insert_one(user_data)

        session['username'] = username
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate the username (email) format using a regular expression
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', username):
            return render_template('login.html',error_message = "Please provide a valid email address.")    

        # Hash the password for comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = users_collection.find_one({'username': username, 'password': hashed_password})
        if user:
            session['username'] = username      
            return redirect(url_for('index'))
        else:
            error_message= "Invalid email or password."

    return render_template('login.html',error_message=error_message)

@app.route('/logout',methods=["GET","POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/c')
def c_category():
    
    
    category_name = 'C'
    blog_content = [
        ('1.PROGRAMIZ', 'https://www.programiz.com/c-programming'),
        ('2.W3 SCHOOLS', 'https://www.w3schools.com/c/c_intro.php'),
        ('3.JAVA POINT', 'https://www.javatpoint.com/c-programming-language-tutorial'),
        ('4.GEEKS FOR GEEKS', 'https://www.geeksforgeeks.org/c-programming-language/'),
        ('5.TUTORIAL POINTS', 'https://www.tutorialspoint.com/cprogramming/index.htm'),
        ('6.FREE CODE CAMP', 'https://www.freecodecamp.org/news/what-is-the-c-programming-language-beginner-tutorial/'),
        ('7.SCALER', 'https://www.scaler.com/topics/c/'),
        ('8.BEGINNERS BOOK', 'https://beginnersbook.com/2014/01/c-tutorial-for-beginners-with-examp'),
        ('9.LOG2BASE2', 'https://www.log2base2.com/C/basic/simple-c-program.html'),
        ('10.C PROGRAMMING.COM', 'https://www.cprogramming.com/tutorial/c-tutorial.html?inl=hp')
    ]
    return render_template('empty_page.html', category_name=category_name, blog_content=blog_content)
@app.route('/python') 
def python_category():
    category_name = 'Python'
    blog_content = [
        ('1.PROGRAMIZ', 'https://www.programiz.com/python-programming'),
        ('2.W3 SCHOOLS', 'https://www.w3schools.com/python/python_intro.asp'),
        ('3.JAVA POINT', 'https://www.javatpoint.com/python-tutorial'),
        ('4.GEEKS FOR GEEKS', 'https://www.geeksforgeeks.org/python-programming-language/'),
        ('5.PYTHON TUTORIAL', 'https://www.pythontutorial.net/'),
        ('6.FREE CODE CAMP', 'https://www.freecodecamp.org/news/python-code-examples-sample-script-coding-tutorial-for-beginners/'),
        ('7.SCALER', 'https://www.scaler.com/topics/python/'),
        ('8.INTELLIPAAT', 'https://intellipaat.com/blog/tutorial/python-tutorial/'),
        ('9.DIGITAL OCEAN', 'https://www.digitalocean.com/community/tutorial-series/how-tl̥o-code-in-python-3'),
        ('10.QUANTLNSTI', 'https://blog.quantinsti.com/python-programming/')
    ]
    return render_template('empty_page.html', category_name=category_name, blog_content=blog_content)
 

@app.route('/java')
def java_category():
    category_name = 'Java'   
    blog_content = [
        ('1.W3 SCHOOLS', 'https://www.w3schools.com/java/java_intro.asp'),
        ('2.PROGMAIZ', 'https://www.programiz.com/java-programming'),
        ('3.JAVA POINT', 'https://www.javatpoint.com/java-tutorial'),
        ('4.GEEKS FOR GEEKS', 'https://www.geeksforgeeks.org/java/'),
        ('5.JAVA TUTORIAL', 'https://www.tutorialspoint.com/java/'),
        ('6.SCALER', 'https://www.scaler.com/topics/java/'),
        ('7.GURU99', 'https://www.guru99.com/java-tutorial.html'),
        ('8.CODE WITH HARRY', 'https://www.codewithharry.com/tutorial/java/'),
        ('9.WIKI BOOKS', 'https://en.wikibooks.org/wiki/Java_Programming'),
        ('10.LEARN JAVA ONLINE','https://www.learnjavaonline.org/')
    ]
    return render_template('empty_page.html', category_name=category_name, blog_content=blog_content)

@app.route('/sports')
def sports_category():
    category_name = 'Sports'
    blog_content = [
        ('1.BBCI', 'https://www.bcci.tv/'),
        ('2.MARCA', 'https://www.marca.com/'),
        ('3.CRICBUZZ', 'https://www.cricbuzz.com/CRICBUZZ'),
        ('4.AS', 'https://as.com/'),
        ('5.ESPNCRICINFO', 'https://www.espncricinfo.com/'),
        ('6.SPORTSKEEDA', 'https://www.sportskeeda.com/'),
        ('7.GOAL', 'https://www.goal.com/en-in'),
        ('8.YAHOO SPORTS', 'https://sports.yahoo.com/'),
        ('9.247SPORTS', 'https://247sports.com/'),
        ('10.ESPN','https://www.espn.in/')
    ]
    return render_template('empty_page.html', category_name=category_name, blog_content=blog_content)

@app.route('/politics')
def politics_category():
    category_name = 'Politics'
    blog_content = [
        ('1.TIMES OF INDIA', 'https://timesofindia.indiatimes.com/blogs/politics/'),
        ('2.NIC', 'https://www.nic.in/'),
        ('3.PRESIDENT OF INDIA', 'https://presidentofindia.nic.in/'),
        ('4.THE HINDU', 'https://www.thehindu.com/news/national/andhra-pradesh/'),

    ]
    return render_template('empty_page.html', category_name=category_name, blog_content=blog_content)
if __name__ == '__main__':
    app.run(debug=True,port=5000)
