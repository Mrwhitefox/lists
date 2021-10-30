<table id="myTable" class="compact row-border hover stripe">
<thead>
<tr>
% if admin:
<th>id</th>
<th>creation date</th>
<th>update date</th>
<th>deletion date</th>
<th>undelete</th>
% end
% for col in view_columns[table][view]:
<th class="sorting">{{col}}</th>
% end
% if not admin and writeable:
<th></th>
% end
</tr>
</thead>
<tbody>
%for t in tasks:
<tr id="{{t.id}}">
% if admin:
<td>{{str(t.id)}}</td>
<td>{{str(t.creation_date)}}</td>
<td>{{str(t.update_date)}}</td>
<td>{{str(t.deletion_date)}}</td>
<td><a href=/{{table}}/deleted-items/undelete/{{t.id}}>undelete</a></td>
% end
% for c in view_columns[table][view]:
<td contenteditable="{{writeable}}" data-col={{c}}>{{! t.getHtml(c)}}</td>
% end
% if not admin and writeable:
<td title="Id: {{t.id}}&#10;Created: {{t.creation_date}}&#10;Updated: {{t.update_date}}">
    <button class="pure-button small-button" onclick="submitRowAsForm('{{t.id}}')">✔</button>
    <button class="pure-button delete-button small-button" data-rowid={{t.id}}>X</button>
    
    </td>
% end
</tr>
%end
</tbody>
</table>
