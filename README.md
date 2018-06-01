
# Using Dash and Flask together

## Introduction
In this lab we are going to be using our knowledge of flask apps and dash apps to combine them into one! This may sound a little confusing, but remember that dash is actually built on flask among other things. So, these two frameworks work together more easily than we might initially think. By the end of this lab, we are going to have an app that has routes to return json data, html templates, AND a dash dashboard that provides us a page to showcase our data visualization skills.

## Objectives
* Restructure an existing flask app to use dash
* Create a dash layout and add a second page for a dashboard
* Add a graph to the new dashboard

## Restructuring a Flask App

Alright, so our flask app from a previous lab is currently set up as a package in our main directory, where we have our run file. Inside our package, which for the purposes of this lab is named `ourpackage`, we have our models and routes defined in their own files and our template files defined in the templates directory, and our `__init__.py` file looks like the following:

```python
# import Flask, jsonify, render_template, and json from flask
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

If we look around it seems like not much has changed, and that is because it hasn't yet! But we can see our flask app is currently assinged to our `app` variable which is problematic since that is the set up we had for our dash app as well. That is okay, because as we talked about before, dash is built on flask. So, we can mostly keep this set up, but we'll need to instantiate our dash app and change some names around. Basically what we are going to be doing is embedding our flask app into our new dash app. This may sound a little backwards, but it makes sense given the set up. Our flask app is going to serve as our logic for handing server requests. So, we are going to rename `app` to `server`. Then when we are creating a new dash app, we can pass an optional argument in for the server. Check it out:

```python
# import Flask, jsonify, render_template, and json from flask
from flask import Flask
# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# import dash framework
import dash

# initialize new flask app
server = Flask(__name__)
# add configurations and database
server.config['DEBUG'] = True
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# connect flask_sqlalchemy to the configured flask app
db = SQLAlchemy(server)

#create new dash app and use existing flask app as our dash app's server
app = dash.Dash(__name__, server=server)

#import our routes after our database has been configured
from ourpackage import routes
```

So, we are assigning our new dash app to the variable `app` and telling it to use our flask application as it's server. If we didn't already have a flask application set up, we could also leave out the server argument and the dash app would create a new flask server for us, as it did in our stand alone dash application. 

We can think of the server as an attribute of the flask app -- this is why we said we would embed the server in the dash app. Either way, once the server is hooked up to the new dash app, we can reference it in two ways; assigning it to a variable, `server` like we have in the example above, or by writing `app.server`. 

After we have configured our new dash app, we need to think about how the changes we just made affect the rest of our application. We must have at least one file that is importing our `app`, right? Let's check -- it looks like our models are importing just our db from `ourpakage`, but the routes file is importing the `app`. We were using our flask instance to create routes on the server but we were referencing this flask instance as `app`, so, we'll need to change this.

We can do one of two things:
1. we can change the import to bring in both `app` and `server`, if we have defined a `server` variable 
2. We can change our decorators from `@app.route([ROUTE])` to `@app.server.route([ROUTE])`

In general, we should justify all our coding decisions with some logic and reasoning. We could argue that keeping our import the same lessens the risk of an unforseen error somewhere else in our code such as an undefined variable. This is especially true in larger code bases where there are many more moving parts. Since this application is small and we know this is the only file importing the `app`, we can choose to either. As it is now part of the app, we will leave the import the same and define our routes by referencing they server with `@app.server.route([ROUTE])`. So, let's change all of the decorators in our routes file accordingly.

The next tweak we need to make to our code is our `run.py` file, which is importing our `app` from `ourpackage`. In our flask app, our command to run our server is:
   
```python
if __name__ == "__main__":
    app.run()
```

However, since our `app` is now an instance of dash, we need to change this command to run our dash app, which is:

```python
if __name__ == "__main__":
    app.run_server()
```

Now, if we run our application, it should function as it did before we made these changes. There is one caveat - if we visit any URL that is not defined on our server, our dash app will try to display our dash's layout. 

To avoid this behavior and only display the routes that we define, we have to give a third argument to our dash instance, `url_base_pathname`. What this does is tell our dash app the route on which we want to display our dashboard. We will give it the route `'/dashboard'` for now, and our application will only display our dashboard at the `'/dashboard` route.

Now that we have everything configured and working with our existing flask app, let's define a layout for our dash app!

## Creating a Dash Layout in a Flask app

The next step is to actually create our dashboard's layout. Previously, we had accomplished this by defining the layout below our new dash instance. However, there's a bit more going on in our new application. So, let's continue with our pattern of separation of concerns. Let's use the file named `dashboard.py`.

To create our app's layout, we will need to import dash's html and core components as well as the dash app itself from ourpackage. 

```python 
import dash_core_components as dcc
import dash_html_components as html
from ourpackage import app
```

Alright, now we are ready to create our layout. Let's just start out with an h1 and a p tag. The h1 should say "Check it out! This app has flask AND dash!" and the p tag should read, "Adding some cool graph here soon:". 

> <h1>Check it out! This app has flask AND dash!</h1>
> <p>Adding some cool graph here soon:</p>

Once we have our layout written up, let's try and go to our `'/dashboard'` route in the browser at `http://localhost:8050/dashboard`. This is what we will see:

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

Now, if you visit the `'/go-to-dashboard'` route, we will see our dashboard displayed there too! Pretty neat stuff!

## Adding a Graph

Alright, it's time to add a graph to our dashboard and remove that `p` tag saying "Adding some cool graph here soon:". 

**Remember:** *graph components come from dash's dash_core_components*

Can use our uber fare data from before and set up a graph using dcc.Graph(). Remember all graphs must have an `id`. We can find our uber data in the uber_data.py file. Once we have our graph set up, we should be all good to check it out in our browser!

## Summary

In this lab, we were able to integrate our knowledge of flask apps with our knowledge of dash. We restructured our flask app a bit and turned it into a dash app. With this restructure, we were able to maintain all the original functionality of our flask app but add in a really cool new dashboard that we can use to display graphs and any type of data visualizations we want.
