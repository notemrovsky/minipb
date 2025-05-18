#!/usr/bin/env python3

# Minimal protobuf encoder for specific use cases - avoids pulling in the full library

def encode_varint(value): # https://github.com/protocolbuffers/protobuf/blob/main/python/google/protobuf/internal/encoder.py
    result = b''
    while value >= 0x80:
        result += bytes([(value & 0x7F) | 0x80])
        value >>= 7
    result += bytes([value & 0x7F])
    return result

def encode_tag(field_number, wire_type):
    return encode_varint((field_number << 3) | wire_type)

def encode_string(field_number, value):
    bytes_value = value.encode('utf-8')
    result = encode_tag(field_number, 2)
    result += encode_varint(len(bytes_value))
    result += bytes_value
    return result

def encode_uint32(field_number, value):
    result = encode_tag(field_number, 0)
    result += encode_varint(value)
    return result

def encode_bytes(field_number, value):
    result = encode_tag(field_number, 2)
    result += encode_varint(len(value))
    result += value
    return result

def encode_nested_message(field_number, data, schema=None, path=""):
    encoded = encode_message(data, schema, path + str(field_number) + ".")
    result = encode_tag(field_number, 2)
    result += encode_varint(len(encoded))
    result += encoded
    return result

def encode_message(data, schema=None, path=""):
    if schema is None:
        schema = {}

    result = b''
    for key, value in data.items():
        field_number = int(key)
        field_path = path + str(field_number)
        wire_type = schema.get(field_path)
        
        if isinstance(value, str):
            result += encode_string(field_number, value)
        elif isinstance(value, int):
            if wire_type == 2:
                # Handle cases where ints need to be encoded as bytes
                result += encode_bytes(field_number, bytes([value]))
            else:
                result += encode_uint32(field_number, value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, int):
                    field_wire_type = schema.get(field_path)
                    if field_wire_type == 2:
                        result += encode_bytes(field_number, bytes([item]))
                    else:
                        result += encode_uint32(field_number, item)
                elif isinstance(item, dict):
                    result += encode_nested_message(field_number, item, schema, path)
        elif isinstance(value, dict):
            result += encode_nested_message(field_number, value, schema, path)
    
    return result

def convert_json_to_protobuf_hex(json_obj, schema=None):
    binary_data = encode_message(json_obj, schema)
    return binary_data
