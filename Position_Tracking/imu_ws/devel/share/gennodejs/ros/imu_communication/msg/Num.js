// Auto-generated. Do not edit!

// (in-package imu_communication.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Num {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.accX = null;
      this.accY = null;
    }
    else {
      if (initObj.hasOwnProperty('accX')) {
        this.accX = initObj.accX
      }
      else {
        this.accX = 0.0;
      }
      if (initObj.hasOwnProperty('accY')) {
        this.accY = initObj.accY
      }
      else {
        this.accY = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Num
    // Serialize message field [accX]
    bufferOffset = _serializer.float64(obj.accX, buffer, bufferOffset);
    // Serialize message field [accY]
    bufferOffset = _serializer.float64(obj.accY, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Num
    let len;
    let data = new Num(null);
    // Deserialize message field [accX]
    data.accX = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [accY]
    data.accY = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'imu_communication/Num';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '40ec70ad81cadc0ffcb5889fcacbbff8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 accX
    float64 accY
    
    
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Num(null);
    if (msg.accX !== undefined) {
      resolved.accX = msg.accX;
    }
    else {
      resolved.accX = 0.0
    }

    if (msg.accY !== undefined) {
      resolved.accY = msg.accY;
    }
    else {
      resolved.accY = 0.0
    }

    return resolved;
    }
};

module.exports = Num;
