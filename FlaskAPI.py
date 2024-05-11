import asyncio
from flask import Flask, request, jsonify
from JenkinsParser import JenkinsParser

app = Flask(__name__)
jk_instance = JenkinsParser()

async def get_job_status(job_name):
    return await jk_instance.getJobStatus(job_name)
async def build_job(job_name):
    return await jk_instance.buildJob(job_name)
async def create_job(job_name, parameters, description):
    return await jk_instance.createJob(job_name, parameters, description)
async def delete_job(job_name):
    return await jk_instance.deleteJob(job_name)

@app.route("/getJobStatus", methods=["GET"])
def get_job_status_handler():
    job_name = request.args.get('jobName')
    result = asyncio.run(get_job_status(job_name))
    return jsonify(result)

@app.route("/buildJob", methods=["POST"])
def build_job_handler():
    job_name = request.args.get("jobName")
    
    try:
        result = asyncio.run(build_job(job_name))
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/createJob', methods=['POST'])
def create_job_handler():
    data = request.json
    job_name = data.get('job_name')
    parameters = data.get('parameters')
    description = data.get('description', '')

    if not job_name:
        return jsonify({'error': 'Job name is required'}), 400

    try:
        result = asyncio.run(create_job(job_name, parameters, description))
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/deleteJob', methods=['POST'])
def delete_job_handler():
    jobName = request.args.get('jobName')
    try:
        result = asyncio.run(delete_job(jobName))
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    # print(asyncio.run(jk_instance.getJobStatus("test2")))
    # app.run(host="debianpc", port=5000)
    print(asyncio.run(jk_instance.createJob("test1", parameters = {
            'bool_param': {'type': 'Boolean', 'description': 'Boolean параметр', 'defaultValue': 'true'},
            'string_param': {'type': 'String', 'description': 'String параметр', 'defaultValue': 'default_value'}
        }, description="ЭЭЭЭЭЭ")))