kml2hpgloe is a script that parses a KML file and uploads its images to
[HP-Gloe](http://www.hpgloe.com/).

# Installation
It should run out of the box, as the script uses several default Python
libraries. If it does not work, you can use virtualenv and install the required
libraries (check the header of the file).

# Running the script
It is very easy:
```
./kml2hpgloe.py -f filename.kml
```

or

```
./kml2hpgloe.py -u http://domain.com/resources.kml
```

# License
[GPLv3](COPYING) (check COPYING file)
