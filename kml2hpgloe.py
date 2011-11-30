#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# Copyright (C) Daniel Lombraña González 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from xml.dom import minidom
from BeautifulSoup import BeautifulSoup as bs
from string import split
import urllib
import json
from optparse import OptionParser

def unescape(s):
    """ Unescape html for CDATA content in <description> tag
    """
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    return s

def main():
    """ This program parses a KML file or URL and uploads the HTML <img
    src="http://domain/image" to HP-Gloe giving one vote per coordinates.
    HP-Gloe only supports Points, so polygons, lines, etc. will be skipped.
    """
    # Arguments for the application
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    
    parser.add_option("-f", "--file", dest="filename", help="KML file name", metavar="FILE")
    parser.add_option("-u", "--url", dest="url", help="URL with the KML file", metavar="URL")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    
    (options, args) = parser.parse_args()

    if options.filename:
        if (options.verbose):
            print "Parsing a file...\n"
        dom = minidom.parse(options.filename)
    elif options.url:
        if (options.verbose):
            print "Retrieving KML from URL and parsing it...\n"
        dom = minidom.parse(urllib.urlopen(options.url))
    else:
        parser.error("you must supply a KML file name or a URL")
    
    Document = dom.getElementsByTagName('Document')[0]
    
    Folder = Document.getElementsByTagName('Folder')[0]
    
    
    for placemark in Folder.getElementsByTagName('Placemark'):
        # HP Gloe query
        # query = query + lat=0.0&lon=0.0&url=img&tags=geotagginglybia
        query = "http://www.hpgloe.com/json/rec/?"
    
        Point = placemark.getElementsByTagName('Point')
        if (Point):
            coordinates = Point[0].getElementsByTagName('coordinates')[0].childNodes
            #print coordinates[0].nodeValue
            (lon,lat) = split(coordinates[0].nodeValue,",")
            soup = bs(unescape(placemark.getElementsByTagName('description')[0].toxml()))
            # Get all images for the placemark
            for image in soup.findAll("img"):
                coordinates = "lat=" + lat + "&lon=" + lon
                url = "&url=" + image["src"]
                query = query + coordinates + url + "&tags=geotaglibya"
                response = json.load(urllib.urlopen(query))
                if (response["error"]):
                    print "ERROR: " + response["error"] + "\n"
                    exit 
                else:
                    print "URL: " + response["url"] 
                    print "Status: " + response["message"] 
                    print "Remaining quota: " + str(response["quota"]) + "\n\n"
        else:
            print "\nFound a polygon for the placemark. This does not fit in HP-Gloe dismissing it. Sorry!\n"

if __name__ == "__main__":
    main()
