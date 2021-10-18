import yaml, json, html
import datetime
import argparse
from bottle import route, post, run, template, response, request, HTTPError, redirect, static_file
from pony import orm

db = orm.Database()
base_url = "" #will be overidden when conf is loaded

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

def check_acl_allowed(table, view):
    user = request.get_header('User-Agent')
    allowed_groups =  acl.get('restricted_views', {}).get(table, {}).get(view, [])
    if not allowed_groups:
        return True
    return any( [user in acl.get('groups', {}).get(allowed_group, []) for allowed_group in allowed_groups] )


def allowed_views():
    allowed_views = {}
    for table in view_columns:
        allowed_views[table] = {}
        for view in view_columns[table]:
            if check_acl_allowed(table, view):
                allowed_views[table][view] = view_columns[table][view]
    return allowed_views


def filter_tasks(tasks_list, table, view):
    result = []
    column_keywords = view_filters.get(table, "{}").get(view, {})

    if not column_keywords:
        return tasks_list

    for task in tasks_list:
        if any( [any([keyword in task.data.get(column, "") for keyword in column_keywords[column]]) for column in column_keywords]):
            result.append(task)
    return result


@route('/')
def index():
    return template('index', tasks=None, view_columns=allowed_views(), table=None, view=None)

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

@route('/<table>/deleted-items')
def deletedItems(table):
    if not check_acl_allowed(table, "deleted-items"):
        redirect('/')
    tasks = []
    with orm.db_session:
        tasks = orm.select(t for t in Task if t.table == table and t.deletion_date is not None).order_by(lambda: orm.desc(t.update_date))[:]
    all_columns = {}
    for task in tasks:
        all_columns.update(task.data)
    
    return template('index', tasks=tasks, view_columns={table:{"deleted":list(all_columns.keys())}}, table=table, view="deleted", admin=True)

@route('/<table>/deleted-items/undelete/<task_id:int>')
def undeleteItem(table, task_id):
    if not check_acl_allowed(table, "undelete"):
        redirect('/')
    with orm.db_session:
        task = Task[task_id]
        task.deletion_date = None
    redirect("/"+table+"/deleted-items")


@route('/<table>/<view>')
def viewTable(table, view):
    if not check_acl_allowed(table, view):
        redirect('/')

    if not view_columns.get(table, {}).get(view):
        # if table or view does not exists, redirect to index
        redirect("/")
    tasks = []
    with orm.db_session:
        tasks = orm.select(t for t in Task if t.table == table and t.deletion_date is None).order_by(lambda: orm.desc(t.update_date))[:]
    tasks = filter_tasks(tasks, table, view)
    return template('index', tasks=tasks, view_columns=view_columns, table=table, view=view)

@post('/<table>/<view>/new')
def newTask(table, view):
    if not check_acl_allowed(table, view):
        redirect('/')
    data = {}
    for key, value in request.forms.decode('utf-8').items():
        data[key] = value

    with orm.db_session:
        Task(data=data, creation_date=datetime.datetime.now(), update_date=datetime.datetime.now(), table=table)
    redirect("/"+table+"/"+view)

@post('/<table>/<view>/update/<task_id:int>')
def updateTask(table, view, task_id):
    if not check_acl_allowed(table, view):
        redirect('/')
    with orm.db_session:
        task = Task[task_id]
        for key, value in request.forms.decode('utf-8').items():
            task.data[key] = value
        task.update_date = datetime.datetime.now()
    redirect("/"+table+"/"+view)

@post('/<table>/<view>/delete/<task_id:int>')
def updateTask(table, view, task_id):
    if not check_acl_allowed(table, view):
        redirect('/')
    with orm.db_session:
        Task[task_id].deletion_date = datetime.datetime.now()
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
        view_columns = params['views']
        view_filters = params.get("filters", {})
        acl = params.get("acl", {})

    db.bind('sqlite', databasePath, create_db=True)
    db.generate_mapping(create_tables=True)
    
    run(host='0.0.0.0', port=http_port, debug=debug)
