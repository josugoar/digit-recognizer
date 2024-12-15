# digit-recognizer

<p align="center">
  <img src="assets/digit-recognizer.png" alt="digit-recognizer" width="640" height="320">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/author-josugoar-blue" alt="author">
  <img src="https://img.shields.io/badge/license-GPL-green" alt="license">
</p>

<h1></h1>


HTML, CSS (SCSS/Sass) and JavaScript (jQuery) interactve and responsive front-end UI on top of a Python (Flask, Flask-RESTful, Flask-Caching, Flask-FlatPages, Flask-SQLAlchemy) back-end API and database*, implementing Python (numpy, sklearn, opencv) machine learning model building** and image recognition preprocessing*** via asyncronous encoded requests. Integrated with Git source control.

* \* Database automatically clears itself up only when the application is booted, therefore it is not adviced to delete stored files whilist the processes are still running.

* ** Predictions are carried out by analyzing individual pixels, which might negatively impact accuracy. More advanced techniques (hog features, stroke sequence...) would result in improved performance.

* *** Preprocessing does not scale image with stroke width, which leads to poorer results as the image size increases.

Popup screen                             |Prediction result
:---------------------------------------:|:---------------------------------------:
![popup-screen](assets/popup-screen.png)|![prediction-result](assets/prediction-result.png)


## Installation

1. Install [Python >= 3.6](https://www.python.org/downloads/)
2. Install package manager [pip](https://pip.pypa.io/en/stable/)
3. Install [virtualenv](https://virtualenv.pypa.io/en/latest/userguide/)
```sh
$ pip install virtualenv
```
4. Create an environment
```sh
$ virtualenv ENV
```
5. Activate the environment
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

See [info.html](src/static/pages/info.html) for further details.
