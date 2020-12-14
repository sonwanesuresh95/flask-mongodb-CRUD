from flask import Flask, request, render_template, redirect
import pymongo

app = Flask(__name__)
app.debug = True

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["mydatabase"]
if 'cars' not in mydb.list_collection_names():
    mycol = mydb.create_collection('cars')
else:
    mycol = mydb['cars']
print(mydb.list_collection_names())


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/cars')


@app.route('/cars', methods=['GET', 'POST'])
def friends():
    if request.method == 'POST':
        name = request.form['name']
        record = {"name": name}
        mycol.insert_one(record)
        return redirect('/cars')
    else:
        names = [i['name'] for i in mycol.find()]
        return render_template('index.html', names=names)


@app.route('/update/<name>', methods=['GET', 'POST'])
def update(name):
    record = [i for i in mycol.find({"name": name})][0]
    del record['_id']
    if request.method == 'POST':
        updated_name = request.form['name']
        updated_record = {"$set": {"name": updated_name}}
        mycol.update_one(record, updated_record)
        return redirect('/cars')
    else:
        return render_template('update.html', name=name)


@app.route('/delete/<name>', methods=['GET', 'POST'])
def delete(name):
    record = [i for i in mycol.find({"name": name})][0]
    del record['_id']
    mycol.delete_one(record)
    return redirect('/cars')


@app.route('/delete_all', methods=['GET', 'POST'])
def delete_all():
    mycol.delete_many({})
    return redirect('/cars')


if __name__ == '__main__':
    app.run()
