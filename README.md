# Color search engine

### Objective
- Preprocessing the image for color extraction

- Automatically determine the numbers of color of an image and extract the RGB values

- Apply reverse indexing strategy for the color searching engine

### File description
- retrieve.py: extract the color of image and compare to the csv file

- save_csv_2: save csv file

- colorname: Get the name of color by it RGB value

- deltaE: Convert RGB Value to Lab value and compare the difference by DeltaE2000

- remove_bg: remove the background of image

- silhouette_coeff: Find the best K value and execute k-Means clustering 
