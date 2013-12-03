"""
Key/Length/Value encoding and decoding
"""

def decode_ber(ber):
    """
    Decodes an array of bytes to an integer value

    If the first byte in the BER length field does not have the high bit set (0x80),
    then that single byte represents an integer between 0 and 127 and indicates
    the number of Value bytes that immediately follows. If the high bit is set,
    then the lower seven bits indicate how many bytes follow that make up a length field
    """
    length = ber[0]
    bytes_read = 1
    if length > 127:
        bytes_read += length & 127 # Strip off the high bit
        length = 0
        for i in range(1, bytes_read):
            length += ber[i] << (8 * (bytes_read - i - 1))
    return length, bytes_read

def encode_ber(value, ber_length=0):
    """
    Encodes an integer to BER
    The length of the encoded BER value (in bytes) can be optionally specified
    """
    if not ber_length:
        if value < 127:
            return [value]
        elif value < 256:
            ber_length = 2
        elif value < 256 * 256:
            ber_length = 3
        elif value < 256 * 256 * 256:
            ber_length = 4
        else:
            ber_length = 5 # 32 bit unsigned int is the max for this function
    # Add the BER byte length
    ber = [127 + ber_length]
    for i in range(1, ber_length):
        ber.append( (value >> (8 * (ber_length - i - 1))) & 255 )
    return ber

def encode(key, value, ber_length=0):
    """
    Encodes a key and value into a KLV
    """
    return key + encode_ber(len(value), ber_length) + value

def decode(k, key_length):
    """
    Decodes a klv message
    """
    key = k[:key_length]
    val_length, ber_length = decode_ber(k[key_length:])
    value = k[key_length + ber_length : key_length + ber_length + val_length]
    return key, value