
# Using Dash and Flask Together

## Introduction
In this lab we are going to be using our knowledge of Flask apps and Dash apps to combine them into one! This may sound a little confusing, but remember that Dash is actually built on Flask among other things. So, these two frameworks work together more easily than we initially might think. By the end of this lab, we are going to have an app that has routes to return JSON data, HTML templates, AND a Dash dashboard that provides us a page to showcase our data visualization skills.

## Objectives
* Restructure an existing Flask app to use Dash
* Create a Dash layout and add a second page for a dashboard
* Add a graph to the new dashboard

## Restructuring a Flask App

The goal for this lab is to create an integrated Flash and Dash app.  We will be working with the users and tweets Flask app from a previous lab, and making changes to integrate a Dash app and graphical visualization.  For the purposes of this lab, we will be using the same graphical representation of Uber fares in Brooklyn and Manhattan.  By the end of the lab, a client should be able to 1) go to any of our API routes to view the correct JSON, 2) go to any non-API URL to view our users and tweets data rendered via the proper HTML template, and 3) be able to go to our app's dashboard to view the graph of Uber data.

Now that our app is becoming larger and more complex, we have separated our concerns by creating specific files for specific tasks.  We will run our integrated app from the `run.py` file in the main directory.  Our users and tweets Flask app is set up in its own folder called `ourpackage`.  Inside this subdirectory, we we can see our models, routes, and HTML templates are already defined.  Our Flask app configuration can be found in the `__init__.py` file.  We'll begin our Flask and Dash integration here.

### `__init__.py`

Our `__init__.py` file looks like the following:

```python
# import Flask
from flask import Flask
# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy


# initialize new flask app
app = Flask(__name__)
# add configurations and database
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# connect flask_sqlalchemy to the configured flask app
db = SQLAlchemy(app)

#import our routes after our database has been configured
from ourpackage import routes
```

**The Problem:**
We begin with a regular Flask app configuration, as we can see above. However, there is one problem: our Flask app is currently assigned to the `app` variable.  Recall that, in the previous lab, our Dash app was assigned to the `app` variable as well. 

`app = dash.Dash()`

Fortunately, Dash is built on Flask as we have already mentioned. We can keep most of our set up, but we'll need to instantiate our Dash app and change some names around to avoid this double assignment problem. Essentially, what we will do is embed our Flask app into our new Dash app. This may sound a little backwards, but it makes sense given the set up. Our Flask app will handle the logic for managing server requests. Therefore, we will rename our Flask app instance from `app` to `server`. Then, when we are creating a new Dash app, we can pass an optional argument in for the server. Check it out:

```python
# import Flask
from flask import Flask
# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# import Dash framework
import dash

# initialize new Flask app
server = Flask(__name__)
# add configurations and database
server.config['DEBUG'] = True
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# connect flask_sqlalchemy to the configured flask app
db = SQLAlchemy(server)

#create new Dash app and use existing Flask app as our Dash app's server
app = dash.Dash(__name__, server=server)

#import our routes after our database has been configured
from ourpackage import routes
```

So, we are assigning our new Dash app to the variable `app` and telling it to use our Flask application as it's server. If we didn't already have a Flask application set up, we could also leave out the server argument and the Dash app would create a new Flask server for us, as it did in our stand alone Dash application. 

We can think of the server as an attribute of the Flask app -- this is why we said we would embed the server in the Dash app. Either way, once the server is hooked up to the new Dash app, we can reference it in two ways; assigning it to a variable, `server` like we have in the example above, or by writing `app.server`. 

### `routes.py`

After we have configured our new Dash app, we need to think about how the changes we just made affect the rest of our application. We must have at least one file that is importing our `app`, right? Let's check -- it looks like our models are importing just our `db` from `ourpackage`, but the routes file is importing the `app`. We were using our Flask instance to create routes on the server but we were referencing this Flask instance as `app`, so, we'll need to change this.

We can do one of two things:
1. We can import `server` from `ourpackage` if we have defined a `server` variable 
2. We can change the decorators for our routes from `@app.route([ROUTE])` to `@app.server.route([ROUTE])`

In general, we should justify all our coding decisions with some logic and reasoning. We could argue that keeping our import the same lowers the risk of an unforeseen error somewhere else in our code like an undefined variable, for example. This is especially true in larger code bases where there are many more moving parts. Since this application is small, we can choose either of the above options. As it is now part of the app, let's forgo importing `server` in favor of referencing the server with `@app.server.route([ROUTE])` decorators. We must change all of the decorators in our routes file accordingly.

