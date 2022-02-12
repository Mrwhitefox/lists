
% import json
% import datetime
% last_week_date = datetime.date.today() - datetime.timedelta(days=7)
% ts_start = gantts[table][view]["col-start"]
% ts_end = gantts[table][view]["col-end"]
% ts_desc = gantts[table][view]["col-description"]

% ts_elts = []
% for t in tasks :
  % if t.data.get(ts_start) and t.data.get(ts_end) and t.data.get(ts_desc):
  % ts_elts.append( [t.id, t.data.get(ts_start).replace("\r\n",""), t.data.get(ts_end).replace("\r\n",""), t.data.get(ts_desc).replace("\r\n","")])
  % end
% end


<script type="text/javascript">
   // google.charts.load('current', {'packages':['gantt'], 'language': 'fr'});
    //google.charts.setOnLoadCallback(drawChart);
    
$(document).ready(
    function drawChart() {

      var data = new google.visualization.DataTable();

      data.addColumn('string', 'Task ID');
      data.addColumn('string', 'Task Name');
      data.addColumn('date', 'Start Date');
      data.addColumn('date', 'End Date');
      data.addColumn('number', 'Duration');
      data.addColumn('number', 'Percent Complete');
      data.addColumn('string', 'Dependencies');


% for t in tasks :
  % if t.data.get(ts_start) and t.data.get(ts_end) and t.data.get(ts_desc):
    data.addRows([[ "{{t.id}}", "{{t.data.get(ts_desc).replace("\r\n","")}}",  new Date("{{t.data.get(ts_start).replace("\r\n","")}}"), new Date("{{ t.data.get(ts_end).replace("\r\n","")}}"), null, null, null]]);
  % end
% end


      var options = {
        gantt: {
            labelStyle: {
                color: 'red'
            },
            percentEnabled: false,
            criticalPathEnabled: false
        }
      };

      var chart = new google.visualization.Gantt(document.getElementById('chart_div'));

      chart.draw(data, options);
    }
    );
  </script>

<div id="chart_div" ></div>
