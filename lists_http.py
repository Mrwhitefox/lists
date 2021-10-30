import yaml, json, html, datetime, argparse
from bottle import route, post, run, template, response, request, HTTPError, redirect, static_file
from pony import orm

db = orm.Database()
view_columns = {}
view_filters = {}
acl = {}

class Task(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    data = orm.Required(orm.Json)
    update_date = orm.Required(datetime.datetime)
    creation_date = orm.Required(datetime.datetime)
    deletion_date = orm.Optional(datetime.datetime)
    table = orm.Required(str)

    def getHtml(self, dataKey):
        colors = { # for html tags when a word is enclosed with special character
            '+': ['<button class="pure-button button-green">','</button>'], '*': ['<button class="pure-button button-orange">','</button>'],
            '-': ['<button class="pure-button button-blue">','</button>'],  '!': ['<button class="pure-button button-red">','</button>'],
            '§': ['<button class="pure-button button-purple">','</button>'], '`': ["<code>","</code>"], '_': ['<b>','</b>']
        }
        words = []
        for word in self.data.get(dataKey, "").replace("\r", "").replace("\n", " \n ").split(" "): # split all words
            if len(word) > 2 and word[0] == word[-1] and colors.get(word[0]): # if word long enough and beginning and ending with special char
                    words.append(colors[word[0]][0]+html.escape(word)+colors[word[0]][1]) #enclose with html
            else:
                words.append(html.escape(word))
        return " ".join(words).replace(" \n ","\n").replace("\n", "<br/>")

def redirect_if_disallowed(table, view, mode="r"):
    if not check_acl_allowed(table, view) or (mode=="rw" and not check_acl_allowed(table, view, "write")) :
        redirect("/")

def check_acl_allowed(table, view, mode="read"):
    user = request.get_header('User-Agent')
    allowed_groups =  acl.get('restricted_views' if mode=="read" else 'restricted_write', {}).get(table, {}).get(view, []) #select different dict if read or write, default is empty
    if not allowed_groups: # no dict = no restrictions = everyone allowed
        return True
    return any( [user in acl.get('groups', {}).get(allowed_group, []) for allowed_group in allowed_groups] ) # True if user is in any list of any allowed groups

def allowed_views(): # return a copy of view_columns without disallowed views
    return {table: { view: view_columns[table][view] for view in views if check_acl_allowed(table, view)} for table, views in view_columns.items() }

def filter_tasks(tasks_list, table, view):
    column_keywords = view_filters.get(table, {}).get(view, {})

    if not column_keywords:
        return tasks_list #no keyword = no filter = return all

    # filter tasks: keep the lines with any column having a mathing keyword
    return filter( lambda task: any( [any([keyword in task.data.get(column, "") for keyword in column_keywords[column]]) for column in column_keywords]) , tasks_list)

@route('/')
def index():
    return template('index', tasks=None, view_columns=allowed_views(), table=None, view=None)

@route('/static/<filename:path>')
@route('/images/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

@route('/<table>/deleted-items')
def deletedItems(table):
    redirect_if_disallowed(table, "deleted-items")
    tasks = []
    with orm.db_session:
        tasks = orm.select(t for t in Task if t.table == table and t.deletion_date is not None).order_by(lambda: orm.desc(t.update_date))[:]
    all_columns = {}
    for task in tasks:
        all_columns.update(task.data)

    return template('index', tasks=tasks, view_columns={table:{"deleted":list(all_columns.keys())}}, table=table, view="deleted", admin=True)

@route('/<table>/deleted-items/undelete/<task_id:int>')
def undeleteItem(table, task_id):
    redirect_if_disallowed(table, "undelete", "rw")
    with orm.db_session:
        task = Task[task_id]
        task.deletion_date = None
    redirect("/"+table+"/deleted-items")

@route('/<table>/<view>')
def viewTable(table, view):
    redirect_if_disallowed(table, view)
    if not view_columns.get(table, {}).get(view):
        redirect("/") # if table or view does not exists, redirect to index
    tasks = []
    with orm.db_session:
        tasks = orm.select(t for t in Task if t.table == table and t.deletion_date is None).order_by(lambda: orm.desc(t.update_date))[:]
    tasks = filter_tasks(tasks, table, view)
    return template('index', tasks=tasks, view_columns=allowed_views(), table=table, view=view, writeable=check_acl_allowed(table, view, "write"))

@post('/<table>/<view>/new')
def newTask(table, view):
    redirect_if_disallowed(table, view, "rw")
    with orm.db_session:
        Task(data={k:v for k,v in request.forms.decode('utf-8').items()}, creation_date=datetime.datetime.now(), update_date=datetime.datetime.now(), table=table)
    redirect("/"+table+"/"+view)

@post('/<table>/<view>/update/<task_id:int>')
def updateTask(table, view, task_id):
    redirect_if_disallowed(table, view, "rw")
    with orm.db_session:
        task = Task[task_id]
        task.data.update({k:v for k,v in request.forms.decode('utf-8').items()})
        task.update_date = datetime.datetime.now()
    redirect("/"+table+"/"+view)

@post('/<table>/<view>/delete/<task_id:int>')
def updateTask(table, view, task_id):
    redirect_if_disallowed(table, view, "rw")
    with orm.db_session:
        Task[task_id].deletion_date = datetime.datetime.now()
    redirect("/"+table+"/"+view)

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument('configPath', metavar='configPath',
            help='Path to YML config file')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Should print information and debug messages')
    args = parser.parse_args()

    verbose = args.verbose

    with open(args.configPath, 'r') as ymlFile:
        params = yaml.load(ymlFile)
        verbose = args.verbose
        databasePath = params['database_path']
        view_columns = params['views']
        http_port = params.get('http_port', 80)
        debug = params.get('debug', False)
        view_filters = params.get("filters", {})
        acl = params.get("acl", {})

    db.bind('sqlite', databasePath, create_db=True)
    db.generate_mapping(create_tables=True)
    
    run(host='0.0.0.0', port=http_port, debug=debug)
