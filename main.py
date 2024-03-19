from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://angeliav:Angel14^_^@localhost/flask_example'
db = SQLAlchemy(app)

class Users(db.Model):
    """
    Class untuk membuat tabel pengguna di database.
    Args:
        db (object): object dari class SQLAlchemy
    """
    id = db.Column(db.Integer, primary_key=True) # kolom id sebagai primary key dengan tipe data integer
    name = db.Column(db.String(50)) # kolom name dengan tipe data string dengan panjang maksimal 50 karakter
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # kolom created_at dengan tipe data datetime dan default value menggunakan UTC timezone
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # kolom updated_at dengan tipe data datetime dan default value menggunakan UTC timezone, dan akan di perbarui otomatis saat data di perbarui
    is_active = db.Column(db.Boolean, default=True) # kolom is_active dengan tipe data boolean dan default value True
    
    def to_dict(self):
        """
        Mengubah object menjadi dictionary
        Returns:
            dict: dictionary yang berisi data object
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }

@app.route('/user', methods=['POST']) 
def create_user():
    """
    Route untuk membuat pengguna baru.
    Pengguna dapat membuat pengguna baru dengan menggunakan method POST.
    Parameter yang di butuhkan adalah "name".
    """
    data = request.get_json()
    new_user = Users(name=data['name'])
    if new_user is None:
        return {'success': False, 'message': 'Gagal, pengguna tidak di buat.'}, 200
    db.session.add(new_user)
    db.session.commit()
    return {'success': True, 'message': 'Pengguna telah berhasil di buat.', 'data': new_user.to_dict()}, 200
    
@app.route('/user', methods=['GET'])
def get_users():
    """
    Route untuk menampilkan semua pengguna.
    Pengguna dapat menampilkan semua pengguna dengan menggunakan method GET.
    """
    users = Users.query.all()
    if not users:
        return {'success': False, 'message': 'Query gagal.'}, 200
    return {'success': True, 'message': 'Query berhasil.', 'data': [user.to_dict() for user in users]}, 200

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    """
    Route untuk menampilkan detail pengguna.
    Pengguna dapat menampilkan detail pengguna berdasarkan id dengan menggunakan method GET.
    Parameter yang di butuhkan adalah "id".
    """
    user = Users.query.get(id)
    if user is None:
        return {'success': False, 'message': 'Gagal, pengguna tidak di temukan.'}, 200
    return {'success': True, 'message': 'Pengguna ditemukan.', 'data': user.to_dict()}, 200

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    """
    Route untuk memperbarui pengguna.
    Pengguna dapat memperbarui pengguna berdasarkan id dengan menggunakan method PUT.
    Parameter yang di butuhkan adalah "id" dan "name".
    """
    data = request.get_json()
    user = Users.query.get(id)
    if user is None:
        return {'status': False, 'message': 'Gagal, pengguna tidak di temukan.'}, 200
    user.name = data['name']
    db.session.commit() 
    return {'status': True, 'message': 'Pengguna telah berhasil di perbarui.'}, 200

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    """
    Route untuk menghapus pengguna.
    Pengguna dapat menghapus pengguna berdasarkan id dengan menggunakan method DELETE.
    Parameter yang di butuhkan adalah "id".
    """
    user = Users.query.get(id)
    if user is None:
        return {'success': False, 'message': 'Gagal, pengguna tidak di temukan.'}, 200
    Users.query.filter_by(id=id).delete()
    db.session.commit()
    return {'success': True, 'message': 'Pengguna telah berhasil di hapus.'}, 200

@app.route('/search', methods=['POST'])
def search():
    """
    Route untuk mencari pengguna berdasarkan nama.
    Pengguna dapat mencari pengguna berdasarkan nama dengan menggunakan method POST.
    Parameter yang di butuhkan adalah "name".
    """
    data = request.get_json()
    users = Users.query.filter(Users.name.ilike(f'%{data["name"]}%'))
    users_found = [user.to_dict() for user in users]
    count_users = users.count()
    if not users or count_users == 0:
        return {'success': False, 'message': 'Gagal, pengguna tidak di temukan.'}, 200
    return {'success': True, 'message': f'Pengguna ditemukan: {count_users}', 'data': users_found}, 200

@app.route('/') 
def index(): 
    """
    Menampilkan halaman utama dengan daftar API endpoints, dan contoh penggunaan.
    Dibuat menggunakan HTML dengan Bootstrap dan Javascript Ajax.
    Versi Bootstrap yang digunakan adalah 4.5.0.
    Versi jQuery yang digunakan adalah 3.5.1.

    Returns:
        str: HTML
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Endpoints</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    </head>
    <body>
        <div class="container mt-5 mb-5">
            <div class="container mt-5 mb-5">
                <h1 class="mb-4">API Endpoints</h1>
                <div>
                    <p>Ini adalah beberapa endpoint yang bisa di gunakan:</p>
                </div>
                <div class="table-responsive-sm">
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>HTTP Method</th>
                                <th>Endpoint</th>
                                <th>Deksripsi</th>
                                <th>Contoh Penggunaan</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>POST</td>
                                <td>/user</td>
                                <td>Buat pengguna baru. JSON dengan bidang kunci "name".</td>
                                <td><a href="#create-user">Javascript Ajax</a></td>
                            </tr>
                            <tr>
                                <td>GET</td>
                                <td>/user</td>
                                <td>Menampilkan semua pengguna.</td>
                                <td><a href="#get-users">Javascript Ajax</a> | <a href="/user" target="_blank">Tab Baru</a></td>
                            </tr>
                            <tr>
                                <td>GET</td>
                                <td>/user/&lt;id&gt;</td>
                                <td>Menampilkan detail pengguna.</td>
                                <td><a href="#get-user">Javascript Ajax</a> | <a href="/user/1" target="_blank">Tab Baru</a></td>
                            </tr>
                            <tr>
                                <td>PUT</td>
                                <td>/user/&lt;id&gt;</td>
                                <td>Memperbarui pengguna. JSON dengan bidang kunci "name".</td>
                                <td><a href="#update-user">Javascript Ajax</a></td>
                            </tr>
                            <tr>
                                <td>DELETE</td>
                                <td>/user/&lt;id&gt;</td>
                                <td>Menghapus pengguna.</td>
                                <td><a href="#delete-user">Javascript Ajax</a></td>
                            </tr>
                            <tr>
                                <td>POST</td>
                                <td>/search</td>
                                <td>Mencari pengguna berdasarkan nama. JSON dengan bidang kunci "name".</td>
                                <td><a href="#search">Javascript Ajax</a></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="container mt-5 mb-5">
                <h1 class="mb-4">Contoh Penggunaan</h1>
                <div>
                <p>Berikut adalah contoh penggunaan API endpoints:</p>
                </div>
                <h2 class="mt-4" id="create-user">Membuat Pengguna</h2>
                <div class="input-group mb-3">
                    <input id="create-user-name" type="text" placeholder="Name" class="form-control">
                    <div class="input-group-append">
                        <button onclick="createUser()" class="btn btn-primary">Buat Pengguna</button>
                    </div>
                </div>
                <div id="create-user-response"></div>

                <h2 class="mt-4" id="get-users">Menampilkan Pengguna</h2>
                <button onclick="getUsers()" class="btn btn-primary mb-3">Tampilkan Pengguna</button>
                <div id="get-users-response"></div>

                <h2 class="mt-4" id="get-user">Menampilkan Detail Pengguna</h2>
                <div class="input-group mb-3">
                    <input id="get-user-id" type="text" placeholder="ID" class="form-control">
                    <div class="input-group-append">
                        <button onclick="getUser()" class="btn btn-primary">Tampilkan Pengguna</button>
                    </div>
                </div>
                <div id="get-user-response"></div>
                
                <h2 class="mt-4" id="update-user">Memperbarui Pengguna</h2>
                <div class="input-group mb-3">
                    <input id="update-user-id" type="text" placeholder="ID" class="form-control">
                    <input id="update-user-name" type="text" placeholder="Name" class="form-control">
                    <div class="input-group-append">
                        <button onclick="updateUser()" class="btn btn-primary">Perbarui Pengguna</button>
                    </div>
                </div>
                <div id="update-user-response"></div>

                <h2 class="mt-4" id="delete-user">Menghapus Pengguna</h2>
                <div class="input-group mb-3">
                    <input id="delete-user-id" type="text" placeholder="ID" class="form-control">
                    <div class="input-group-append">
                        <button onclick="deleteUser()" class="btn btn-primary">Hapus Pengguna</button>
                    </div>
                </div>
                <div id="delete-user-response"></div>

                <h2 class="mt-4" id="search">Mencari Pengguna</h2>
                <div class="input-group mb-3">
                    <input id="search-user-name" type="text" placeholder="Name" class="form-control">
                    <div class="input-group-append">
                        <button onclick="searchUser()" class="btn btn-primary">Cari Pengguna</button>
                    </div>
                </div>
                <div id="search-user-response"></div>

            </div>
        </div>

        <script>
            function createUser() {
                var userName = $('#create-user-name').val();
                $.ajax({
                    url: '/user',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ name: userName }),
                    success: function(data) {
                        $('#create-user-response').html('<pre>' + JSON.stringify(data, null, 2) + '</pre>');
                    }
                });
            }

            function getUsers() {
            $.ajax({
                    url: '/user',
                    type: 'GET',
                    success: function(data) {
                        $('#get-users-response').html('<pre>' + JSON.stringify(data, null, 2) + '</pre>');
                    }
                });
            }

            function getUser() {
            var userId = $('#get-user-id').val();
                $.ajax({
                    url: '/user/' + userId,
                    type: 'GET',
                    success: function(data) {
                        $('#get-user-response').html('<pre>' + JSON.stringify(data, null, 2) + '</pre>');
                    }
                });
            }

            function updateUser() {
            var userName = $('#update-user-name').val();
            var userId = $('#update-user-id').val();
                $.ajax({
                    url: '/user/'+userId,
                    type: 'PUT',
                    contentType: 'application/json',
                    data: JSON.stringify({ name: userName }),
                    success: function(data) {
                        $('#update-user-response').html('<pre>' + JSON.stringify(data, null, 2) + '</pre>');
                    }
                });
            }

            function deleteUser() {
            var userId = $('#delete-user-id').val();
                $.ajax({
                    url: '/user/' + userId,
                    type: 'DELETE',
                    success: function(data) {
                        $('#delete-user-response').html('<pre>' + JSON.stringify(data, null, 2) + '</pre>');
                    }
                });
            }

            function searchUser() {
            var userName = $('#search-user-name').val();
                $.ajax({
                    url: '/search',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ name: userName }),
                    success: function(data) {
                        $('#search-user-response').html('<pre>' + JSON.stringify(data, null, 2) + '</pre>');
                    }
                });
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)