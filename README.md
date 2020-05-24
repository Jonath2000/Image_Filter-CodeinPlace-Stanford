# Image_Filter-CodeinPlace-Stanford
I have developed an Image Filter application using Python for the final project in Code in Place(CS106A), Stanford.
This program will implement available filters of users choice. 

# Filters available
The application has the following filter 
1. Normal Filter
2. GrayScale Filter
3. Warhol Filter
4. Rad Filter
5. Sepia Filter
6. Hue Rotate Filter
7. Invert Filter
8. Half Tone Filter
9. Dithering Filter
10. Black & White Grain Filter
11. Brightness Filter
12. Black & White Filter.

# Adding new filter to the Application
More filters can be added easily by following the bellow steps:
1. Add the filter name to the FILTER_LIST. (This name will be displayed in the banner icon of the application).
2. Add the filter algorithm to the program.
3. Add the index of the filter in the FILTER_LIST and a command to call the respective filter function
in the create_filter_canvas(). This function takes the index of the banner icon passed as parameter.
