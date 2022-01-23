# pixel-planet
Semi-hash-based Image Generator

Utilizable for NFTs

![sample_image](https://user-images.githubusercontent.com/33227410/150660720-9bdaa13b-b593-436e-8bb9-590a3a5a1578.png)

### Generation Process
1. Input is salted and hashed
2. Colors (background, planet, stars) are chosen based on input hash
3. Stars are placed and sized with a slight variation in color randomly (not hash-based)
4. Planet is first completely colored with the primary planet color
5. Planet is then colored with a probabilistic breadth-first-search algorithm using probabilities from the input hash with a secondary color
6. Planet is then randomly colored with a tertiary color (not hash-based)
7. Decide if moon is included based on input hash
8. Position and color moon based on input hash

### Notes
 - Image size is fixed at 1000 by 500
 - Planet size is diameter = 400
