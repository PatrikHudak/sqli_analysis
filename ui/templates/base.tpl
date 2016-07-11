<!DOCTYPE html>
<html lang="en" data-ng-app="App">
<head>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
  <meta charset="utf-8">
  <meta content="IE=edge" http-equiv="X-UA-Compatible">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <title>{% block title %} {% endblock %} | SQLi analysis</title>

  <link href="{{ url_for('static', filename='css/bootstrap.min.css') }}" rel="stylesheet">
  <link href="{{ url_for('static', filename='fonts/css/font-awesome.min.css') }}" rel="stylesheet">
  <link href="{{ url_for('static', filename='fonts/css/font-mfizz.css') }}" rel="stylesheet">
  <link href="{{ url_for('static', filename='css/animate.min.css') }}" rel="stylesheet">
  <link href="{{ url_for('static', filename='css/custom.css') }}" rel="stylesheet">
  <link href="{{ url_for('static', filename='css/maps/jquery-jvectormap-2.0.3.css') }}" rel="stylesheet">
  <link href="{{ url_for('static', filename='css/icheck/flat/green.css') }}" rel="stylesheet">
  <link href="{{ url_for('static', filename='css/floatexamples.css') }}" rel="stylesheet">

  {% block stylesheets %} {% endblock %}

  <script src="{{ url_for('static', filename='js/jquery.min.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/nprogress.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/angular.min.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/ng-app.js') }}">
  </script>
</head>
<body class="nav-md">
  <div class="container body">
    <div class="main_container">
      <div class="col-md-3 left_col">
        <div class="left_col scroll-view">
          <div class="navbar nav_title" style="border: 0;">
            <a class="site_title" href="/"><i class="fa fa-user-md"></i> <span>SQLi analysis</span></a>
          </div>
          <div class="clearfix"></div><br>
          <div class="main_menu_side hidden-print main_menu" id="sidebar-menu">
            <div class="menu_section">
              <ul class="nav side-menu">
                <li class="nav-dashboard">
                  <a href="/"><i class="fa fa-signal"></i> Dashboard </a>
                </li>
                <li class="nav-analysis">
                  <a href="/analysis"><i class="fa fa-search"></i> Analysis </a>
                </li>
                <li class="nav-canaries">
                  <a href="/canaries"><i class="fa fa-paper-plane-o"></i> Canaries </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="right_col" role="main" {% if ngcontroller %}data-ng-controller={{ ngcontroller }}{% endif %}>
        {% block main %} {% endblock %}
      </div>
    </div>
  </div>
  <div class="custom-notifications dsp_none" id="custom_notifications">
    <ul class="list-unstyled notifications clearfix" data-tabbed_notifications="notif-group"></ul>
    <div class="clearfix"></div>
    <div class="tabbed_notifications" id="notif-group"></div>
  </div>

  <script src="{{ url_for('static', filename='js/bootstrap.min.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/progressbar/bootstrap-progressbar.min.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/custom.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/icheck/icheck.min.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/notify/pnotify.core.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/notify/pnotify.buttons.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/notify/pnotify.nonblock.js') }}">
  </script>

  <script src="{{ url_for('static', filename='js/moment/moment.min.js') }}">
  </script>

  {% block scripts %} {% endblock %}

  <script> NProgress.done(); </script>
</body>
</html>
