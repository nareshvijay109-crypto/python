# Assignment 5 — Python Programming (CO5)
**Student:** Naresh Vijay R.  
**Register No.:** 1972260060D  
**Case study:** City Air-Quality Monitoring Network

## Assignment report
The complete PDF report is provided with the ChatGPT deliverables. This repository contains the executable source code, synthetic test data and automated validation tests.

## Files
- `air_quality_pipeline.py` — CSV acquisition, validation, cleaning, Fahrenheit-to-Celsius conversion, SQLite storage, daily/monthly summaries and charts.
- `citizen_ai.py` — complaint sentiment, extractive summary and FAQ chatbot.
- `benchmark.py` — Python loop / pandas / SQLite benchmark.
- `test_pipeline.py` — eight automated validation tests.
- `data/sample_station_readings.csv` — synthetic demonstration data (not official station readings).

## Run
```bash
python -m pip install pandas matplotlib
python -m unittest -v
python air_quality_pipeline.py --input data/sample_station_readings.csv --db air_quality.sqlite --fahrenheit-stations ST11,ST12 --out output
python citizen_ai.py
python benchmark.py --rows 50000 --repeats 3
```

Missing markers become SQL NULL; invalid fields are nulled, and rows with no usable measurements are rejected. ST11 and ST12 are demonstration Fahrenheit stations and the mapping is configurable. SQL values use parameterised statements. The sentiment lexicon is an educational prototype, not a validated production classifier.

**Important:** Real station exports and labelled complaint text were not supplied. Replace the synthetic CSV with approved source data before operational use.
