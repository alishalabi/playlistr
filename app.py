from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.exceptions import NotFound

client = MongoClient()
db = client.playlistr
playlists = db.playlists

app = Flask(__name__)

# playlists = [
#     {'title': 'Cat Videos', 'description': 'Cats acting weird'},
#     {'title': '80\'s Music', 'description': 'Don\'t stop believing!'}
# ]


@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())


@app.route('/playlists/new')
def playlists_new():
    """CRUD - Helper: Render New Playlist Form"""
    return render_template('playlists_new.html', playlist={}, title='New Playlist')


@app.route('/playlists', methods=["POST"])
def playlists_submit():
    """CRUD: Create New Playlist"""
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """CRUD - Helper: Render One Playlist"""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)


@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """CRUD - Helper: Render Edit Form """
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')


@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """CRUD: Update Playlist"""
    if request.form.get('_method') == 'PUT':
        updated_playlist = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'videos': request.form.get('videos').split()
        }
        playlists.update_one(
            {'_id': ObjectId(playlist_id)},
            {'$set': updated_playlist})
        return redirect(url_for('playlists_show', playlist_id=playlist_id))
    else:
        raise NotFound()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
