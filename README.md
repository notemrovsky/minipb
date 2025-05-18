```markdown
# minipb

A lightweight, zero-dependency protobuf encoder for Python that lets you convert JSON structures back to protobuf binary format.

## Features

- Pure Python implementation with no dependencies
- Converts decoded protobuf JSON back to binary format
- Support for nested messages, repeated fields, and wire type customization
- Perfect for API reverse engineering and testing

## Installation


git clone https://github.com/emrovsky/minipb.git
cd minipb
```

## Usage

Take a decoded protobuf payload from HTTP Toolkit and convert it back to binary:

```python
from minipb import convert_json_to_protobuf_hex

# JSON structure from HTTP Toolkit's decoded protobuf 
data = {
    "1": "X-oVtzDcTGjZVms4LEgykmnCV",
    "2": "03AFcWeA4LNUlmsn9Fq4alUra4VlBUh4JI2RPYvjV-XZeS-2Q43TCPN_UmTMG..."
}

# Convert back to protobuf binary
binary_data = convert_json_to_protobuf_hex(data)
print(binary_data.hex())
```

## How It Works

1. Intercept API traffic with [HTTP Toolkit](https://httptoolkit.com/)
2. HTTP Toolkit automatically decodes protobuf payloads into readable JSON
3. Copy the decoded JSON structure
4. Use minipb to convert it back to binary format
5. Optionally modify fields before re-encoding

![HTTP Toolkit Example](https://github.com/user-attachments/assets/fcc6b67b-a7c9-4d94-93b3-21ca6b204b4b)


## Examples

### User Data Example

```python
# Schema with explicit wire type specifications
user_schema = {
    "2": 0,    # Age as varint (default, but being explicit)
    "4.1.1": 0 # Phone type as varint
}

user_data = {
    "1": "user123",
    "2": 25,
    "3": {
        "1": "123 Main St",
        "2": "Anytown",
        "3": "CA", 
        "4": "12345"
    },
    "4": [
        {
            "1": 1,
            "2": "555-1234"
        },
        {
            "1": 2,
            "2": "555-5678"
        }
    ]
}

binary = convert_json_to_protobuf_hex(user_data, user_schema)
```

### Handling Special Wire Types

Sometimes you need to override the default wire type encoding:

```python
# Force field 4.1 to be encoded as bytes (wire type 2) instead of varint
spotify_schema = {
    "4.1": 2
}

data = {
    "1": {
        "1": "client_id",
        "2": "device_id"
    },
    "4": {
        "1": [1],  # This field needs special handling
        "2": {
            "1": 1,
            "2": "https://example.com/callback"
        }
    }
}

binary = convert_json_to_protobuf_hex(data, spotify_schema)
```

## Use Cases

- Re-encode HTTP Toolkit's decoded protobuf messages
- Modify API request payloads and re-encode them
- Test APIs by creating protobuf messages without .proto files
- Reverse engineer proprietary protobuf-based APIs

## Workflow

1. Capture API traffic with HTTP Toolkit
2. Examine the auto-decoded protobuf structure
3. Modify fields as needed
4. Use minipb to convert back to binary
5. Send to target API

## Inspiration

Inspired by work from [@xtekky](https://github.com/xtekky) [@project]([https://github.com/xtekky](https://github.com/onlpx/pyproto)).

## Contact

Discord: @emrovsky

## License

MIT
```
