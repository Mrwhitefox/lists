<form method="post" action="/{{table}}/{{view}}/new" class="pure-form">
<fieldset>
% for column in view_columns[table][view]:
<input type="textarea" name="{{column}}" placeholder="{{column}}"/>
% end
 <input type="hidden" name="lists_internal_view" value="{{view}}">
 <input type="submit" class="pure-button pure-button-primary" value="Submit">
 </fieldset>
</form>
