<p><button class="pure-button" style="font-size: xx-small;" onclick="$('#myTable').DataTable().order([[0,'None']]).draw();">Reset filters</button></p>
<table id="myTable" class="pure-table compact row-border hover stripe">
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
<td contenteditable="true" data-col={{c}}>{{! t.getHtml(c)}}</td>
% end
% if not admin and writeable:
<td>
    <button class="pure-button" onclick="submitRowAsForm('{{t.id}}')">✔</button>
    <button class="pure-button delete-button" data-rowid={{t.id}}>X</button>
    
    </td>
% end
</tr>
%end
</tbody>
</table>
