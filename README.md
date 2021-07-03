# Star Simulator Software Development :star:
Development of star simulator software for star sensor research during my internship at the National Institute of Aeronautics and Space (Lembaga Penerbangan dan Antariksa Nasional). This software will generate star image or video by the user by first providing three inputs which are:
1. Right ascension (α)
2. Declination (δ)
3. Roll (ψ)

It's basically a planetarium software but only shows stars. This software can be used for star pattern recognition system validation.

## Description :blue_book:
In this repository, the main file that generates the star image is ```star_simulator.py```. When running the main file, the star image will be automatically saved under the directory ```sample_images/``` with ```.jpg``` extension. Other files include:
1. ```SAO.xlsx```
<br>This file contains the complete star catalogue from the Smithsonian Astrophysical Observatory.
2. ```star_filtering.py```
<br>This script is for generating CSV files to create filtered star catalogue that contains stars only in a specified magnitude range and will be saved under the directory ```filtered_catalogue/```
3. ```nested_function.py```
<br>This is the script used to minimize the hassle of creating the full code for generating a star image when trying to create each frame for the star tracking video.
4. ```star_sim_with_angular_rate.py```.
<br>Generates the star tracking video and the video will be automatically saved under the directory ```sample_tracking_videos/``` with ```.avi``` extension.
5. ```star_image_class.py```
<br>This image is the class file which can be reused for any development in the future.
6. ```gui_root.py```
<br>Run this to get a more user friendly interface. This is the graphical user interface based star simulator.

## Dependencies
Before running ```star_simulator.py```, [Python](https://www.python.org/downloads/) must be installed and the following libraries:
* [Numpy](https://numpy.org/doc/stable/)
```bash
pip install numpy
```
* [Pandas](https://pandas.pydata.org/docs/)
```bash
pip install pandas
```
* [Matplotlib](https://matplotlib.org/3.3.3/contents.html)
```bash
pip install matplotlib
```
* [OpenCV](https://docs.opencv.org/master/)
```bash
pip install cv2-python
```
* [Tkinter](https://docs.python.org/3/library/tk.html)
```bash
pip install tkinter
```

## App Screenshot!

Run `gui_root.py` you will get this result!

<img src="https://user-images.githubusercontent.com/32363208/124360155-78613e80-dc52-11eb-8900-1ae988bedbf2.png" height=600/>

### Features:
- Change the attitude of the field of view
- Change the focal length of the camera
- Change the pixel size of the camera
