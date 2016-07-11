# -*- coding: utf-8 -*-

import json
import os
import random
import string

import arrow
import flask
import rethinkdb as r
from flask.ext.cors import CORS

import engine

app = flask.Flask(__name__, template_folder='ui/templates', static_folder='ui/static')
CORS(app)

# Loads configuration file into dictionary
with open('config.json') as fr:
	global config
	config = json.loads(fr.read())

# Define Jinja globals and filters
def pcap_exists(pcap_filename):
	""" Checks whether PCAP is available on the filesystem """
	return os.access(os.path.join(config['pcap_directory'], pcap_filename), os.F_OK & os.R_OK)

def arrow_humanize(timestamp):
	""" Humanize time (e.g. Today at 8:40pm) """
	return arrow.get(timestamp).humanize()

def arrow_format(timestamp):
	""" Convert arrow time to iso8601 """
	return arrow.get(timestamp).format()

app.jinja_env.globals.update(pcap_exists=pcap_exists)
app.jinja_env.filters.update(arrow_humanize=arrow_humanize,
							arrow_format=arrow_format)

@app.before_request
def before_request():
	""" Creates database connection before executing endpoint handler """
	try:
		flask.g.rdb_conn = r.connect(	host=config['rethinkdb']['host'],
										port=config['rethinkdb']['port'],
										db=config['rethinkdb']['db'])
	except(r.RqlDriverError, ):
		flask.abort(503, 'Database connection error')

@app.teardown_request
def after_request(Exception):
	""" Closes database connection after handler execution """
	try:
		flask.g.rdb_conn.close()
	except (AttributeError, ):
		flask.abort(503, 'Database connection error')

# ~~~~~ UI endpoints ~~~~~
@app.route('/')
def dashboard():
	""" Renders dashboard page """ 
	return flask.render_template('dashboard.tpl')

@app.route('/analysis')
def analysis_list():
	""" Renders analyses listing page """
	return flask.render_template('analysis.tpl')

@app.route('/analysis/create')
def analysis_create():
	""" Renders analysis creation page """
	return flask.render_template('analysis_creation.tpl')

@app.route('/analysis/<task_id>')
def analysis_show(task_id):
	""" Renders analysis result page """
	analysis = r.table('analysis').get(task_id).run(flask.g.rdb_conn)
	if not analysis:
		flask.abort(404, 'Analysis not found.')
	return flask.render_template('analysis_result.tpl', **analysis)

@app.route('/canaries')
def canaries():
	""" Renders canaries page """
	return flask.render_template('canaries.tpl')

# ~~~~~ API endpoints ~~~~~
@app.route('/api/dashboard')
def api_dashboard():
	""" Returns data for dashboards """

	# Get data for timeline
	analysis_count_graph = []
	for i in range(7):
		start = arrow.utcnow().replace(days=-i).floor('day').timestamp
		end = arrow.utcnow().replace(days=-i).ceil('day').timestamp
		count = r.table('analysis').filter((r.row['date'] < r.epoch_time(end)) & (r.row['date'] > r.epoch_time(start))).count().run(flask.g.rdb_conn)
		# JavaScript Date object expects timestamp * 1000
		analysis_count_graph.append([(start * 1000), count])

	return flask.jsonify(
		analysis_graph=analysis_count_graph[::-1],
		analysis_count=r.table('analysis').count().run(flask.g.rdb_conn),
		success_count=r.table('analysis').filter(r.row['job_status']['state'] == 'SUCCESS').count().run(flask.g.rdb_conn),
		progress_count=r.table('analysis').filter(r.row['job_status']['state'] == 'PROGRESS').count().run(flask.g.rdb_conn),
		pending_count=r.table('analysis').filter(r.row['job_status']['state'] == 'PENDING').count().run(flask.g.rdb_conn),
		error_count=r.table('analysis').filter(r.row['job_status']['state'] == 'ERROR').count().run(flask.g.rdb_conn),
		exec_time=round(r.table('analysis').avg('exec_time').default(0).run(flask.g.rdb_conn))
	)

