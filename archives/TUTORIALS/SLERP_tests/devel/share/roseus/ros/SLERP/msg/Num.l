;; Auto-generated. Do not edit!


(when (boundp 'SLERP::Num)
  (if (not (find-package "SLERP"))
    (make-package "SLERP"))
  (shadow 'Num (find-package "SLERP")))
(unless (find-package "SLERP::NUM")
  (make-package "SLERP::NUM"))

(in-package "ROS")
;;//! \htmlinclude Num.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass SLERP::Num
  :super ros::object
  :slots (_q1 _q2 _t ))

(defmethod SLERP::Num
  (:init
   (&key
    ((:q1 __q1) (instance geometry_msgs::Quaternion :init))
    ((:q2 __q2) (instance geometry_msgs::Quaternion :init))
    ((:t __t) 0.0)
    )
   (send-super :init)
   (setq _q1 __q1)
   (setq _q2 __q2)
   (setq _t (float __t))
   self)
  (:q1
   (&rest __q1)
   (if (keywordp (car __q1))
       (send* _q1 __q1)
     (progn
       (if __q1 (setq _q1 (car __q1)))
       _q1)))
  (:q2
   (&rest __q2)
   (if (keywordp (car __q2))
       (send* _q2 __q2)
     (progn
       (if __q2 (setq _q2 (car __q2)))
       _q2)))
  (:t
   (&optional __t)
   (if __t (setq _t __t)) _t)
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Quaternion _q1
    (send _q1 :serialization-length)
    ;; geometry_msgs/Quaternion _q2
    (send _q2 :serialization-length)
    ;; float32 _t
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Quaternion _q1
       (send _q1 :serialize s)
     ;; geometry_msgs/Quaternion _q2
       (send _q2 :serialize s)
     ;; float32 _t
       (sys::poke _t (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Quaternion _q1
     (send _q1 :deserialize buf ptr-) (incf ptr- (send _q1 :serialization-length))
   ;; geometry_msgs/Quaternion _q2
     (send _q2 :deserialize buf ptr-) (incf ptr- (send _q2 :serialization-length))
   ;; float32 _t
     (setq _t (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get SLERP::Num :md5sum-) "17a538d213721bf39aee66a387b311dd")
(setf (get SLERP::Num :datatype-) "SLERP/Num")
(setf (get SLERP::Num :definition-)
      "geometry_msgs/Quaternion q1
geometry_msgs/Quaternion q2
float32 t




================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :SLERP/Num "17a538d213721bf39aee66a387b311dd")


