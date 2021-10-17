import yaml, json, html
import datetime
import argparse
from bottle import route, post, run, template, response, request, HTTPError, redirect, static_file
from pony import orm

db = orm.Database()
base_url = "" #will be overidden when conf is loaded

columns = {}
view_columns = {}

class Task(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    data = orm.Required(orm.Json)
    date = orm.Required(datetime.date)
    table = orm.Required(str)
    

    def getHtml(self, dataKey):
        colors = {
            '+': ['<button class="pure-button button-green">','</button>'],
            '*': ['<button class="pure-button button-orange">','</button>'],
            '-': ['<button class="pure-button button-blue">','</button>'],
            '!': ['<button class="pure-button button-red">','</button>'],
            '`': ["<code>","</code>"],
            '_': ['<b>','</b>']
        }
        words = []
        for word in self.data.get(dataKey, "").split(" "):
            if word[0] == word[-1] and colors.get(word[0]):
                words.append(colors[word[0]][0]+html.escape(word)+colors[word[0]][1])
            else:
                words.append(html.escape(word))
        return " ".join(words).replace("\n", "<br/>")

@route('/')
def index():
    return template('index', tasks=None, view_columns=view_columns, table=None, view=None)

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

@route('/<table>/raw')
def index(table):
    tasks = []
    with orm.db_session:
        tasks = orm.select(t for t in Task if t.table == table).order_by(lambda: orm.desc(t.date))[:]
    return template('index', tasks=tasks, columns=columns[table], view=None)

@route('/<table>/<view>')
def viewTable(table, view):
    if not view_columns.get(table, {}).get(view):
        # if table or view does not exists, redirect to index
        redirect("/")
    tasks = []
    with orm.db_session:
        tasks = orm.select(t for t in Task if t.table == table).order_by(lambda: orm.desc(t.date))[:]
    return template('index', tasks=tasks, view_columns=view_columns, table=table, view=view)


@post('/<table>/<view>/new')
def newTask(table, view):
    data = {}
    for key, value in request.forms.decode('utf-8').items():
        data[key] = value

    with orm.db_session:
        Task(data=data, date=datetime.datetime.now(), table=table)
    redirect("/"+table+"/"+view)

@post('/<table>/<view>/update/<task_id:int>')
def updateTask(table, view, task_id):
    #udpate only provided fields, do not modify other fields
    #data = {}

    table = ""
    with orm.db_session:
        task = Task[task_id]
        for key, value in request.forms.decode('utf-8').items():
            task.data[key] = value
            print("upd:{}={}".format(key, value))
        task.date = datetime.datetime.now()
        table = task.table
    redirect("/"+table+"/"+view)

@post('/<table>/<view>/delete/<task_id:int>')
def updateTask(table, view, task_id):
    table = ""
    with orm.db_session:
        table = Task[task_id].table
        Task[task_id].delete()
    redirect("/"+table+"/"+view)


if __name__ == '__main__':    
    # Read CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('configPath', metavar='configPath',
            help='Path to YML config file')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Should print information and debug messages')
    args = parser.parse_args()

    verbose = args.verbose

    with open(args.configPath, 'r') as ymlFile:
        params = yaml.load(ymlFile)
        # CONSTANTS
        verbose = args.verbose
        databasePath = params['database_path']
        base_url = params['base_url']
        http_port = params['http_port']
        debug = params['debug']
        columns = params['tables']
        view_columns = params['views']

    db.bind('sqlite', databasePath, create_db=True)
    db.generate_mapping(create_tables=True)
    
    run(host='0.0.0.0', port=http_port, debug=debug)
    #run(host='0.0.0.0', port=2000, debug=True)
