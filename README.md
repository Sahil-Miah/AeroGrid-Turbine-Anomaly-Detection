# AeroGrid Turbine Anomaly Detection

A Python script that goes through wind turbine sensor data and picks out any turbine running outside safe temperature or vibration limits. The repo also has a Dockerfile for running it in a container, a diagram of a cloud setup for handling the live data, and a short report to the CTO.

I did this as part of the Internship Experience UK (IEUK) virtual internship, run with Bright Network, in 2026. [Certificate](./assets/IEUK_Technology_%26_Engineering_Internship_Certificate.png)

## The scenario

AeroGrid is a made-up offshore wind company from the internship brief. Its turbines have sensors that send temperature, vibration and RPM readings. The old server can't keep up with the constant stream of data, and a few turbines have failed because nobody spotted the warning signs in the logs. The brief asked me to find the failing turbines, package the analysis in a container, suggest a better cloud setup, and write a short report for the CTO.

## What I found

| Turbine | Rule broken | Value | Limit |
|---|---|---|---|
| T-04 | Average temperature | 90.58°C | 85.0°C |
| T-07 | Highest vibration | 25.0 mm/s | 15.0 mm/s |

The other eight turbines (T-01, T-02, T-03, T-05, T-06, T-08, T-09 and T-10) stayed inside both limits.

The data is 5,000 readings from 10 turbines, with timestamps running from 15 to 19 April 2026. Every reading from T-04 was over 85°C and every reading from T-07 was over 15 mm/s, so these look like ongoing faults and not one-off glitches. In the report I suggested a cooling or bearing problem for T-04 and imbalance or blade damage for T-07, but the data can't confirm the cause.

The brief gave the two thresholds (average temperature over 85.0°C, vibration over 15.0 mm/s), so I applied them and didn't choose them.

## The script

For each turbine, `analyse_turbines.py` works out the average temperature and the highest vibration reading, then prints any turbine that goes over either limit. The notebook does the same thing and was written in Google Colab.

## Files

| File | What it is |
|---|---|
| `analyse_turbines.py` | The analysis script |
| `AeroGrid_Turbine_Analysis.ipynb` | The same analysis as a notebook |
| `telemetry_data.csv` | The sensor data that came with the brief |
| `Dockerfile` | Packages the script and data into a container |
| `AeroGrid_Engineering_Report.pdf` | My report to the CTO |
| `assets/` | The architecture diagram and my certificate |

## Running it

Keep the script and `telemetry_data.csv` in the same folder.

With Python:

    pip install pandas
    python analyse_turbines.py

With Docker:

    docker build -t aerogrid-analysis .
    docker run aerogrid-analysis

## Cloud setup (design only)

![Cloud architecture diagram](./assets/Aerogrid_Flowchart_Visual.png)

The idea is to stop sending sensor data straight to one server:

1. The sensors send readings to AWS Kinesis, a message queue. It holds the data when there's a sudden burst, so the processing side doesn't get overwhelmed. This is meant to fix the crashing.
2. AWS Lambda runs the same two rules on the data as it comes through, and sends an alert to the engineers when a turbine goes over a limit (email or SMS in the diagram).
3. InfluxDB, a time-series database, keeps the last 30 days of data for live dashboards.
4. After that the data moves to AWS S3, which is cheaper, as a long-term archive.

To keep costs down, the report suggests S3 Intelligent-Tiering. It moves data that hasn't been opened for 30 days into cheaper storage automatically, and AWS says that can save up to 40% on data that's rarely accessed.

I haven't built any of this on AWS. It's a diagram and a written explanation. The brief pointed at the kinds of thing to include (a message queue, stream processing, hot and cold storage), so my job was to pick specific services and explain why.

## Limits and what I'd do next

- The script reads one CSV file in one go. In the cloud design, the same rules would run on the live stream in Lambda.
- The vibration rule triggers on a single reading. That's fine here because T-07 went over on every reading, but a live system would probably need a few readings in a row to avoid false alarms from one bad value.
- RPM is in the data but neither rule uses it. I'd look at whether it changes alongside temperature or vibration.
- I'd build a small version of the pipeline to test the design, instead of leaving it as a diagram.
