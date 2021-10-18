;; Auto-generated. Do not edit!


(when (boundp 'imu_communication::Num)
  (if (not (find-package "IMU_COMMUNICATION"))
    (make-package "IMU_COMMUNICATION"))
  (shadow 'Num (find-package "IMU_COMMUNICATION")))
(unless (find-package "IMU_COMMUNICATION::NUM")
  (make-package "IMU_COMMUNICATION::NUM"))

(in-package "ROS")
;;//! \htmlinclude Num.msg.html


(defclass imu_communication::Num
  :super ros::object
  :slots (_accX _accY ))

(defmethod imu_communication::Num
  (:init
   (&key
    ((:accX __accX) 0.0)
    ((:accY __accY) 0.0)
    )
   (send-super :init)
   (setq _accX (float __accX))
   (setq _accY (float __accY))
   self)
  (:accX
   (&optional __accX)
   (if __accX (setq _accX __accX)) _accX)
  (:accY
   (&optional __accY)
   (if __accY (setq _accY __accY)) _accY)
  (:serialization-length
   ()
   (+
    ;; float64 _accX
    8
    ;; float64 _accY
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _accX
       (sys::poke _accX (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _accY
       (sys::poke _accY (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _accX
     (setq _accX (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _accY
     (setq _accY (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get imu_communication::Num :md5sum-) "40ec70ad81cadc0ffcb5889fcacbbff8")
(setf (get imu_communication::Num :datatype-) "imu_communication/Num")
(setf (get imu_communication::Num :definition-)
      "float64 accX
float64 accY




")



(provide :imu_communication/Num "40ec70ad81cadc0ffcb5889fcacbbff8")


