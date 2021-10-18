    <div id="menu">
        <div class="pure-menu">
            <a class="pure-menu-heading" href="#">Tables</a>
            <ul class="pure-menu-list">
            % for menutable in view_columns:
            % for menuview in view_columns[menutable]:
                <li class="pure-menu-item {{"menu-item-divided pure-menu-selected" if menutable == table and menuview == view else ""}}"><a href="/{{menutable}}/{{menuview}}" class="pure-menu-link">{{menutable}} - {{menuview}}</a></li>
            % end
            % end
            </ul>
        </div>
    </div>
