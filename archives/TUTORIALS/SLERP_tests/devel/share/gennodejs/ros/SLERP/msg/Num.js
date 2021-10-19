// Auto-generated. Do not edit!

// (in-package SLERP.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class Num {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.q1 = null;
      this.q2 = null;
      this.t = null;
    }
    else {
      if (initObj.hasOwnProperty('q1')) {
        this.q1 = initObj.q1
      }
      else {
        this.q1 = new geometry_msgs.msg.Quaternion();
      }
      if (initObj.hasOwnProperty('q2')) {
        this.q2 = initObj.q2
      }
      else {
        this.q2 = new geometry_msgs.msg.Quaternion();
      }
      if (initObj.hasOwnProperty('t')) {
        this.t = initObj.t
      }
      else {
        this.t = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Num
    // Serialize message field [q1]
    bufferOffset = geometry_msgs.msg.Quaternion.serialize(obj.q1, buffer, bufferOffset);
    // Serialize message field [q2]
    bufferOffset = geometry_msgs.msg.Quaternion.serialize(obj.q2, buffer, bufferOffset);
    // Serialize message field [t]
    bufferOffset = _serializer.float32(obj.t, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Num
    let len;
    let data = new Num(null);
    // Deserialize message field [q1]
    data.q1 = geometry_msgs.msg.Quaternion.deserialize(buffer, bufferOffset);
    // Deserialize message field [q2]
    data.q2 = geometry_msgs.msg.Quaternion.deserialize(buffer, bufferOffset);
    // Deserialize message field [t]
    data.t = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 68;
  }

  static datatype() {
    // Returns string type for a message object
    return 'SLERP/Num';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '17a538d213721bf39aee66a387b311dd';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    geometry_msgs/Quaternion q1
    geometry_msgs/Quaternion q2
    float32 t
    
    
    
    
    ================================================================================
    MSG: geometry_msgs/Quaternion
    # This represents an orientation in free space in quaternion form.
    
    float64 x
    float64 y
    float64 z
    float64 w
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Num(null);
    if (msg.q1 !== undefined) {
      resolved.q1 = geometry_msgs.msg.Quaternion.Resolve(msg.q1)
    }
    else {
      resolved.q1 = new geometry_msgs.msg.Quaternion()
    }

    if (msg.q2 !== undefined) {
      resolved.q2 = geometry_msgs.msg.Quaternion.Resolve(msg.q2)
    }
    else {
      resolved.q2 = new geometry_msgs.msg.Quaternion()
    }

    if (msg.t !== undefined) {
      resolved.t = msg.t;
    }
    else {
      resolved.t = 0.0
    }

    return resolved;
    }
};

module.exports = Num;
