print('BOOTING UP')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
#mapping object that represents the user’s environmental variables.
from reqpy import *
import sudukomath

Imagepath = "Resources/1.jpg"
Imgheight = 450
Imgwidth = 450
model = intializePredectionModel()  
#CNN MODEL

#### 1. PREPAREING THE IMAGE
img = cv2.imread(Imagepath)
img = cv2.resize(img, (Imgwidth, Imgheight))
# RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
imgBlank = np.zeros((Imgheight, Imgwidth, 3), np.uint8)  
# DEBUGING IF REQUIRED TO CREATE A BLANK_IMAGE FOR TESTING
imgThreshold = preProcess(img)

##### 2. FINDING COUNTOURS
imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS

#### 3. FIND THE biggest COUNTOUR AND USE IT AS SUDOKU
major, maxArea = majorContour(contours) # FIND THE MAJOR CONTOUR
print(major)
if major.size != 0:
    major = reorder(major)
    print(major)
    cv2.drawContours(imgBigContour, major, -1, (0, 0, 255), 25) # DRAW THE MAJOR CONTOUR
    points1 = np.float32(major) # PREPARE POINTS FOR WARP
    points2 = np.float32([[0, 0],[Imgwidth, 0], [0, Imgheight],[Imgwidth, Imgheight]]) 
# PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(points1, points2) # GER
    imgWarpColored = cv2.warpPerspective(img, matrix, (Imgwidth, Imgheight))
    imgDetectedDigits = imgBlank.copy()
    imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

    #### 4. FIND EACH DIGIT AVAILABLE AND SPLIT THE IMAGE 
    imgSolvedDigits = imgBlank.copy()
    boxes = splitBoxes(imgWarpColored)
    print(len(boxes))
    # cv2.imshow("Sample",boxes[65])
    numbers = getPredection(boxes, model)
    print(numbers)
    imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
    numbers = np.asarray(numbers)
    posArray = np.where(numbers > 0, 0, 1)
    print(posArray)


    #### 5. FIND SOLUTION OF THE BOARD
    board = np.array_split(numbers,9)
    print(board)
    try:
        sudukomath.solve(board)
    except:
        pass
    print(board)
    flatList = []
    for sublist in board:
        for item in sublist:
            flatList.append(item)
    solvedNumbers =flatList*posArray
    imgSolvedDigits= displayNumbers(imgSolvedDigits,solvedNumbers)

    ##### 6. FINAL SOLUTION
    points2 = np.float32(major) # PREPARE POINTS FOR WARP
    points1 =  np.float32([[0, 0],[Imgwidth, 0], [0, Imgheight],[Imgwidth, Imgheight]])
 # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(points1, points2)  # GER
    imgInvWarpColored = img.copy()
    imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (Imgwidth, Imgheight))
    inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
    imgDetectedDigits = drawGrid(imgDetectedDigits)
    imgSolvedDigits = drawGrid(imgSolvedDigits)

    imageArray = ([img,imgThreshold,imgContours, imgBigContour],
                  [imgDetectedDigits, imgSolvedDigits,imgInvWarpColored,inv_perspective])
    stackedImage = stackImages(imageArray, 0.5)
    cv2.imshow('Stacked Images', stackedImage)
else:
    print("Sudoku Not Found")
cv2.waitKey(0)
