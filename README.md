<h1 align="center">Speedtest</h1>

<p align="center"><strong>Explore network measurements from both sides of the browser.</strong></p>
<p align="center">A Python and Flask experiment combining browser request timing with server-side transfer and speedtest-cli measurements.</p>

<p align="center">
  <strong>English</strong> · <a href="README.tr.md">Türkçe</a><br />
  <a href="#run-locally"><strong>Run locally</strong></a> ·
  <a href="#measurement-paths">Measurement paths</a> ·
  <a href="#validation-and-current-limits">Current limits</a>
</p>

---

This project explores two approaches to connection testing. The browser page times HTTP requests, while a separate Flask route combines file transfers, speedtest-cli and a system ping command. Reading them together shows why the location of the measurement, the transferred byte count and the timing method matter.

**This is an experimental prototype.** Several measurement and upload paths need correction before their output can be treated as an accurate speed result. The interface is primarily English, with some Turkish upload responses. Documentation is available in English and Turkish.

## Run locally

| Requirement | Purpose |
| --- | --- |
| Python 3 with pip and venv | Isolated development environment |
| Flask 3.0.0 | Web routes and templates |
| Requests 2.31.0 and speedtest-cli 2.1.3 | Imported by the server |
| Modern browser | JavaScript request timing |

Clone the source and create a fresh environment.

```text
git clone https://github.com/ArdaHFO/speedtest.git
cd speedtest
python -m venv .venv
```

Activate it with `.venv\Scripts\activate` on Windows Command Prompt or `source .venv/bin/activate` on macOS/Linux. Install the direct runtime dependencies and start a local preview.

```text
python -m pip install Flask==3.0.0 requests==2.31.0 speedtest-cli==2.1.3
python -m flask --app app run --host 127.0.0.1 --port 8000
```

Open [localhost:8000](http://127.0.0.1:8000). These commands start the UI without initiating a transfer test. The broader [requirements.txt](requirements.txt) is a historical environment snapshot. The committed `Scripts/` directory contains environment-specific binaries, so use the newly created environment instead.

## Inside the project

- **Browser download timing.** A button requests a remote image and displays a calculated rate.
- **File upload experiment.** A file picker sends a multipart request to the Flask server.
- **HTTP round-trip timing.** The ping button measures the time taken by a request to `/ping`.
- **Server-side comparison.** `POST /measure` combines a fixed-size download, an upload to an external echo service, speedtest-cli results and a system ping.
- **Separate result view.** The server renders its measurements into a Jinja template with server-location details.

## Measurement paths

| Path | Behavior | Where the measurement occurs |
| --- | --- | --- |
| `GET /` | Displays the browser interface | Browser |
| `GET /ping` | Returns `Pong` | HTTP request from browser to Flask |
| `POST /upload` | Saves a submitted file under `uploads/` | Browser to Flask |
| `POST /measure` | Runs transfers, speedtest-cli and system ping | The machine running Flask |
| `GET /views/` | Alternate entry to the same interface | Browser |

A remote Flask deployment measures a different network path from a local one. The server-side route measures the server's connectivity, not automatically the visitor's internet connection. The browser's “Ping” is an HTTP round trip, not an ICMP measurement.

## Validation and current limits

The Python source, templates, routes and dependency declarations were reviewed for this documentation. No network measurements or runtime integration tests were performed.

- The browser download uses a fixed remote IP address and an assumed 1 MiB payload, while the requested filename suggests a different size. Availability, TLS and cross-origin access are not verified.
- Browser rate calculations label byte-based values as Mbps without the required conversion to bits. The server's custom calculations also need review. Displayed numbers should not be used as benchmark results.
- The upload directory is not included. The upload handler saves the supplied filename without a production upload policy, so keep this prototype local and use non-sensitive test files.
- The custom server upload calculation counts the response body rather than the transmitted file bytes.
- The server measurement form has its submit control commented out. Its system-ping handling also depends on operating-system behavior.
- External requests lack explicit timeouts and robust status handling. Running `POST /measure` generates real network traffic.

For a corrected implementation, define the network path first, check HTTP success, use the actual payload size, and calculate decimal Mbps as `bytes × 8 / seconds / 1,000,000`. Report repeatability and caching behavior alongside any result.

## Project map

```text
app.py                 Flask routes and server-side measurements
views.py               Additional page routes
templates/index.html   Browser controls and JavaScript timing
templates/measure.html Server-side result view
5MB.png, 10MB.png,
20MB.png               Transfer fixtures
requirements.txt       Historical dependency snapshot
Scripts/               Committed historical Python environment
```

## Development and contributions

Keep browser measurements and server measurements clearly identified in changes. For a bug report, include the operating system, Python version, requested route, HTTP status and the exact calculation involved. Describe whether validation was static, local HTTP testing or a real transfer measurement.

Useful next work includes correcting units, making download fixtures configurable, hardening uploads and adding isolated tests for route behavior and calculations.

## License and credits

Distributed under the [MIT license](LICENSE). External endpoints and speedtest-cli are separate services and dependencies with their own terms and availability.

