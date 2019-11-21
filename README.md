# Datathon Melbourne 2019

A React app that provides useful information (e.g. vegetation index, false color images etc.) using satellite images from Copernicus Sentinel 2.

Release 2.0 will include more features such as ndvi projection and whether forecast.

## Examples

<img src = './img/fci-mode1.jp2'>

Near infrared (red), green (blue), red (green). This is useful in seeing changes in plant health. Vegetation appears in different shades of red depending on the types and conditions of the vegetation, since it has a high reflectance in the NIR band. Plants are dark red because they reflect infrared light strongly, and the infrared band is assigned to be red. Plants that are growing quickly reflect more infrared, so they are brighter red. That means that this type of false-color image can help us see how well plants are growing and how densely vegetated an area is.

<img src = './img/fci-mode2.jp2'>

Shortwave infrared (red), near infrared (green), and green (blue), often used to show floods or newly burned land. In this false-color band combination, plant-covered land is bright green, water is black, and bare earth ranges from tan to pink. Newly burned farmland is dark red, while older burns are lighter red. Much of the farmland in this area is used to grow sugar cane. Farmers burn the crop before harvest to remove leaves from the canes. Because burned land looks different in this kind of false-color image, it is possible to see how extensively farmers rely on fire in this region.

Water absorbs all three wavelengths, so it is black in this band combination. However, water is blue if it is full of sediment. Sediment reflects visible light, which is assigned to look blue in this band combination. This means that both sediment-laden water and saturated soil will appear blue. 


<img src = './img/fci-mode3.jp2'>
Blue (red), two different shortwave infrared bands (green and blue), useful to differentiate between snow, ice, and clouds.


<img src = './img/ndvi.jp2'>

At least three types of vegetation can be discriminated in this colour composite image: green, bright yellow and golden yellow areas. The green areas consist of dense trees with closed canopy. The bright yellow areas are covered with shrubs or less dense trees. The golden yellow areas are covered with green fields. The non vegetated areas appear in dark blue and magenta.

cite: [https://crisp.nus.edu.sg/~research/tutorial/opt_int.htm](https://crisp.nus.edu.sg/~research/tutorial/opt_int.htm), [https://earthobservatory.nasa.gov/features/FalseColor](https://earthobservatory.nasa.gov/features/FalseColor)
