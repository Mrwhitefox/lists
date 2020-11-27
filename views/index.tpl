
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

    % include("menu.tpl", columns=columns, table=table)

    <div id="main">
        <div class="content">
            % if table:
            <p>
            % include("new_form.tpl", columns=columns, table=table)
            </p>

            <p>
            % include("table.tpl", columns=columns, table=table, tasks=tasks)
            </p>
            %end
        </div>
    </div>
</div>

<script src="/static/ui.js"></script>

</body>
</html>

