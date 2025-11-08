\# Solar Challenge Week 1



\## Environment Setup



\### Prerequisites

\- Python 3.9 or higher

\- Git



\### Installation Steps



1\. \*\*Clone the repository:\*\*

&nbsp;  ```bash

&nbsp;  git clone https://github.com/beza1619/solar-challenge-week1.git

&nbsp;  cd solar-challenge-week1

&nbsp;  ```



2\. \*\*Set up Python virtual environment:\*\*

&nbsp;  ```bash

&nbsp;  python -m venv venv

&nbsp;  ```

&nbsp;  

&nbsp;  \*\*Activate the environment:\*\*

&nbsp;  - Windows:

&nbsp;    ```bash

&nbsp;    venv\\Scripts\\activate

&nbsp;    ```

&nbsp;  - Mac/Linux:

&nbsp;    ```bash

&nbsp;    source venv/bin/activate

&nbsp;    ```



3\. \*\*Install dependencies:\*\*

&nbsp;  ```bash

&nbsp;  pip install -r requirements.txt

&nbsp;  ```



4\. \*\*Launch Jupyter Notebook for analysis:\*\*

&nbsp;  ```bash

&nbsp;  jupyter notebook

&nbsp;  ```



\## Project Structure

```

solar-challenge-week1/

├── .github/workflows/    # CI/CD workflows

├── notebooks/            # Jupyter notebooks for EDA

├── src/                  # Source code modules

├── tests/                # Unit tests

├── app/                  # Streamlit dashboard

├── data/                 # Dataset files (gitignored)

├── .gitignore

├── requirements.txt

└── README.md

```



\## Usage

\- For data analysis: Use Jupyter notebooks in `notebooks/` folder

\- For dashboard: Run `streamlit run app/main.py` from the app directory



\## CI/CD

This project uses GitHub Actions for continuous integration. On every push, it automatically:

\- Installs dependencies from requirements.txt

\- Runs basic validation

