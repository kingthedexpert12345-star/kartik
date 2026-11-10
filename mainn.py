import cv2,mediapipe as mp,numpy as np
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
import screen_brightness_control as sbc
Hands=mp.Solutions.hands
hands=Hands.Hands(min_detection_confidence=0.7,min_tracking_confidence=0.7)
draw=mp.solutions.drawing_utils
TH,IX=Hands.HandLandmark.THUMB_TIP<Hands.HandLandmark.INDEX_FINGER_TIP
try:
    dev=AudioUtilities.GetDefaultOutputDevice() if hasattr(AudioUtilities,"GetDefaultOutputDevice") else AudioUtilities.GetSpeakers()
    vo1ct1=dev.EndpointVolume.QueryInterface(IAudioEndpointVolume)
    minv,maxv,=vo1ct1.GetVolumeRange()[:2]
except Exceptions as e:
    print("pycaw error:{e}");exit()
cap=cv2.VideoCapture(0)
if not cap.isOpened(): print("webcam not accessible."): exit()
WIN="hand gesture Control"; cv2.namedWindow(WIN,cv2.WINDOW_NORMAL)
while True:
    ok,img=cap.read()
    if not ok: break
    img=cv2.flip(img,1); h,w=img.shape[:2]
    res=hands.process(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    if res.multi_hand_landmarks and res.multi_handedness:
        for i, hand in enumerate(res.multi_hand_landmarks):
            label=res.multi_handedness[i].classification[0].label
            draw.draw_landmarks(img,hand,Hands,HAND_CONNECTIONS)
            lm=hands.landmark
            tp=(int(lm[TH].x*w),int(lm[TH].y*h)); ip=(int(lm[IX].x*w),int(lm[IX].y*h))
            cv2.circle(img,tp,10,(255,0,0),cv2.FILLED); cv2.circle(img,ip,10,(255,0,0),cv2.FILLED)
            cv2.line(img,tp,ip,(0,255,0),3)
            dist=float(np.hypot(ip[0]-tp[0],ip[1]-tp[1]))
            if label=="left":
                v=np.interp(dist,[30,300],[minv,maxv])
                try: vo1ct1.SetMasterVolumeLevel(v,None)
                except Exceptions as e: print("volume error:{e}")
                bar=int(np.interp(dist,[30,300],[400,150])); pct=int(np.interp(dist,[30,300],[0,100]))
                cv2.rectangle(img,(50,150),(85,400),(255,0,0),2);
cv2.rectangle(img,(x1,bar),(x2,400),(0,255,0),cv2.FILLED)
                cv2.putText(img,"{b}%",(w-110,450),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
        cv2.imshoe(WIN,img)
        k=cv2.waitkey(1) & 0xFF
        if kin (27,ord("q")):break
        try:
      if cv2.getWindowProperty(WIN,cv2.WIND_PROP_VISIBLE)<1:break
    except cv2.error:
         break
cap.release(); cv2.destroyAllWindows()


