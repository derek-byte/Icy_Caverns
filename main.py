import cv2
import cvzone 
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from random import randint
import time

# cv2.setWindowTitle("Image", "Icy Caverns" ) 

detector = HandDetector(detectionCon=0.8, maxHands=1)

def resetIcicle():
    x_ice = randint(100, 1140-48)
    y_ice = randint(10, 40)
    iceiclePos = [x_ice, y_ice]
    return iceiclePos

num_shards = 3

for num in range(1, num_shards):
    x_ice = randint(100, 1140-48)
    y_ice = randint(10, 40)
    exec(f'iceiclePos{num} = [{x_ice}, {y_ice}]')
    exec(f'x{num}, y{num} = resetIcicle()')

speedY = 50
check_over = False


cap = cv2.VideoCapture(0)

# Setting up camera frame size
cap.set(3, 1280)
cap.set(4, 720)

imgBackground = cv2.imread("Resources/cave.png")
iceicle = cv2.imread("Resources/iceicle.png", cv2.IMREAD_UNCHANGED)
miner1 = cv2.imread("Resources/miner1.png", cv2.IMREAD_UNCHANGED)
miner2 = cv2.imread("Resources/miner2.png", cv2.IMREAD_UNCHANGED)
game_over = cv2.imread("Resources/GameOver.png")

# Resize images
background_resized = cv2.resize(imgBackground, (1280,720), interpolation = cv2.INTER_AREA)
miner_resized1 = cv2.resize(miner1, (48,65), interpolation = cv2.INTER_AREA)
miner_resized2 = cv2.resize(miner2, (80,120), interpolation = cv2.INTER_AREA)
game_over_resized = cv2.resize(game_over, (1280,720), interpolation = cv2.INTER_AREA)

t0 = time.time()

increasing_timer = 0

while True:
    # Access camera
    _, img = cap.read()

    # Flip the image horizontally (vertically would be 0)
    img = cv2.flip(img, 1)

    imgRaw = img.copy()

    # Find hand and landmarks
    # flipType tells CVZone to not flip the image 
    hands, img = detector.findHands(img, flipType=False)

    # Create image overlay
    img = cv2.addWeighted(img, 0.2, background_resized, 0.8, 0.0)

    # Check for hands
    if hands:
        for hand in hands:
            # Move
            # Maybe make it my index finger?
            x, y, w, h, = hand['bbox']

            # Get shape 
            h1, w1, _ = miner_resized1.shape
            x_hand = x - w1//2
            # Create borders
            x_hand = np.clip(x_hand, 100, 1140)

            if hand['type'] == "Right":
                #Draw the Miner
                img = cvzone.overlayPNG(img, miner_resized1, (x_hand,550))

                for num in range(1, num_shards):
                    exec(f'if (x_hand-w1) < iceiclePos{num}[0] < x_hand + w1 and (560-h1) < iceiclePos{num}[1] < 550: check_over = True')

    # Keep character on screen
    else:
        try:
            img = cvzone.overlayPNG(img, miner_resized1, (x_hand,550))
        except:
            pass

    if check_over:
        img = cv2.addWeighted(game_over_resized, 0.8, background_resized, 0.2, 0.0)
        cv2.putText(img, str(seconds).zfill(2), (540, 460), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 5)

        cv2.putText(img, "Icy Caverns", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 2.75, (375, 255, 0), 9)

        cv2.putText(img, "Hint #1: Number of ice shards increased by 2 every 5 seconds", (400, 660), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img, "Hint #2: Make sure your whole hand is visible to the camera", (400, 690), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    else:
        # Move the iceicle
        for num in range(1, num_shards):
                    exec(f'if iceiclePos{num}[1] <= 600 and iceiclePos{num}[1] >= 10: iceiclePos{num}[1] += speedY')
                    exec(f'img = cvzone.overlayPNG(img, iceicle, iceiclePos{num})')

        #Draw the Iceicle
        for num in range(1, num_shards):
                    exec(f'x{num}, y{num} = resetIcicle()')
                    exec(f'if iceiclePos{num}[1] == (600 + y{num}):iceiclePos{num}[0], iceiclePos{num}[1] = x{num}, y{num}')

        # Check the time
        t1 = time.time()
        total = t1-t0
        seconds = int(total)

        cv2.putText(img, "Time: "+str(seconds), (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, "Press [r] to restart", (1025, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        cv2.putText(img, "Note: Number of ice shards increased by 2 every 5 seconds", (22, 713), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Increase amount of iceicles
        if seconds%5 == 0 and increasing_timer == 0:
            increasing_timer += 1
            print("Increased timer plus 1")

        increasing_amount = 2
        if seconds%5 != 0 and increasing_timer == 1:
            num_shards += increasing_amount
            increasing_timer = 0
            print("Increased shards by 3")

            # Creating the added iceicles
            for num in range(num_shards-increasing_amount, num_shards):
                print(num)
                x_ice = randint(100, 1140-48)
                y_ice = randint(10, 40)
                exec(f'iceiclePos{num} = [{x_ice}, {y_ice}]')
                exec(f'x{num}, y{num} = resetIcicle()')

    # Create image of yourself in corner
    img[580:700, 20:233] = cv2.resize(imgRaw, (213,120))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("r"):
        for num in range(1, num_shards):
            exec(f'x{num}, y{num} = resetIcicle()')
            exec(f'iceiclePos{num} = [x{num}, y{num}]')

        num_shards = 3
        t0 = time.time()
        speedY = 50
        check_over = False
    
