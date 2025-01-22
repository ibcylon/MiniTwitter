from flask import Flask, request
from CustomJSONProvider import CustomJSONProvider

app = Flask(__name__)
app.users = { }
app.id_count = 1
app.tweets = []
app.json = CustomJSONProvider(app)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/sign-up', methods=['POST'])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count += 1
    return new_user, 201

@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload["id"])
    new_tweet = payload["tweet"]

    if user_id not in app.users:
        return "user not found", 404

    if len(new_tweet) > 300:
        return "tweet too long", 400

    app.tweets.append({
        'user_id': user_id,
        'tweet': new_tweet
    })
    return '', 204

@app.route('/follow', methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload["id"])
    target_id = int(payload["follow"])

    if user_id not in app.users or target_id not in app.users:
        return 'user not found', 404

    user = app.users[user_id]
    user.setdefault("follow", set()).add(target_id)

    return user, 200

@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload["id"])
    target_id = int(payload["unfollow"])

    if user_id not in app.users or target_id not in app.users:
        return 'user not found', 404
    user = app.users[user_id]
    user.setdefault("follow", set()).discard(target_id)
    return user, 200

@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return "user not found", 404
    follow_list = app.users[user_id].get("follow", set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet["user_id"] in follow_list]

    return { 'user_id': user_id, 'timeline': timeline }, 200

if __name__ == '__main__':
    app.run()

