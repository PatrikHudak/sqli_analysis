{% extends "base.tpl" %}
{% block stylesheets %}
<link href="{{ url_for('static', filename='css/vis.min.css') }}" rel="stylesheet">
{% endblock %}
{% block title %} Analysis {{ id }} {% endblock %}

{% block main %}
<div class="page-title">
  <div class="row">
    <div class="title_left col-md-8">
        <h3>Analysis <strong>{{ id }}</strong></h3>
    </div>

    <div class="title_right col-md-4">
        <div class="btn-group pull-right">
          {% if job_status.state == 'SUCCESS' and pcap_exists(pcap_file) %}
          <a href="/api/pcap/{{ pcap_file }}" class="btn btn-primary btn-md">
            <i class="fa fa-download"></i> Download PCAP
          </a>
          {% else %}
          <a href="#" class="btn btn-primary btn-md" disabled>
            <i class="fa fa-download"></i> PCAP unavailable
          </a>
          {% endif %}
          <a href="/api/analysis/{{ id }}" class="btn btn-default btn-md">
            <i class="fa fa-download"></i> Download JSON
          </a>
      </div>
    </div>
  </div>
</div>
<div class="clearfix"></div>

{% if job_status.state == 'ERROR' or 'error' in job_status %}
<div class="alert alert-danger alert-dismissible fade in alert-heading" role="alert">
  <strong>Error!</strong> {{ job_status['error'] }}
</div>
{% endif %}

