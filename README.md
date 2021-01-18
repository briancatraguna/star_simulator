# Star Simulator Software Development :star:
Development of star simulator software for star sensor research during my internship in the National Institute of Aeronautics and Space (Lembaga Penerbangan dan Antariksa Nasional). This software will generate star image or video by the user by first providing three inputs which are:
1. Right ascension (α)
2. Declination (δ)
3. Roll (ψ)

It's basically a planetarium software but only shows stars. This software can be used for star sensor algorithms research for satellite attitude determination system.

## Description :blue_book:
In this repository, the main file that generates the star image is ```star_simulator.py```. Other files include:
1. ```SAO.xlsx```
<br>This file contains the complete star catalogue from the Smithsonian Astrophysical Observatory.
2. ```star_filtering.py```
<br>This script is for generating CSV files to create filtered star catalogue that contains stars only in a specified magnitude range.
3. ```Below_6.0_SAO.csv```
<br>This is the CSV file that is used as the star catalogue reference in the star simulator program. This file is generated after running ```star_filtering.py```.
4. ```nested_function.py```
<br>This is the script used to minimize the hassle of creating the full code for generating a star image when trying to create each frame for the star tracking video.
5. ```star_sim_with_angular_rate.py```
<br>Generates the star tracking video.

## Dependencies
Before running ```star_simulator.py```, [Python](https://www.python.org/downloads/) must be installed and the following libraries:
* Numpy
```bash
pip install numpy
```
* Pandas
```bash
pip install pandas
```
* Matplotlib
```bash
pip install matplotlib
```
* OpenCV
```bash
pip install cv2-python
```

That's it, and enjoy! Any feedbacks would be very much appreciated!
