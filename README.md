This app estimates file transfer speeds and connection delays from a web browser or its server.

<h1 align="center">Network Speed Check</h1>

<p align="center"><strong>Explore network measurements from both sides of the browser.</strong></p>
<p align="center">A Python and Flask application combining browser request timing with server-side transfer and speedtest-cli measurements.</p>

<p align="center">
  <strong>English</strong> · <a href="README.tr.md">Türkçe</a><br />
  <a href="#run-locally"><strong>Run locally</strong></a> ·
  <a href="#measurement-paths">Measurement paths</a> ·
  <a href="#validation-and-current-limits">Current limits</a>
</p>

---

This project explores two approaches to connection testing. The browser page times HTTP requests, while a separate Flask route combines file transfers, speedtest-cli and a system ping command. Reading them together shows why the location of the measurement, the transferred byte count and the timing method matter.

**Measurement status.** Transfer paths and arithmetic have received static fixes, but end-to-end behavior and measurement accuracy have not been verified. The interface is primarily English. Documentation is available in English and Turkish.

## Run locally

| Requirement | Purpose |
| --- | --- |
| Python 3 with pip and venv | Isolated development environment |
| Flask 3.0.0 | Web routes and templates |
| Requests 2.31.0 and speedtest-cli 2.1.3 | Imported by the server |
| Modern browser | JavaScript request timing |

Clone the source and create a fresh environment.

```text
git clone https://github.com/ArdaHFO/network-speed-check.git
cd network-speed-check
python -m venv .venv
```

Activate it with `.venv\Scripts\activate` on Windows Command Prompt or `source .venv/bin/activate` on macOS/Linux. Install the direct runtime dependencies and start a local preview.

```text
python -m pip install Flask==3.0.0 requests==2.31.0 speedtest-cli==2.1.3
python -m flask --app app run --host 127.0.0.1 --port 8000
```

Open [localhost:8000](http://127.0.0.1:8000). These commands start the UI without initiating a transfer test. The broader [requirements.txt](requirements.txt) is a historical environment snapshot. The committed `Scripts/` directory contains environment-specific binaries, so use the newly created environment instead.

## Inside the project

- **Browser download timing.** A button requests the bundled transfer fixture and calculates a rate from the received byte count.
- **File upload timing.** A file picker sends a multipart request, and the server confirms the received byte count without saving an application file.
- **HTTP round-trip timing.** The ping button measures the time taken by a request to `/ping`.
- **Server-side comparison.** `POST /measure` combines a fixed-size download, an upload to an external echo service, speedtest-cli results and a system ping.
- **Separate result view.** The server renders its measurements into a Jinja template with server-location details.

## Measurement paths

| Path | Behavior | Where the measurement occurs |
| --- | --- | --- |
| `GET /` | Displays the browser interface | Browser |
| `GET /ping` | Returns `Pong` | HTTP request from browser to Flask |
| `GET /download` | Serves the bundled `20MB.png` without caching | Flask to browser |
| `POST /upload` | Counts received bytes without saving an application file | Browser to Flask |
| `POST /measure` | Runs transfers, speedtest-cli and system ping | The machine running Flask |
| `GET /views/` | Alternate entry to the same interface | Browser |

A remote Flask deployment measures a different network path from a local one. The server-side route measures the server's connectivity, not automatically the visitor's internet connection. The browser's “Ping” is an HTTP round trip, not an ICMP measurement.

## Validation and current limits

The source has been reviewed statically. No application execution, automated tests, network measurements or benchmarks were performed for these changes.

- Browser timing now uses successful HTTP responses, actual payload bytes, elapsed seconds and decimal Mbps. Download and ping responses disable caching. These corrections have not been exercised in a browser.
- Browser downloads use the bundled `20MB.png`, so the measured path is between the browser and this Flask server. A local preview does not measure ISP bandwidth.
- Upload requests are limited to 32 MiB including multipart overhead. The handler consumes file bytes for counting and does not retain a saved application file.
- The server-side upload rate includes request and response time. HTTP handling, network conditions and remote services influence the observed rate.
- The optional server measurement route still uses external transfer services and speedtest-cli. Its form submit control is commented out, and no current provider availability is claimed.
- System ping output remains operating-system dependent. Commands and custom HTTP requests have bounded waits, but the complete external-service flow has not been verified.

Rates are calculated as `bytes × 8 / seconds / 1,000,000`. Meaningful benchmark reporting still requires controlled payloads, repeat runs and a clear account of the network path.

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

Useful next work includes isolated route/calculation tests and repeatable measurements against a controlled server.

## License and credits

Distributed under the [MIT license](LICENSE). External endpoints and speedtest-cli are separate services and dependencies with their own terms and availability.
