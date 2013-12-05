"""
Tests KLV functionality
"""

import unittest
import klv

class TestKLV(unittest.TestCase):
    """
    KLV tests
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_decode_ber(self):
        self.assertEqual(klv.decode_ber([0x00])[0], 0)
        self.assertEqual(klv.decode_ber([0x01])[0], 1)
        self.assertEqual(klv.decode_ber([0x7f])[0], 127)
        self.assertEqual(klv.decode_ber([0x81, 0x00])[0], 0)
        self.assertEqual(klv.decode_ber([0x81, 0x01])[0], 1)
        self.assertEqual(klv.decode_ber([0x81, 0x7f])[0], 127)
        self.assertEqual(klv.decode_ber([0x81, 0xff])[0], 255)
        self.assertEqual(klv.decode_ber([0x82, 0x00, 0x00])[0], 0)
        self.assertEqual(klv.decode_ber([0x82, 0x00, 0x01])[0], 1)
        self.assertEqual(klv.decode_ber([0x82, 0x00, 0x7f])[0], 127)
        self.assertEqual(klv.decode_ber([0x82, 0x01, 0x00])[0], 256)
        self.assertEqual(klv.decode_ber([0x83, 0x00, 0x00, 0x00])[0], 0)
        self.assertEqual(klv.decode_ber([0x83, 0x00, 0x00, 0x01])[0], 1)
        self.assertEqual(klv.decode_ber([0x83, 0x00, 0x00, 0x7f])[0], 127)
        self.assertEqual(klv.decode_ber([0x83, 0x00, 0x01, 0x00])[0], 256)
        self.assertEqual(klv.decode_ber([0x83, 0x01, 0x00, 0x00])[0], 65536)
        self.assertEqual(klv.decode_ber([0x83, 0x01, 0x00, 0x0a])[0], 65546)
        self.assertEqual(klv.decode_ber([0x83, 0x01, 0x01, 0x00])[0], 65536 + 256)
        self.assertEqual(klv.decode_ber([0x83, 0x01, 0x01, 0x01])[0], 65536 + 257)

    def test_decode_ber_with_strings(self):
        self.assertEqual(klv.decode_ber('\x7f'), (127, 1,))
        self.assertEqual(klv.decode_ber('\x81\xff'), (255, 2,))
        self.assertEqual(klv.decode_ber('\x82\x01\x00'), (256, 3,))
        self.assertEqual(klv.decode_ber('\x83\x00\x01\x00'), (256,4,))
        self.assertEqual(klv.decode_ber('\x83\x01\x01\x01'), (65536 + 257, 4,))

    def test_encode_ber(self):
        self.assertEqual(klv.encode_ber(0, 4), bytearray([0x83, 0x00, 0x00, 0x00]))
        self.assertEqual(klv.encode_ber(10, 4), bytearray([0x83, 0x00, 0x00, 0x0a]))
        self.assertEqual(klv.encode_ber(127, 4), bytearray([0x83, 0x00, 0x00, 0x7f]))
        self.assertEqual(klv.encode_ber(255, 4), bytearray([0x83, 0x00, 0x00, 0xff]))
        self.assertEqual(klv.encode_ber(256, 4), bytearray([0x83, 0x00, 0x01, 0x00]))
        self.assertEqual(klv.encode_ber(65535, 4), bytearray([0x83, 0x00, 0xff, 0xff]))
        self.assertEqual(klv.encode_ber(65536, 4), bytearray([0x83, 0x01, 0x00, 0x00]))
        self.assertEqual(klv.encode_ber(65546, 4), bytearray([0x83, 0x01, 0x00, 0x0a]))
        self.assertEqual(klv.encode_ber(65536 + 256, 4), bytearray([0x83, 0x01, 0x01, 0x00]))
        self.assertEqual(klv.encode_ber(65536 + 257, 4), bytearray([0x83, 0x01, 0x01, 0x01]))

    def test_encode_ber_with_strings(self):
        self.assertEqual(klv.encode_ber(0, 4), bytearray('\x83\x00\x00\x00'))
        self.assertEqual(klv.encode_ber(10, 4), bytearray('\x83\x00\x00\x0a'))
        self.assertEqual(klv.encode_ber(127, 4), bytearray('\x83\x00\x00\x7f'))
        self.assertEqual(klv.encode_ber(65536, 4), bytearray('\x83\x01\x00\x00'))
        self.assertEqual(klv.encode_ber(65546, 4), bytearray('\x83\x01\x00\x0a'))
        self.assertEqual(klv.encode_ber(65536 + 257, 4), bytearray('\x83\x01\x01\x01'))

    def test_encode_decode_ber(self):
        for val in (0, 10, 127, 256, 513, 65535, 65536, 65546, 104532, 256*256*256*24):
            self.assertEqual(klv.decode_ber(klv.encode_ber(val))[0], val)

    def test_encode_klv_key_length_16(self):
            key = [0x03, 0x2E, 0x5F, 0xAB, 0x08, 0x12, 0x2F, 0x0C,
                   0xEE, 0x33, 0x00, 0x01, 0x02, 0x45, 0x6D, 0xDD]
            value = [0x05, 0x04, 0x03, 0x02, 0x01]
            k = klv.encode(key, value)
            self.assertEqual(k, bytearray(key + [0x05] + value))
            k = klv.encode(key, value, 4);
            self.assertEqual(k, bytearray(key + [0x83, 0x00, 0x00, 0x05] + value))

    def test_encode_klv_key_length_18(self):
            key = [0x03, 0x2E, 0x5F, 0xAB, 0x08, 0x12, 0x2F, 0x0C, 0xEE,
                   0x33, 0x00, 0x01, 0x02, 0x45, 0x6D, 0xDD, 0x55, 0x96]
            value = list('these are little endian encoded Unicode characters'.encode('utf-16le'))
            k = klv.encode(key, value)
            self.assertEqual(k, bytearray(key + [0x64] + value))
            k = klv.encode(key, value, 4)
            self.assertEqual(k, bytearray(key + [0x83, 0x00, 0x00, 0x64] + value))

    def test_decode_klv(self):
        key = [0x03, 0x2E, 0x5F, 0xAB, 0x08, 0x12, 0x2F, 0x0C,
               0xEE, 0x33, 0x00, 0x01, 0x02, 0x45, 0x6D, 0xDD]
        value = [0x06, 0x05, 0x04, 0x03, 0x02, 0x01, 0x00]
        k = key + [0x83, 0x00, 0x00, 0x07] + value
        self.assertEqual(klv.decode(k, 16), (bytearray(key), bytearray(value),))

    def test_encode_decode_klv(self):
        key = [0x03, 0x2E, 0x5F, 0xAB, 0x08, 0x12, 0x2F, 0x0C, 0xEE,
               0x33, 0x00, 0x01, 0x02, 0x45, 0x6D, 0xDD, 0x55, 0x96]
        value = list('these are little endian encoded Unicode characters'.encode('utf-16le'))
        k = klv.encode(key, value)
        self.assertEqual(klv.decode(k, 18), (bytearray(key), bytearray(value),))

    def test_decode_klv_no_value(self):
        key = [0x03, 0x2E, 0x5F, 0xAB, 0x08, 0x12, 0x2F, 0x0C,
               0xEE, 0x33, 0x00, 0x01, 0x02, 0x45, 0x6D, 0xDD]
        k = key + [0x00]
        self.assertEqual(klv.decode(k, 16), (bytearray(key), bytearray(),))

    def test_encode_decode_klv_no_value(self):
        key = [0x03, 0x2E, 0x5F, 0xAB, 0x08, 0x12, 0x2F, 0x0C,
               0xEE, 0x33, 0x00, 0x01, 0x02, 0x45, 0x6D, 0xDD]
        value = []
        k = klv.encode(key, value)
        self.assertEqual(klv.decode(k, 16), (bytearray(key), bytearray(value),))