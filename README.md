# python-pilot

**python-pilot** is a compact automation framework for data scraping and test automation using Python and Selenium.  Drop your script into the `scripts/` directory and use the runner to execute it and save the results where you want.

## Key features

* **Runner** – `scraperRunner.py` loads a script, calls its `initParsing()` function (or test entry point) and writes the resulting data or report into a timestamped folder under `output/reports/`.
* **Script separation** – Place data automation scripts under `scripts/scrapers/` and test scripts under `tests/`.  Both work with the same runner.
* **Web driver helpers** – `utils/seleniumEngine.py` sets up a Chrome WebDriver and provides simple helpers for waiting, clicking, typing and managing cookies.

## Getting started

1. **Install dependencies:** run the setup script (requires Python 3.8+).

   ```bash
   bash setup_project.sh
   ```

2. **Add a script:** create a file in `scripts/scrapers/` with an `initParsing()` function that returns a `pandas.DataFrame` or produces a test report.
3. **Run the script:**

   ```bash
   python scraperRunner.py YourScript.py
   ```

   The runner will create `output/reports/YourScript` and save the result there.  To run a default script without specifying a file name, use `python RUN_FILE.py`.

4. **Run tests:** if you have test modules in `tests/`, execute them with:

   ```bash
   pytest
   ```

## Project structure

```
python-pilot/
├── data/                  # persistent data (e.g., cookies.json)
├── scripts/
│   └── scrapers/          # data automation scripts (each defines initParsing())
├── tests/                 # test automation modules (run with pytest)
├── utils/                 # helper libraries (e.g., seleniumEngine.py)
├── scraperRunner.py       # core runner that executes automation scripts
├── RUN_FILE.py            # wrapper for running a default script
├── setup_project.sh       # installs system and Python dependencies
├── requirements.txt       # list of Python dependencies
└── LICENSE                # project license
```

## License

Released under the MIT License (see `LICENSE`).
