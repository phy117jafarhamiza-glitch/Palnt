import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import numpy as np

# إعدادات MediaPipe لاستخراج المفاصل
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

st.title("⚽ تحليل ضربة الجزاء - كرة الصالات (Futsal)")
st.write("قم برفع فيديو للاعب أثناء تنفيذ ضربة الجزاء لتحليل حركته البايوميكانيكية.")

# أداة رفع الفيديو
uploaded_file = st.file_uploader("ارفع فيديو (MP4, AVI)", type=['mp4', 'avi', 'mov'])

if uploaded_file is not None:
    # حفظ الفيديو المؤقت لمعالجته بـ OpenCV
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    
    # مكان لعرض الفيديو داخل واجهة Streamlit
    stframe = st.empty()
    
    st.write("⏳ جاري تحليل الحركة...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # تحويل الألوان من BGR (OpenCV) إلى RGB (MediaPipe)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # معالجة الصورة واستخراج المفاصل
        results = pose.process(image)
        
        image.flags.writeable = True
        
        # رسم الهيكل العظمي على اللاعب
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )
            
            # هنا مستقبلاً سنضيف كود حساب الزوايا بين الحوض والكتف وقدم الارتكاز
            
        # عرض الإطار في واجهة Streamlit
        stframe.image(image, channels="RGB", use_container_width=True)
        
    cap.release()
    st.success("✅ تم الانتهاء من تحليل الفيديو!")