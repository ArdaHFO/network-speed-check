This app measures file transfers in the browser and runs separate speed checks from its server.

# Network Speed Check

[English](README.md) · [Türkçe](README.tr.md)

The main page times downloads, uploads and HTTP requests between your browser and Flask. A separate `POST /measure` route combines external file transfers, speedtest-cli and system ping results.

## Run locally

You need Python 3 with pip and venv, and a web browser.

```text
git clone https://github.com/ArdaHFO/network-speed-check.git
cd network-speed-check
python -m venv .venv
```

Activate the environment with `.venv\Scripts\activate` in Windows Command Prompt, or `source .venv/bin/activate` on macOS/Linux.

```text
python -m pip install Flask==3.0.0 requests==2.31.0 speedtest-cli==2.1.3
python -m flask --app app run --host 127.0.0.1 --port 8000
```

Open [localhost:8000](http://127.0.0.1:8000). Starting the server does not start a transfer.

[requirements.txt](requirements.txt) contains a larger historical dependency list. The committed `Scripts/` folder belongs to that old Python environment; use the fresh virtual environment above.

## Browser measurements

The page downloads the bundled `20MB.png` through `GET /download`, sends a selected file to `POST /upload`, and times `GET /ping`.

The server confirms the uploaded byte count without saving a copy of the file. Upload requests are limited to **32 MiB**, including multipart overhead. Download and ping responses disable caching.

## Server measurements

`POST /measure` runs these operations on the machine hosting Flask:

1. Requests a 5 MB download from thinkbroadband.
2. Uploads the bundled `5MB.png` to httpbin.
3. Runs speedtest-cli download and upload measurements.
4. Runs the operating system's ping command.

Results appear in `templates/measure.html`, including the server selected by speedtest-cli. The form's submit button is currently commented out, so this route requires a direct POST request. It makes external network requests and can transfer more data than the two named files alone.

## Reading the results

Custom transfer rates use `bytes × 8 / seconds / 1,000,000` to report decimal Mbps. They include request handling time; the httpbin upload also includes the response.

The browser's Ping button measures an HTTP round trip. The system ping in the server report is a separate measurement. Browser results describe the browser-to-Flask connection, while server results describe the hosting machine's connection to external services. Localhost transfers do not measure ISP bandwidth.

End-to-end behavior and measurement accuracy have not been validated. External services may be unavailable, and system-ping output varies by operating system.

## Code and license

[app.py](app.py) contains the routes and server measurements. Browser timing is in [templates/index.html](templates/index.html); [views.py](views.py) provides the alternate page routes.

[MIT license](LICENSE). Dependencies and external services retain their own licenses and terms.