### `run.py`

Next, we will need to tweak our `run.py` file, where we are also importing `app` from `ourpackage`. Recall that in our Flask app, our command to run our server was:
   
```python
if __name__ == "__main__":
    app.run(debug=True)
```

However, since our `app` is now an instance of Dash, we need to change this command to run our Dash app like so:

```python
if __name__ == "__main__":
    app.run_server(debug=True)
```

Now, if we run our application, it should function as it did before we made these changes.

### Back to `__init__.py`

There is one caveat - if we visit any URL that is not defined on our server, our Dash app will try to display Dash's layout. 

To avoid this behavior and only display the routes that we define, we have to give a third argument to our Dash instance, `url_base_pathname`. What this does is tell our Dash app the route on which we want to display our dashboard. We will give it the route `'/dashboard'` for now, and our application will only display our dashboard at the `'/dashboard'` route.

Now that we have everything configured and working with our existing Flask app, let's define a layout for our Dash app!

## Creating a Dash Layout in a Flask app

The next step is to actually create our dashboard's layout. Previously, we had accomplished this by defining the layout below our new Dash instance. However, there's a bit more going on in our new application. So, let's continue with our pattern of separation of concerns. Let's use the file named `dashboard.py`.

To create our app's layout, we will need to import Dash's html and core components as well as our Dash app itself from ourpackage. 

```python 
import dash_core_components as dcc
import dash_html_components as html
from ourpackage import app
```

Alright, now we are ready to create our layout. Let's just start out with an h1 and a p tag. The h1 should say "Check it out! This app has Flask AND Dash!" and the p tag should read, "Adding some cool graph here soon:". 

> <h1>Check it out! This app has Flask AND Dash!</h1>
> <p>Adding some cool graph here soon:</p>

Once we have our layout written up, let's try try it out! Run `python run.py` in the terminal and venture over to our `'/dashboard'` route in the browser at `http://localhost:8050/dashboard`.  What will we see?

> **builtins.AttributeError**
> AttributeError: 'NoneType' object has no attribute 'traverse'

Oh no! What went wrong? The problem we have is that we are not importing our new app's layout anywhere. Our `routes.py` file is still loading our initial app instance from the `__init__.py` file. So, we will need to change this. We could import our `dashboard.py` file in our `__init__.py` file and then our route to `'/dashboard'` would work since our run file is now importing it when it runs the `__init__.py` file. However, we could imagine in the future that we might want to change our routes based on which graph we are showing. So, we wouldn't be able to keep our separation of concerns if we start defining routes somewhere else in our package. 

Let's go back to the routes and change up our imports a bit. Let's import our app from the dashboard file. So, our imports will now look like this:

```python
from flask import render_template, jsonify, json
from ourpackage.models import User, Tweet
from ourpackage import db, app
from ourpackage.dashboard import app
```

Notice we are importing our app from the `dashboard.py` file where we defined our layout. Now, if we refresh our web page, we will see our dashboard display. If we wanted to make further use of this import and wanted to define another route at which we can view the dashboard, we can simply define another route like we have before and call the `index` method on our app instance. 

```python
@app.server.route('/go-to-dashboard')
def dashboard():
    return app.index()
```

Now, if you visit the `'/go-to-dashboard'` route, we will see our dashboard displayed there too! Go to the URLs of some of the other routes we defined.  Our JSON data should be appear when we go to any of the API routes and our HTML should be rendered, via our templates, whenever we go to the regular web page URLs.  Pretty neat stuff!

## Adding a Graph

Alright, it's time to add a graph to our dashboard. 

**Remember:** *graph components come from Dash's dash_core_components*

We can use our Uber fare data from the previous lab and set up a graph using dcc.Graph(). Remember all graphs must have an `id`. We can find our Uber data in the uber_data.py file. Once we have our graph set up, we should be all good to check it out in our browser!

## Summary

In this lab, we were able to integrate our knowledge of Flask apps with our knowledge of Dash. We restructured our Flask app to embed it into a Dash app. With this restructuring, we were able to maintain all the original functionality of our Flask app but add in a really cool new dashboard that we can use to display graphs and any type of data visualizations we want.
