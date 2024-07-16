import cv2
import mediapipe as mp
import os
import subprocess

mpDrawing = mp.solutions.drawing_utils #rysowanie detekcji
mpDrawingStyles = mp.solutions.drawing_styles #Style rysowania elementów
mpHands = mp.solutions.hands #detekcja dłoni

cap = cv2.VideoCapture(0) # domyslna kamera
hands = mpHands.Hands() # Inicjalizacja detekotra dłoni
thumbCounter = 0
indexCounter = 0
middleCounter = 0
ringCounter = 0
smallCounter = 0

def close_photos():
    try:
        subprocess.run(["taskkill", "/IM", "Photos.exe", "/F"], check=True)
    except subprocess.CalledProcessError:
        print("Microsoft Photos not found or couldn't be closed with taskkill.")
while True:

    data,image = cap.read() #odczyt frame z kamery, data- zmienna logiczna wskazujaca czy ramka zostala otworzna, image - rzczywisty obraz kamery
    if not data:
        continue
        
    image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB) #odbicie ekranu w poziomie
    results = hands.process(image) #przetworzenie obrazu za pomoca mediaPipe
    if results.multi_hand_landmarks: #jesli wykryte są dłonie:
        for hand_landmarks in results.multi_hand_landmarks: #iteracja przez kazda dłoń


            mpDrawing.draw_landmarks(image, hand_landmarks,mpHands.HAND_CONNECTIONS) # rysowanie punktow i polaczeen na image
            thumbCounter = 0
            indexCounter = 0
            middleCounter = 0
            ringCounter = 0
            smallCounter = 0

            if hand_landmarks.landmark[mpHands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[
                mpHands.HandLandmark.PINKY_MCP].y:
                smallCounter += 1
            if hand_landmarks.landmark[mpHands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[
                mpHands.HandLandmark.RING_FINGER_MCP].y:
                ringCounter += 1
            if hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[
                mpHands.HandLandmark.INDEX_FINGER_MCP].y:
                indexCounter += 1

            if hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[
                mpHands.HandLandmark.THUMB_IP].x:
                thumbCounter += 1

            if hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[
                mpHands.HandLandmark.MIDDLE_FINGER_MCP].y:
                middleCounter += 1

            if thumbCounter == 1 and indexCounter == 0 and middleCounter == 0 and ringCounter == 0 and smallCounter == 0:
                close_photos()
                imagePath = "KciukWGore.png"
                os.startfile(imagePath)
            if thumbCounter == 1 and indexCounter == 1 and middleCounter == 1 and ringCounter == 1 and smallCounter == 1:
                close_photos()
                imagePath = "PJONA.jpeg"
                os.startfile(imagePath)
            if thumbCounter == 0 and indexCounter == 1 and middleCounter == 0 and ringCounter == 0 and smallCounter == 1:
                close_photos()
                imagePath = "HellYeah.jpeg"
                os.startfile(imagePath)
            if thumbCounter == 1 and indexCounter == 0 and middleCounter == 0 and ringCounter == 0 and smallCounter == 1:
                close_photos()
                imagePath = "ESSA.jpeg"
                os.startfile(imagePath)

    cv2.imshow("Handtracker", image) #wyswietlanie obrazu w oknie
    cv2.waitKey(1)#szybkie odswiezanie