<div class="row">
  <div class="col-md-6">
    <div class="x_panel">
      <div class="x_content">
        <h2> General </h2>
        <table class="table analysis-results">
          <tbody>
            <tr>
              <th scope="row"> Timestamp </th>
              <td> {{ date | arrow_format }} </td>
            </tr>
            <tr>
              <th scope="row"> Status </th>
              <td>
              {% if job_status.state == 'SUCCESS' %}
              <button type="button" class="btn btn-success btn-xs btn-noclick"> <i class="fa fa-check"></i> Success </button>
              {% elif job_status.state == 'PROGRESS' %}
              <button type="button" class="btn btn-info btn-xs btn-noclick"> <i class="fa fa-refresh fa-spin fa-fw"></i> In progress </button>
              {% elif job_status.state == 'PENDING' %}
              <button type="button" class="btn btn-warning btn-xs btn-noclick"> <i class="fa fa-hourglass-start"></i> Pending </button>
              {% else %}
              <button type="button" class="btn btn-danger btn-xs btn-noclick"> <i class="fa fa-times"></i> Error </button>
              {% endif %}
              </td>
            </tr>
            {% if job_status.state == 'SUCCESS' %}
            <tr>
              <th scope="row"> Analysis time </th>
              <td> {{ exec_time }} seconds </td>
            </tr>
            {% endif %}

            {% if job_status.state == 'PENDING' %}
            <tr>
              <th scope="row"> Scheduled on </th>
              <td> {{ job_status.eta | arrow_format }} </td>
            </tr>
            {% endif %}

          </tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="col-md-6">
    <div class="x_panel">
      <div class="x_content">
        <h2> Alert </h2>
        <table class="table analysis-results">
          <tbody>
            <tr>
              <th scope="row"> Timestamp </th>
              <td> {{ alert['details'].timestamp | arrow_format }} </td>
            </tr>

            <tr>
              <th scope="row"> Detection source </th>
              <td> <strong>Snort</strong> (IDS) </td>
            </tr>

            <tr>
              <th scope="row"> Count </th>
              <td> {{ alert['count'] }} </td>
            </tr>

            <tr>
              <th scope="row"> Source </th>
              <td> {{ alert['details'].src_ip }} </td>
            </tr>

            <tr>
              <th scope="row"> Target </th>
              <td> {{ alert['details'].dest_ip }}:{{ alert['details'].dest_port }} </td>
            </tr>

            {% if alert['details'].detection == 'snort' %}
            <tr>
              <th scope="row"> Metadata </th>
              <td>
                <table class="table table-striped">
                  <tbody>
                    <tr>
                      <th scope="row"> GID:SID:REV </th>
                      <td> {{ alert['details'].meta.gid }}:{{ alert['details'].meta.sid }}:{{ alert['details'].meta.rev }} </td>
                    </tr>

                    <tr>
                      <th scope="row"> Description </th>
                      <td>
                        {% if 'description' in alert['details'].meta %}
                          {% if 'reference' in alert['details'].meta and alert['details'].meta.reference %}
                            <a href="{{ alert['details'].meta.reference }}"> {{ alert['details'].meta.description }} </a>
                          {% else %}
                            {{ alert['details'].meta.description }}
                          {% endif %}
                        {% else %}
                          <em> No SID mapping </em>
                        {% endif %}
                      </td>
                    </tr>
                    {% if 'classification' in alert['details'].meta %}
                    <tr>
                      <th scope="row"> Classification </th>
                      <td> {{ alert['details'].meta.classification }} </td>
                    </tr>
                    {% endif %}
                  </tbody>
                </table>
              </td>
            </tr>
            {% endif %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

{% if job_status.state == 'SUCCESS' %}
<div class="row analysis-tabs">
  <div class="col-md-12">
    <div class="x_panel">
      <div class="x_content">
        <h3> Modules output </h3>
        <div class="col-md-12 col-sm-12 col-xs-12">
          <div class="" data-example-id="togglable-tabs" role="tabpanel">
            <ul class="nav nav-tabs bar_tabs" role="tablist">
              {% if 'ipinfo' in results %}
              <li class="active" role="presentation">
                <a data-toggle="tab" href="#ipinfo" role="tab"> ipinfo </a>
              </li>
              {% endif %}

              {% if 'canary' in results %}
              <li role="presentation">
                <a data-toggle="tab" href="#canary" role="tab"> canary </a>
              </li>
              {% endif %}

              {% if 'websiteinfo' in results %}
              <li role="presentation">
                <a data-toggle="tab" href="#websiteinfo" role="tab"> websiteinfo </a>
              </li>
              {% endif %}

              {% if 'connections' in results %}
              <li role="presentation">
                <a data-toggle="tab" href="#connections" role="tab"> connections </a>
              </li>
              {% endif %}
              <li role="presentation">
                <a data-toggle="tab" href="#statistics" role="tab"> statistics </a>
              </li>
            </ul>

            <div class="tab-content">
              {% if 'ipinfo' in results %}
              <div class="tab-pane fade active in" id="ipinfo" role="tabpanel">
                {% if 'error' in results['ipinfo'] and 'RFC 1918' in results['ipinfo']['error'] %}
                <div class="alert alert-warning alert-dismissible fade in" role="alert">
                  Source IP address is a Private IP address.
                </div>
                {% elif 'error' in results['ipinfo'] %}
                <div class="alert alert-danger alert-dismissible fade in" role="alert">
                  <strong>Error!</strong> {{ results['ipinfo']['error'] }}
                </div>
                {% else %}
                {% if results['ipinfo']['is_tor'] == false %}
                <div class="alert alert-info alert-dismissible fade in" role="alert">
                  Source IP address doesn't seem to be a Tor exit node
                </div> 
                {% elif results['ipinfo']['is_tor'] == true %}
                <div class="alert alert-danger alert-dismissible fade in" role="alert">
                  <strong> Source IP address seems to be a Tor exit node! </strong>
                </div> 
                {% endif %}
                <table class="table">
                  <tbody>
                    <tr>
                      <th scope="row"> IP address </th>
                      <td> {{ alert['details'].src_ip  }} </td>
                    </tr>
                    <tr>
                      <th scope="row"> CIDR </th>
                      <td> {{ results['ipinfo']['cidr'] }} </td>
                    </tr>
                    <tr>
                      <th scope="row"> Country </th>
                      <td> {{ results['ipinfo']['country'] }} </td>
                    </tr>
                    <tr>
                      <th scope="row"> ISP </th>
                      <td> {{ results['ipinfo']['isp'] }} </td>
                    </tr>
                    <tr>
                      <th scope="row"> Abuse contact </th>
                      <td> 
                        <a target="_blank" href="mailto:{{ results['ipinfo']['abuse'] }}">
                          {{ results['ipinfo']['abuse'] }}
                        </a> 
                      </td>
                    </tr>
                    <tr>
                      <th scope="row"> ASN </th>
                      <td>
                        <a target="_blank" href="https://mxtoolbox.com/SuperTool.aspx?action=asn%3aas{{ results['ipinfo']['asn']}}&run=toolpage">
                          {{ results['ipinfo']['asn'] }}
                        </a> 
                      </td>
                    </tr>
                  </tbody>
                </table>
              {% endif %}
              </div>
              {% endif %}

              {% if 'canary' in results %}
              <div class="tab-pane fade in" id="canary" role="tabpanel">
                {% if results['canary']['found'] %}
                <div class="alert alert-success alert-dismissible fade in" role="alert">
                  <strong>Database canary found! </strong><em>({{ results['canary']['found'] }})</em>
                </div>
                {% else %}
                <div class="alert alert-info alert-dismissible fade in" role="alert">
                  Database canary not found.
                </div>
                {% endif %}
              </div>
              {% endif %}

              {% if 'websiteinfo' in results %}
              <div class="tab-pane fade" id="websiteinfo" role="tabpanel">
                {% if 'error' in results['websiteinfo'] %}
                <div class="alert alert-danger alert-dismissible fade in" role="alert">
                  <strong>Error!</strong> {{ results['websiteinfo']['error'] }}
                </div>
                {% else %}
                <h4> Detected technologies on <em>{{ alert['details'].dest_ip }}:{{ alert['details'].dest_port }}</em></h4>
                <table class="table table-striped">
                  <tbody>
                    {% for tech in results['websiteinfo']['technologies'] %}
                      <tr>
                        <td>
                          {% if tech.lower() == 'apache' %}
                          <i class="icon-apache"></i>
                          {% elif tech.lower() == 'php' %}
                          <i class="icon-php-alt"></i>
                          {% elif tech.lower() == 'ubuntu' %}
                          <i class="icon-ubuntu"></i>
                          {% elif tech.lower() == 'nginx' %}
                          <i class="icon-nginx"></i>
                          {% elif tech.lower() == 'debian' %}
                          <i class="icon-debian"></i>
                          {% elif tech.lower() == 'red hat' %}
                          <i class="icon-redhat"></i>
                          {% elif tech.lower() == 'fedora' %}
                          <i class="icon-fedora"></i>
                          {% elif tech.lower() == 'mysql' %}
                          <i class="icon-mysql"></i>
                          {% elif tech.lower() == 'iis' %}
                          <i class="fa fa-windows"></i>
                          {% else %}
                          <i class="fa fa-cog"></i>
                          {% endif %}
                          {{ tech }}
                        </td>
                      </tr>
                    {% endfor %}
                  </tbody>
                </table>
                {% endif %}
              </div>
              {% endif %}

              {% if 'connections' in results %}
              <div class="tab-pane fade in" id="connections" role="tabpanel">
                {% if 'error' in results['connections'] %}
                <div class="alert alert-danger alert-dismissible fade in" role="alert">
                  <strong>Error!</strong> {{ results['connections']['error'] }}
                </div>
                {% else %}
                <div id="moloch_connections"></div>
                <script>
                  $(function() {
                    var container = document.getElementById('moloch_connections');
                    var nodes = {{ results['connections']['nodes']|tojson|safe }};
                    var edges = {{ results['connections']['edges']|tojson|safe }};

                    var data = {
                      nodes: new vis.DataSet(nodes),
                      edges: new vis.DataSet(edges)
                    };

                    var options = {
                      nodes: {borderWidth: 2},
                      interaction: {hover: true},
                      autoResize: true,
                      width: '100%',
                      height: '100%'
                    };

                    moloch_connections = new vis.Network(container, data, options);
                  });

                  $('a[href="#connetions"]').click(function() {
                    moloch_connections.fit();
                  });
                </script>
                {% endif %}
              </div>
              {% endif %}

              {% if 'statistics' in results %}
              <div class="tab-pane fade in" id="statistics" role="tabpanel">
                {% if 'error' in results['statistics'] %}
                <div class="alert alert-danger alert-dismissible fade in" role="alert">
                  <strong>Error!</strong> {{ results['statistics']['error'] }}
                </div>
                {% else %}
                <div class="row">
                  <div class="col-md-6">
                    <div class="x_panel">
                      <div class="x_content">
                        <h4> Endpoints </h4>
                        <table class="table table-striped">
                          <tbody>
                            {% for endpoint in results['statistics']['endpoints'] %}
                            <tr>
                              <th scope="row" style="width: 70%"> {{ endpoint[0] }} </th>
                              <td> {{ endpoint[1] * 100 }}% </td>
                            </tr>
                            {% endfor %}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="x_panel">
                      <div class="x_content">
                        <h4> MIME types </h4>
                        <table class="table table-striped">
                          <tbody>
                            {% for mime in results['statistics']['mime'] %}
                            <tr>
                              <th scope="row" style="width: 70%"> {{ mime[0] }} </th>
                              <td> {{ mime[1] * 100 }}% </td>
                            </tr>
                            {% endfor %}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="x_panel">
                      <div class="x_content">
                        <h4> User agents </h4>
                        <table class="table table-striped">
                          <tbody>
                            {% for user_agent in results['statistics']['user_agents'] %}
                            <tr>
                              <th scope="row" style="width: 70%"> {{ user_agent[0] }} </th>
                              <td> {{ user_agent[1] * 100 }}% </td>
                            </tr>
                            {% endfor %}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
                {% endif %}
              </div>
              {% endif %}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
{% endif %}

{% endblock %}

{% block scripts %}
  <script src="{{ url_for('static', filename='js/vis.min.js') }}">
  </script>

  <script>
    $(document).ready(function() {
      $('li.nav-analysis').addClass('active');
    });
  </script>
{% endblock %}
