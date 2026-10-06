# use a light version of python as foundation
FROM python:3.11-slim

# setting the working directory inside the container so everything is organised
WORKDIR /app

#installing pandas so script can read csv
RUN pip install pandas

# copying the script and data file in the container
COPY analyse_turbines.py .
COPY telemetry_data.csv .

#running the script when the container starts
CMD ["python", "analyse_turbines.py"]