@app.route('/api/analysis')
def api_analysis_list():
	""" Returns list of all analyses with basic details """
	analyses = r.table('analysis').order_by(r.desc('date')).run(flask.g.rdb_conn)

	filtered = []
	for analysis in analyses:
		filtered.append({
			'id': analysis['id'],
			'job_status': analysis['job_status'],
			'date': arrow.get(analysis['date']).format()
		})

	return flask.jsonify(analyses=filtered)

@app.route('/api/analysis/<task_id>')
def get_analysis(task_id):
	""" Returns analysis details for analysis with id of task id """
	analysis = r.table('analysis').get(task_id).run(flask.g.rdb_conn)
	if not analysis:
		flask.abort(404, 'Analysis not found.')
	return flask.jsonify(**analysis)

@app.route('/api/analysis', methods=['POST'])
def create_analysis():
	""" Processes the alert + creates an analysis when necessary """
	analysis_data = flask.request.get_json()
	if any(key not in analysis_data for key in ['src_ip', 'dest_ip', 'dest_port', 'detection', 'timestamp']):
		flask.abort(500, 'Bad format of input data')

	aggregate = False
	alert_tuple = (analysis_data['src_ip'], analysis_data['dest_ip'], analysis_data['dest_port'])
	for progress in r.table('analysis').filter(r.row['job_status']['state'] == 'PENDING').run(flask.g.rdb_conn):
		if (progress['alert']['details']['src_ip'], progress['alert']['details']['dest_ip'], progress['alert']['details']['dest_port']) == alert_tuple:
			aggregate = progress['id']
			break

	# Create `analysis` table if necessary
	if 'analysis' not in r.table_list().run(flask.g.rdb_conn):
		r.table_create('analysis').run(flask.g.rdb_conn)

	if not aggregate:
		# Alert creates a new analysis
		analysis = {}
		job = engine.analyze.apply_async((analysis_data, ), countdown=config['job_freeze'])
		analysis['id'] = job.task_id
		analysis['job_freeze'] = config['job_freeze']
		analysis['date'] = r.now()
		analysis['alert'] = {
			'details': analysis_data,
			'count': 1
		}
		analysis['job_status'] = {
			'state': 'PENDING',
			'eta': r.iso8601(str(arrow.utcnow().replace(seconds=config['job_freeze'])))
		}
		
		r.table('analysis').insert(analysis).run(flask.g.rdb_conn)
		return flask.jsonify(job_id=job.task_id)
	else:
		# Alert is aggregated to the existing analysis
		r.table('analysis').get(aggregate).update({'alert': {'count': r.row['alert']['count'].add(1)}}).run(flask.g.rdb_conn)
		return flask.jsonify(job_id=aggregate)

@app.route('/api/pcap/<pcap_filename>')
def download_pcap(pcap_filename):
	""" Returns PCAP with pcap filename filename """
	if pcap_exists(pcap_filename):
		return flask.send_from_directory(directory=config['pcap_directory'], filename=pcap_filename)
	flask.abort(404, 'PCAP not found.')

@app.route('/api/canary')
def api_canary_list():
	""" Returns list of generated canaries """
	return flask.jsonify(canaries=list(r.table('canary').order_by(r.desc('date')).run(flask.g.rdb_conn)))

@app.route('/api/canary', methods=['POST'])
def generate_canary():
	""" Generates new canary string """
	canary = ''.join(random.SystemRandom().choice('abcdef' + string.digits) for _ in range(64))

	if 'canary' not in r.table_list().run(flask.g.rdb_conn):
		r.table_create('canary').run(flask.g.rdb_conn)

	r.table('canary').insert({'date': r.now(), 'canary': canary}).run(flask.g.rdb_conn)
	return flask.jsonify(canary=canary)

@app.route('/api/canary/<canary>', methods=['POST'])
def remove_canary(canary):
	""" Deletes canary string canary """
	if not r.table('canary').filter({'canary': canary}).run(flask.g.rdb_conn):
		return flask.abort(404, 'Canary does not exist')
	r.table('canary').filter({'canary': canary}).delete().run(flask.g.rdb_conn)
	return flask.jsonify(status='ok')

if __name__ == '__main__':
	# If run directly without uWSGI
	app.run('0.0.0.0', port=8000, debug=True)
