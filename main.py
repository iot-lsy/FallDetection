import cv2

# 영상 정보 불러오기
video = cv2.VideoCapture('FALL-Lateral_.mp4')
# 가우시안 혼합 배경제거 알고리즘
fgbg = cv2.createBackgroundSubtractorMOG2(history=0, varThreshold=137, detectShadows=0)

rect_count = 0
fall_count = 0


def MOG(frame):
    global rect_count
    global fall_count
    x = 0
    y = 0
    w = 0
    h = 0


    fgmask = fgbg.apply(frame)
    results = cv2.findContours(
        fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in results[0]:
        x, y, w, h = cv2.boundingRect(contour)

        if w*h >= 20000:
            A = ((x + w) + y) / 2
            B = (x + (y + h)) / 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if A > B:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                fall_count += 1


    cv2.imshow('fgmask', fgmask)


while True:

    ret, frame = video.read()

    if ret is True:

        MOG(frame)

        cv2.imshow('video', frame)

        if(fall_count >= 60):
            print("낙상감지")
            fall_count = 0

        if cv2.waitKey(1) > 0:
            break