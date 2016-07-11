{% extends "base.tpl" %}
{% set ngcontroller = 'dashboard' %}
{% block title %} Dashboard {% endblock %}

{% block main %}
  <div class="row tile_count" data-ng-cloak>
    <div class="animated flipInY col-md-2 col-sm-4 col-xs-4 tile_stats_count">
      <div class="left"></div>
      <div class="right">
        <span class="count_top"><i class="fa fa-search"></i> Total Analyses</span>
        <div class="count">
          {[ dashboard.analysis_count ]}
        </div>
      </div>
    </div>
    <div class="animated flipInY col-md-2 col-sm-4 col-xs-4 tile_stats_count">
      <div class="left"></div>
      <div class="right">
        <span class="count_top"><i class="fa fa-check"></i> Successful </span>
        <div class="count green">
          {[ dashboard.success_count ]}
        </div>
      </div>
    </div>
    <div class="animated flipInY col-md-2 col-sm-4 col-xs-4 tile_stats_count">
      <div class="left"></div>
      <div class="right">
        <span class="count_top"><i class="fa fa-spinner"></i> In progress </span>
        <div class="count blue">
          {[ dashboard.progress_count ]}
        </div>
      </div>
    </div>
    <div class="animated flipInY col-md-2 col-sm-4 col-xs-4 tile_stats_count">
      <div class="left"></div>
      <div class="right">
        <span class="count_top"><i class="fa fa-hourglass-start"></i> Pending </span>
        <div class="count yellow">
          {[ dashboard.pending_count ]}
        </div>
      </div>
    </div>
    <div class="animated flipInY col-md-2 col-sm-4 col-xs-4 tile_stats_count">
      <div class="left"></div>
      <div class="right">
        <span class="count_top"><i class="fa fa-times"></i> Errors </span>
        <div class="count red">
          {[ dashboard.error_count ]}
        </div>
      </div>
    </div>
    <div class="animated flipInY col-md-2 col-sm-4 col-xs-4 tile_stats_count">
      <div class="left"></div>
      <div class="right">
        <span class="count_top"><i class="fa fa-clock-o"></i> Avg analysis time </span>
        <div class="count">
          {[ dashboard.exec_time ]} sec
        </div>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12 col-sm-12 col-xs-12">
      <div class="dashboard_graph">
        <div class="row x_title">
          <div class="col-md-6">
            <h3>Analysis activity <small>Past 7 days</small></h3>
          </div>
        </div>
        <div class="col-md-12 col-sm-12 col-xs-12">
          <div class="demo-placeholder" id="placeholder33" style="height: 260px; display: none"></div>
          <div style="width: 100%;">
            <div class="demo-placeholder" id="canvas_dahs" style="width: 100%; height:270px;"></div>
          </div>
        </div>
        <div class="clearfix"></div>
      </div>
    </div>
  </div>
{% endblock %}

{% block scripts %}
  <script>
    $(document).ready(function() {
      $('li.nav-dashboard').addClass('active');
    });
  </script>

  <script src="{{ url_for('static', filename='js/flot/jquery.flot.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/flot/jquery.flot.time.min.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/graphs.js') }}">
  </script>
{% endblock %}
