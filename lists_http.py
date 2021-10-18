import yaml, json, html
import datetime
import argparse
from bottle import route, post, run, template, response, request, HTTPError, redirect, static_file
from pony import orm

db = orm.Database()
base_url = "" #will be overidden when conf is loaded

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
        for word in self.data.get(dataKey, "").replace("\r", "").replace("\n", " \n ").split(" "):
            if len(word) > 1:
                if word[0] == word[-1] and colors.get(word[0]):
                    words.append(colors[word[0]][0]+html.escape(word)+colors[word[0]][1])
                else:
                    words.append(html.escape(word))
        return " ".join(words).replace(" \n ","\n").replace("\n", "<br/>")

@route('/')
def index():
    return template('index', tasks=None, view_columns=view_columns, table=None, view=None)

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

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
    with orm.db_session:
        task = Task[task_id]
        for key, value in request.forms.decode('utf-8').items():
            task.data[key] = value
        task.date = datetime.datetime.now()
    redirect("/"+table+"/"+view)

@post('/<table>/<view>/delete/<task_id:int>')
def updateTask(table, view, task_id):
    table = ""
    with orm.db_session:
        table = Task[task_id].table
        Task[task_id].delete()
    redirect("/"+table+"/"+view)


#TODO : login decorator auth_basic by bottle (check someone is logged in)
#TODO : other access decorator for acl and group (check the logged in user has the right)



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
        view_columns = params['views']

    db.bind('sqlite', databasePath, create_db=True)
    db.generate_mapping(create_tables=True)
    
    run(host='0.0.0.0', port=http_port, debug=debug)
