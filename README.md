# Rest Api Data Perpustakaan

Website to display a list of all libraries in Indonesia, through the rest api that I have created. Using the streamlit library

#### You will need clone [rest-api-perpustakaan](https://github.com/bal-19/rest-api-perpustakaan) project first

## Environment Variables

To run this project, you need to add the following environment variables to your .env file or you can replace the values ​​from the .env.example file

`API_URL`

## Installation

clone project using git

```bash
git clone https://github.com/bal-19/streamsilit-perpustakaan.git
cd streamsilit-perpustakaan
```

create python virtual environment

```bash
python3 -m venv .venv
```

activate virtual environment

-   Windows

```bash
.venv\Scripts\Activate.ps1
```

-   Linux

```bash
source .venv/bin/activate
```

install project requirements

```bash
pip install -r requirements.txt
```

renaming .env file

-   Windows

```bash
ren .env.example .env
```

-   Linux

```bash
mv .env.example .env
```

start project

```bash
streamlit run search.py
```
