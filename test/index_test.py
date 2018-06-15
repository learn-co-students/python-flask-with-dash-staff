import unittest, sys, json
sys.path.insert(0, '..')
from ourpackage import app, server
sys.path.insert(0, '..')
from ourpackage.uber_data import data

class DashAppTestCase(unittest.TestCase):
    testy = server.test_client()

    def test_html_routes(self):
        response = self.testy.get("/users")
        self.assertEqual(response.status_code, 200)
        users = response.data.decode()
        self.assertTrue('<h3>Username: Jeff</h3>' in users)
        self.assertTrue('<h3>Username: Rachel</h3>' in users)
        self.assertTrue('<h3>Username: Daniel</h3>' in users)

        tweet_resp = self.testy.get("/tweets")
        self.assertEqual(tweet_resp.status_code, 200)
        tweets = tweet_resp.data.decode()
        self.assertEqual(tweets.count("<h4>Author: Jeff</h4>"), 3)
        self.assertEqual(tweets.count("<h4>Author: Rachel</h4>"), 3)
        self.assertEqual(tweets.count("<h4>Author: Daniel</h4>"), 3)
        self.assertEqual(tweets.count("Author:"), 9)
        self.assertEqual(tweets.count("Content:"), 9)

    def test_api_routes(self):
        response = self.testy.get("/api/users")
        self.assertEqual(response.status_code, 200)
        users_str = response.data.decode()
        users_json = json.loads(users_str)
        result = [{'id': 1, 'tweets': [{'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}, {'id': 2, 'text': 'Python is pretty neat', 'user': 'Jeff', 'user_id': 1}, {'id': 3, 'text': "Wishing I was chillin' in mexico rn", 'user': 'Jeff', 'user_id': 1}], 'username': 'Jeff'}, {'id': 2, 'tweets': [{'id': 4, 'text': 'RPDR is the best show', 'user': 'Rachel', 'user_id': 2}, {'id': 5, 'text': 'I just made the coolest NPM package!', 'user': 'Rachel', 'user_id': 2}, {'id': 6, 'text': 'Running is so fun!', 'user': 'Rachel', 'user_id': 2}], 'username': 'Rachel'}, {'id': 3, 'tweets': [{'id': 7, 'text': 'I love hogs', 'user': 'Daniel', 'user_id': 3}, {'id': 8, 'text': 'Hogs are the best way to teach react', 'user': 'Daniel', 'user_id': 3}, {'id': 9, 'text': 'Programming is lyfe', 'user': 'Daniel', 'user_id': 3}], 'username': 'Daniel'}]
        self.assertEqual(users_json, result)

        tweet_resp = self.testy.get("/api/tweets")
        self.assertEqual(tweet_resp.status_code, 200)
        tweets_str = tweet_resp.data.decode()
        tweets_json = json.loads(users_str)
        tweeprise = [{'id': 1, 'tweets': [{'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}, {'id': 2, 'text': 'Python is pretty neat', 'user': 'Jeff', 'user_id': 1}, {'id': 3, 'text': "Wishing I was chillin' in mexico rn", 'user': 'Jeff', 'user_id': 1}], 'username': 'Jeff'}, {'id': 2, 'tweets': [{'id': 4, 'text': 'RPDR is the best show', 'user': 'Rachel', 'user_id': 2}, {'id': 5, 'text': 'I just made the coolest NPM package!', 'user': 'Rachel', 'user_id': 2}, {'id': 6, 'text': 'Running is so fun!', 'user': 'Rachel', 'user_id': 2}], 'username': 'Rachel'}, {'id': 3, 'tweets': [{'id': 7, 'text': 'I love hogs', 'user': 'Daniel', 'user_id': 3}, {'id': 8, 'text': 'Hogs are the best way to teach react', 'user': 'Daniel', 'user_id': 3}, {'id': 9, 'text': 'Programming is lyfe', 'user': 'Daniel', 'user_id': 3}], 'username': 'Daniel'}]
        self.assertEqual(tweets_json, tweeprise)

    def test_dash(self):
        dash = app.serve_layout()
        raw = dash.data
        str = raw.decode()
        children = json.loads(str)['props']['children']
        self.assertEqual(dash.status_code, 200)
        self.assertEqual(children[0]['props']['children'], 'Check it out! This app has Flask AND Dash!')
        self.assertEqual(children[0]['type'], 'H1')
        self.assertEqual(children[1]['props']['children'], 'Adding some cool graph here soon:')
        self.assertEqual(children[1]['type'], 'P')
        self.assertEqual(children[2]['props']['id'], 'uber_pricing_graph')
        self.assertEqual(children[2]['props']['figure']['data'], data)
        self.assertEqual(children[2]['props']['figure']['layout']['title'], 'Uber Pricing in Brooklyn and Manhattan')
