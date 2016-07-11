{% extends "base.tpl" %}
{% set ngcontroller = 'analysis' %}
{% block title %} Analyses {% endblock %}

{% block main %}
  <div class="page-title">
    <div class="title_left">
      <h3>Analyzed events </h3>
    </div>

    <div class="title_right">
      <div class="col-md-5 col-sm-5 col-xs-12 form-group pull-right top_search">
        <a href="/analysis/create" class="btn btn-success btn-md" disabled>
          <i class="fa fa-plus"></i> Create analysis
        </a>
      </div>
    </div>
  </div>
  <div class="clearfix"></div>

  <div data-ng-cloak data-ng-if="!analyses || analyses.length == 0" class="alert alert-warning alert-dismissible fade in alert-heading" role="alert">
    No analyses yet
  </div>

  <div data-ng-cloak class="row" data-ng-if="analyses.length > 0">
    <div class="col-md-12">
      <div class="x_panel">
        <div class="x_content">
          <table class="table table-striped projects" data-ng-cloak>
            <thead>
              <tr>
                <th style="width: 20%"> ID </th>
                <th> Date (UTC) </th>
                <th style="width: 25%"> Score </th>
                <th style="text-align: center"> Analysis status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr data-ng-repeat="analysis in analyses track by $index">
                <td>
                  <span> {[ analysis.id ]} </span>
                </td>

                <td>
                  <span> {[ analysis.date | humantime ]} </span>
                </td>

                <td class="project_progress">
                  <div class="progress progress_sm">
                    <div class="progress-bar bg-red" data-transitiongoal="57" role="progressbar"></div>
                  </div>
                  <small>Score unknown</small>
                </td>

                <td class='column-status'>
                  <button class="btn btn-success btn-md btn-round btn-noclick" type="button" data-ng-if="analysis.job_status.state == 'SUCCESS'">
                    <i class="fa fa-check"></i> Success
                  </button>

                  <button class="btn btn-info btn-md btn-round btn-noclick" type="button" data-ng-if="analysis.job_status.state == 'PROGRESS'">
                    <i class="fa fa-refresh fa-spin fa-fw"></i> In progress
                  </button>

                  <button class="btn btn-warning btn-md btn-round btn-noclick" type="button" data-ng-if="analysis.job_status.state == 'PENDING'">
                    <i class="fa fa-hourglass-start"></i> Pending
                  </button>

                  <button class="btn btn-danger btn-md btn-round btn-noclick" type="button" data-ng-if="analysis.job_status.state == 'ERROR'">
                    <i class="fa fa-times"></i> Error
                  </button>
                </td>

                <td>
                  <a class="btn btn-dark btn-md" data-ng-href="/analysis/{[ analysis.id ]}"><i class="fa fa-eye"></i> View </a>
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
      $('li.nav-analysis').addClass('active');
    });
  </script>
{% endblock %}
