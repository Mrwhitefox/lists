%setdefault('admin', False)
%setdefault('writeable', False)

<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/pure.min.css">
    <link rel="stylesheet" href="/static/index.css">
% include('headers.tpl')
</head>
<body>

<div id="layout">
    <!-- Menu toggle -->
    <a href="#menu" id="menuLink" class="menu-link">
        <!-- Hamburger icon -->
        <span></span>
    </a>

    % include("menu.tpl", view_columns=view_columns, table=table, view=view)

    <div id="main">
        <div class="content">
            % if table:
            % if writeable:
            <p>
            % include("new_form.tpl", view_columns=view_columns, table=table, view=view)
            </p>
            % end
            <p>
            % include("table.tpl", view_columns=view_columns, table=table, view=view, tasks=tasks, admin=admin, writeable=writeable)
            </p>
            % end
        </div>
    </div>
</div>

<script src="/static/ui.js"></script>

</body>
</html>

