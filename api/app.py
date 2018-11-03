import os
import re

import sys
import subprocess

from flask import Flask, Response, url_for, render_template, send_from_directory
from flask import request
from flask import json

import hashlib
import logging

import logging.config

from werkzeug.utils import redirect

# logging.config.fileConfig('logger.conf')
print("Starting Smart Invoice Hack ")

BASE = 36
BLOCK_SIZE = 4
DISCRETE_VALUES = BASE ** BLOCK_SIZE

UPLOAD_FOLDER = '/tmp/rdisk'
ALLOWED_EXTENSIONS = set(['csv'])

#
# The entry point
#
app = Flask(__name__)


#
# default response. we could make it fancy
#
@app.route("/")
def index():
    return Response("Welcome to Smart Invoice Hack v0.0.1"), 200


@app.route('/<name>')
def hello_name(name):
    return "No service found for {}!".format(name)


#
# generate a random file name
#
def uniq_id(output_path, content):
    # orig = datetime.now().strftime("%m%d%H%M%S_") + "{0:04d}".format(random.randint(0, 10000))
    # masked_id = mask_with_hsa(orig)
    #
    # switch to use md5. This will help to group the same uploads together,
    # especially when people test the service with that awesome_invoice.pdf on the web site.
    # Truncate the hash to 16 character to make it shorter, but add length to reduce collision
    #
    masked_id = hashlib.md5(content.encode('utf-8')).hexdigest()
    masked_id = masked_id[0:16] + "_" + str(len(content))
    fan_out_012 = masked_id[0:3]   # first three letters
    fan_out_345 = masked_id[3:6]   # second three letters

    target_folder = "{}/{}/{}/{}".format(output_path, fan_out_012, fan_out_345, masked_id)
    if not os.path.isdir(target_folder):
        os.makedirs(target_folder)
    return target_folder, masked_id


def allowed_file(filename):
    # this has changed from the original example because the original did not work for me
    return filename[-3:].lower() in ALLOWED_EXTENSIONS


def extract_intents(request):

    # if behind a proxy
    ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    if ip is None:
        ip = request.environ['REMOTE_ADDR']
    if ip is None:
        ip = request.remote_addr

    if request.method != 'POST':
        print('Invalid method - ' + request.method + ' - ' + ip)
        return 'Invalid method - ' + request.method, 400

    # if request.headers['Content-Type'] != 'application/json':
    #     print('Invalid content - ' + request.headers['Content-Type'] + ' - ' + ip)
    #     return 'Invalid content', 415

    # if request.data is None:
    #     print('Invalid content - no data' + ' - ' + ip)
    #     return 'Invalid content', 422

    file = request.files['file']
    if file and not allowed_file(file.filename):
        print('Invalid content type - ' + request.method + ' - ' + ip)
        return 'Invalid content type - ' + request.method, 400

    cl = request.content_length
    if cl is not None and cl > 100 * 1024 * 1024:
        print('Invalid content length exceed the limit' + ' - ' + ip)
        return 'Invalid content', 413

    #
    # add all parameters to form a proxy of the content. Eventually, we use it to get an unique id
    #
    content = {
        'length': cl,
    }
    content_str = json.dumps(content)
    target_folder, file_id = uniq_id(UPLOAD_FOLDER, content_str)
    input_file_name = file_id + '_all.csv'
    input_file = os.path.join(target_folder, input_file_name)
    file.save(input_file)

    return target_folder, input_file, file_id


@app.route('/extract/<oid>', methods=['GET'])
def output(oid=None):

    fan_out_012 = oid[0:3]   # first three letters
    fan_out_345 = oid[3:6]   # second three letters

    target_folder = "{}/{}/{}/{}".format(UPLOAD_FOLDER, fan_out_012, fan_out_345, oid)
    if not os.path.isdir(target_folder):
        os.makedirs(target_folder)

    tar_file_name = oid + '.tar.gz'
    tar_file = os.path.join(target_folder, tar_file_name)
    if not os.path.exists(tar_file):
        redirect(url_for('status', oid=oid))

    return send_from_directory(target_folder, tar_file_name)


@app.route('/status/<oid>', methods=['GET'])
def status(oid=None):

    fan_out_012 = oid[0:3]   # first three letters
    fan_out_345 = oid[3:6]   # second three letters

    return render_template('status.html', oid=oid, log=log_content, dir=ls_content)


@app.route('/intents', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        target_folder, input_file, fid = extract_intents(request)
        log_file_path = os.path.join(target_folder, fid + "_log.txt")

        # out, err = cmd.communicate()
        return redirect(url_for('status', oid=fid))

    return render_template('intents.html')


if __name__ == "__main__":
    app.run(debug=True)
