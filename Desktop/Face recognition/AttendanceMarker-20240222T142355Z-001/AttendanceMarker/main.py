import cv2
"""
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    grey=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow("murali attendance marker",frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()

cv2.destroyAllWindows()"""
"""
img=cv2.imread("shiva.jpg",0)
print(img)
cv2.imshow("murali image validator",img)
k=cv2.waitKey(0)
if k==27:
    cv2.destroyAllWindows()
elif k==ord('s'):
    cv2.imwrite("greyshiva2.png",img)
    cv2.destroyAllWindows()"""
"""
img=cv2.imread("greyshiva.png")
img=cv2.line(img,(0,0),(255,255),(0,0,255),20)
img=cv2.rectangle(img,(0,0),(255,255),(0,0,255),1)
cv2.circle(img,(255,255),55,(0,0,255),7)
font=cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,"murali",(255,100),font,4,(0,255,255),cv2.LINE_4)
cv2.imshow("frame",img)
k=cv2.waitKey(0)
if k==ord("s"):
    cv2.imwrite("changed.jpg",img)
    cv2.destroyAllWindows()
else:
    cv2.destroyAllWindows()"""
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow("shot by murali",gray)
    k=cv2.waitKey(1)
    if k==27:
        cv2.destroyAllWindows()
        break
    elif k==ord("b"):
        cv2.imwrite("firstpic.png",gray)
        cap.release()
        cv2.destroyAllWindows()
        break
    elif k==ord("c"):
        cv2.imwrite("images/firstpic.png",frame)
        cap.release()
        cv2.destroyAllWindows()
        break


    