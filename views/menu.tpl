    <div id="menu">
        <div class="pure-menu">
            <a class="pure-menu-heading" href="#">Tables</a>
            <ul class="pure-menu-list">
            % for menutable in columns:
                <li class="pure-menu-item {{"menu-item-divided pure-menu-selected" if menutable == table else ""}}"><a href="/{{menutable}}" class="pure-menu-link">{{menutable}}</a></li>
            % end
            </ul>
        </div>
    </div>
