import cv2
import cvzone 
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from random import randint
import time

class VideoCamera(object):

    def resetIcicle(self):
            x_ice = randint(100, 1140-48)
            y_ice = randint(10, 40)
            iceiclePos = [x_ice, y_ice]
            return iceiclePos

    def __init__(self):
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)

        self.num_shards = 3

        for num in range(1, self.num_shards):
            x_ice = randint(100, 1140-48)
            y_ice = randint(10, 40)
            exec(f'self.iceiclePos{num} = [{x_ice}, {y_ice}]')
            exec(f'x{num}, y{num} = self.resetIcicle()')

        self.speedY = 50
        self.check_over = False

        self.video = cv2.VideoCapture(0)
        self.video.set(3, 1280)
        self.video.set(4, 720)

        imgBackground = cv2.imread("Resources/cave.png")
        self.iceicle = cv2.imread("Resources/iceicle.png", cv2.IMREAD_UNCHANGED)
        miner1 = cv2.imread("Resources/miner1.png", cv2.IMREAD_UNCHANGED)
        miner2 = cv2.imread("Resources/miner2.png", cv2.IMREAD_UNCHANGED)
        game_over = cv2.imread("Resources/GameOver.png")

        # Resize images
        self.background_resized = cv2.resize(imgBackground, (1280,720), interpolation = cv2.INTER_AREA)
        self.miner_resized1 = cv2.resize(miner1, (48,65), interpolation = cv2.INTER_AREA)
        self.miner_resized2 = cv2.resize(miner2, (80,120), interpolation = cv2.INTER_AREA)
        self.game_over_resized = cv2.resize(game_over, (1280,720), interpolation = cv2.INTER_AREA)

        self.t0 = time.time()

        self.increasing_timer = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, self.img = self.video.read()

        self.img = cv2.flip(self.img, 1)

        imgRaw = self.img.copy()

        # Find hand and landmarks
        # flipType tells CVZone to not flip the image 
        hands, self.img = self.detector.findHands(self.img, flipType=False)

        # Create image overlay
        self.img = cv2.addWeighted(self.img, 0.2, self.background_resized, 0.8, 0.0)

        # Check for hands
        if hands:
            for hand in hands:
                # Move
                # Maybe make it my index finger?
                x, y, w, h, = hand['bbox']

                # Get shape 
                h1, w1, _ = self.miner_resized1.shape
                x_hand = x - w1//2
                # Create borders
                x_hand = np.clip(x_hand, 100, 1140)

                if hand['type'] == "Right":
                    #Draw the Miner
                    self.img = cvzone.overlayPNG(self.img, self.miner_resized1, (x_hand,550))

                    for num in range(1, self.num_shards):
                        exec(f'if (x_hand-w1) < self.iceiclePos{num}[0] < x_hand + w1 and (560-h1) < self.iceiclePos{num}[1] < 550: self.check_over = True')
                        
                    # Keep character on screen
        else:
            try:
                self.img = cvzone.overlayPNG(self.img, self.miner_resized1, (x_hand,550))
            except:
                pass

        if self.check_over:
            self.img = cv2.addWeighted(self.game_over_resized, 0.8, self.background_resized, 0.2, 0.0)
            cv2.putText(self.img, str(self.seconds).zfill(2), (540, 460), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 5)

            cv2.putText(self.img, "Icy Caverns", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 2.75, (375, 255, 0), 9)

            cv2.putText(self.img, "Hint #1: Number of ice shards increased by 2 every 5 seconds", (400, 660), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(self.img, "Hint #2: Make sure your whole hand is visible to the camera", (400, 690), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        else:
            # Move the iceicle
            for num in range(1, self.num_shards):
                        exec(f'if self.iceiclePos{num}[1] <= 600 and self.iceiclePos{num}[1] >= 10: self.iceiclePos{num}[1] += self.speedY')
                        exec(f'self.img = cvzone.overlayPNG(self.img, self.iceicle, self.iceiclePos{num})')

            #Draw the Iceicle
            for num in range(1, self.num_shards):
                        exec(f'x{num}, y{num} = self.resetIcicle()')
                        exec(f'if self.iceiclePos{num}[1] == (600 + y{num}):self.iceiclePos{num}[0], self.iceiclePos{num}[1] = x{num}, y{num}')

            # Check the time
            t1 = time.time()
            total = t1-self.t0
            self.seconds = int(total)

            cv2.putText(self.img, "Time: "+str(self.seconds), (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(self.img, "Press [r] to restart", (1025, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            cv2.putText(self.img, "Note: Number of ice shards increased by 2 every 5 seconds", (22, 713), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Increase amount of iceicles
            if self.seconds%5 == 0 and self.increasing_timer == 0:
                self.increasing_timer += 1
                print("Increased timer plus 1")

            increasing_amount = 2
            if self.seconds%5 != 0 and self.increasing_timer == 1:
                self.num_shards += increasing_amount
                self.increasing_timer = 0
                print("Increased shards by 3")

                # Creating the added iceicles
                for num in range(self.num_shards-increasing_amount, self.num_shards):
                    print(num)
                    x_ice = randint(100, 1140-48)
                    y_ice = randint(10, 40)
                    exec(f'self.iceiclePos{num} = [{x_ice}, {y_ice}]')
                    exec(f'x{num}, y{num} = self.resetIcicle()')
        # Create image of yourself in corner
        self.img[580:700, 20:233] = cv2.resize(imgRaw, (213,120))

        cv2.imshow("Image", self.img)
        key = cv2.waitKey(1)

        if key == ord("r"):
            for num in range(1, self.num_shards):
                exec(f'x{num}, y{num} = self.resetIcicle()')
                exec(f'self.iceiclePos{num} = [x{num}, y{num}]')

            self.num_shards = 3
            self.t0 = time.time()
            self.speedY = 50
            self.check_over = False

        _, jpeg = cv2.imencode('.jpg', self.img)
        return jpeg.tobytes()