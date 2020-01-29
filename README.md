# Digit Recognizer

![Author](https://img.shields.io/badge/author-JoshGoA-blue) ![License](https://img.shields.io/badge/license-GPL-green)

HTML, CSS (SCSS/Sass) and JavaScript (jQuery) interactve and responsive front-end UI, built on top of a Python (Flask, Flask-RESTful, Flask-Caching, Flask-FlatPages, Flask-SQLAlchemy) back-end API and database, using Python (numpy, sklearn, opencv) machine learning model building and image recognition preprocessing for asyncronous predictions via encoded requests, integrated with Git source control.

DISCLAIMER: Predictions are carried out by analyzing individual pixels, which might negatively impact accuracy. More advanced techniques (hog features, stroke sequence...) would lead to improved results.

Popup screen                                     |  Prediction result
:-----------------------------------------------:|:-------------------------:
![screenshot(0)](media/screenshot(0).png)  |  ![screenshot(1)](media/screenshot(1).png)


## Installation

1. Install [python](https://www.python.org/downloads/)
2. Install package manager [pip](https://pip.pypa.io/en/stable/)
3. Install [virtualenv](https://virtualenv.pypa.io/en/latest/userguide/)
```sh
$ pip install virtualenv
```
4. Create environment
```sh
$ virtualenv ENV
```
5. Activate environment
```sh
(Posix)
$ source /path/to/ENV/bin/activate
```
```sh
(Windows)
$ \path\to\ENV\Scripts\activate
```
6. Install [requirements.txt](requirements.txt)
```sh
$ /path/to/ENV/bin/pip install -r requirements.txt
```

## Usage

1. Run [run.py](run.py) **in root**
```sh
$ python run.py
```
2. Open localhost port server link

See [docs.html](src/static/pages/docs.html) for further details.

## Contributors

* **JoshGoA** - *Main contributor* - [GitHub](https://github.com/JoshGoA)
