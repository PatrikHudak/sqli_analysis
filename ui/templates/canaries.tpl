{% extends "base.tpl" %}
{% set ngcontroller = 'canaries' %}
{% block title %} Canaries {% endblock %}

{% block main %}
  <div class="page-title">
    <div class="title_left">
      <h3> Generated canaries </h3>
    </div>

    <div class="title_right">
      <div class="col-md-5 col-sm-5 col-xs-12 form-group pull-right top_search">
        <button class="btn btn-success btn-md" data-ng-click="createCanary()">
          <i class="fa fa-plus"></i> Create canary
        </button>
      </div>
    </div>
  </div>
  <div class="clearfix"></div>

  <div data-ng-if="created_canary" class="alert alert-info alert-dismissible fade in alert-heading" role="alert">
    Canary <strong>{[ created_canary ]}</strong> created.
  </div>

  <div data-ng-if="canaries.length == 0" class="alert alert-warning alert-dismissible fade in alert-heading" role="alert">
    No canaries yet
  </div>

  <div class="row" data-ng-if="canaries.length > 0">
    <div class="col-md-12">
      <div class="x_panel">
        <div class="x_content">
          <table class="table table-striped projects" data-ng-cloak>
            <thead>
              <tr>
                <th> Creation date (UTC) </th>
                <th> Canary </th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr data-ng-repeat="canary in canaries track by $index">
                <td>
                  <span> {[ canary.date | humantime ]} </span>
                </td>

                <td class="project_progress">
                  <strong> {[ canary.canary ]}
                </td>

                <td>
                  <button class="btn btn-danger btn-md" data-ng-click="deleteCanary(canary.canary)">
                    <i class="fa fa-trash"></i> Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
{% endblock %}

{% block scripts %}
  <script>
    $(document).ready(function() {
      $('li.nav-canaries').addClass('active');
    });
  </script>
{% endblock %}
