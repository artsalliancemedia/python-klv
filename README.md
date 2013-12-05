[![Build Status](https://travis-ci.org/artsalliancemedia/python-klv.png)](http://travis-ci.org/artsalliancemedia/python-klv)

KLV in Python
=============

A Python  parser for KLV (Key Length Value) encoded data. KLV encoding is commonly used in the motion picture industry.

http://en.wikipedia.org/wiki/KLV

Unit Tests
----------

Install nose:

```bash
python install nose
```

Run the command ```nosetests``` in the root directory.

Encode Key/Value
----------------

```python
import klv
key = [0x03, 0x2E, 0x5F, 0xAB, 0x08, 0x12, 0x2F, 0x0C,
       0xEE, 0x33, 0x00, 0x01, 0x02, 0x45, 0x6D, 0xDD]
value = [0x05, 0x04, 0x03, 0x02, 0x01]
klv_msg = klv.encode(key, value)
```

```klv_msg``` will be a bytearray; to convert to an array of ints, use ```list(klv_msg)``` and to convert to a string of bytes, use ```str(klv_msg)```.

Decode KLV Messages
-------------------

```python
import klv
key, value = klv.decode(klv_msg, 16)
```

Decode takes the form ```decode(<klv>,<key length>)``` to accomodate messages with different length keys. The ```key``` and ```value``` results are bytearrays.