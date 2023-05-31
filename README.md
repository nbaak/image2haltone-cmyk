# Image 2 Halftone CMYK

<img src="images/tree.jpg"><img src="images/halftone_tree.jpg">

Create a Halftone CMYK Effect for your images. Maybe Photoshop can do this too (I don't know, I don't use PS) but it is more fun to build it your self!

## How to run it
Start the Service with running the App.

```bash
cd ./src
python3 App.py
```

Now the Service should be running on port 5000. To Access it go to <a src="http://localhost:5000">http://localhost:5000</a>.

## Required Packages

```bash
python3 -m pip install pillow Flask
```

Flask for the Webapp. Pillow to manipulate the Image.