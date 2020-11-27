<form method="post" action="/{{table}}/new" class="pure-form">
<fieldset>
% for column in columns[table]:
<input type="textarea" name="{{column}}" placeholder="{{column}}"/>
% end
 <input type="submit" class="pure-button pure-button-primary" value="Submit">
 </fieldset>
</form>
