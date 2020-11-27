import yaml, json, html
import datetime
import argparse
from bottle import route, post, run, template, response, request, HTTPError, redirect, static_file
from pony import orm

db = orm.Database()
base_url = "" #will be overidden when conf is loaded

columns = {}

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
        for word in self.data.get(dataKey, "").split():
            if word[0] == word[-1] and colors.get(word[0]):
                words.append(colors[word[0]][0]+html.escape(word)+colors[word[0]][1])
            else:
                words.append(html.escape(word))
                
        return " ".join(words)

@route('/')
def index():
    return template('index', tasks=None, columns=columns, table=None)

@route('/<table>')
def index(table):
    tasks = []
    with orm.db_session:
        tasks = orm.select(t for t in Task if t.table == table).order_by(lambda: orm.desc(t.date))[:]
    return template('index', tasks=tasks, columns=columns, table=table)

@post('/<table>/new')
def newTask(table):
    data = {}
    for key, value in request.forms.items():
        data[key] = value

    with orm.db_session:
        Task(data=data, date=datetime.datetime.now(), table=table)
    redirect("/"+table)

@post('/update/<task_id:int>')
def updateTask(task_id):
    data = {}
    for key, value in request.forms.items():
        data[key] = value

    table = ""
    with orm.db_session:
        task = Task[task_id]
        task.data = data
        task.date = datetime.datetime.now()
        table = task.table
    
    redirect("/"+table)

@post('/delete/<task_id:int>')
def updateTask(task_id):
    table = ""
    with orm.db_session:
        table = Task[task_id].table
        Task[task_id].delete()
    redirect("/"+table)

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

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

    db.bind('sqlite', databasePath, create_db=True)
    db.generate_mapping(create_tables=True)
    
    run(host='0.0.0.0', port=http_port, debug=debug)
    #run(host='0.0.0.0', port=2000, debug=True)
