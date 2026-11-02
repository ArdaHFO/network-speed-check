from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
from views import views
from subprocess import check_output
import sys, io, threading, subprocess, re, platform, os, requests, time, speedtest, re
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.register_blueprint(views, url_prefix = "/views")
#----------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')
#----------------------------------------------------------------------------------------------------
def speed_test(type="", size=0):
    start = time.perf_counter()
    if type == 'download':
        url = f"http://ipv4.download.thinkbroadband.com:8080/{size}MB.zip"
        with requests.get(url, stream=True, timeout=(10, 60)) as response:
            response.raise_for_status()
            transferred = sum(len(chunk) for chunk in response.iter_content(64 * 1024))
    elif type == 'upload':
        file_path = Path(app.root_path) / f"{size}MB.png"
        transferred = file_path.stat().st_size
        with file_path.open('rb') as payload:
            response = requests.post(
                'https://httpbin.org/post', files={'file': payload}, timeout=(10, 60)
            )
            response.raise_for_status()
            response.close()
    else:
        raise ValueError("Unknown transfer type.")
    elapsed = time.perf_counter() - start
    if elapsed <= 0:
        raise RuntimeError("The transfer duration could not be measured.")
    return f"{elapsed:.2f} seconds", transferred * 8 / elapsed / 1_000_000, f"{transferred} bytes"

#----------------------------------------------------------------------------------------------------
def measure_ping_speed(host):
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        response = subprocess.run(
            ["ping", count_flag, "4", host],
            capture_output=True, text=True, errors="replace", timeout=15, check=True,
        )
        lines = response.stdout.splitlines()
        return "\n".join(lines[:2]), "\n".join(lines[2:])
    except (OSError, subprocess.SubprocessError):
        return None, None

#****************************************************************************************************   
@app.route('/measure', methods=['POST'])
def measure():
    if request.method == 'POST':
        download_datasize = ""
        download_datatime = ""
        download_speed = ""
        upload_datasize = ""
        upload_datatime = ""
        upload_speed = ""
        #------------------------------------------
        t_download_time,  t_download_speed, t_download_datasize = speed_test("download", 5) 
        download_datasize = t_download_datasize
        download_datatime = t_download_time
        download_speed = t_download_speed 
        #------------------------------------------
        t_upload_time,  t_upload_speed, t_upload_datasize = speed_test("upload", 5) 
        upload_datasize = t_upload_datasize
        upload_datatime = t_upload_time
        upload_speed = t_upload_speed 
         #------------------------------------------
         #Speed ​​Test Result uses Speedtest component - Begin
        st = speedtest.Speedtest()
        servers = st.get_best_server()
        download_speedtest = ""
        upload_speedtest = ""
        download_speedtest = st.download() / 1000000  # Convert to Mbps
        upload_speedtest = st.upload() / 1000000  # Convert to Mbps
        country_speedtest=servers['country']
        name_speedtest= servers['name']
        sponsor_speedtest=servers['sponsor']
        host_speedtest=servers['host']
        #Speed ​​Test Result uses Speedtest component - End
         #------------------------------------------
        ping_speed,ping_result = measure_ping_speed("www.verizon.com")#Frankfurt
        if ping_speed is not None:
            ping_Command = f"{ping_speed}"   
        else:
            ping_Command = "-1"
        #------------------------------------------
    return render_template('measure.html',  
           download_datatime=download_datatime, download_datasize=download_datasize, download_speed=download_speed, 
           upload_datatime=upload_datatime, upload_speed=upload_speed,upload_datasize=upload_datasize ,
           download_speedtest=download_speedtest, upload_speedtest=upload_speedtest,
           country_speedtest=country_speedtest, name_speedtest=name_speedtest, sponsor_speedtest=sponsor_speedtest, host_speedtest=host_speedtest,
           ping_Command=ping_Command,ping_result=ping_result)
#****************************************************************************************************   
@app.route('/ping')
def ping():
    return 'Pong', 200, {'Cache-Control': 'no-store'}
#****************************************************************************************************   

#****************************************************************************************************

@app.route('/download')
def download():
    response = send_file(
        Path(app.root_path) / '20MB.png',
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='20MB.png',
        conditional=False,
        etag=False,
        max_age=0,
    )
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file is None or not file.filename:
        return jsonify(error='Select a file to upload.'), 400
    received = 0
    for chunk in iter(lambda: file.stream.read(64 * 1024), b''):
        received += len(chunk)
    return jsonify(bytes_received=received)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
#----------------------------------------------------------------------------------------------------
