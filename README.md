# Serializer Benchmarks

File format and serializer benchmarks for the YouSense upload dataset.

Also an experiment in using PyCharm and python3-like python2.7 code.

The most important factor is serialized data size (it's often transferred over mobile networks).
Speed of serialization is secondary, as the individual writes are small enough for it not to be a bottleneck, and python serialization speeds may be very different to Java on Android.

# Initial Results

<table>
<tr><td>ujson</td><td>62.447 seconds</td><td>838 MB</td></tr>
<tr><td>msgpack</td><td>129.311 seconds</td><td>674 MB</td></tr>
<tr><td>ujson+gzip</td><td>190.586 seconds</td><td>201 MB</td></tr>
<tr><td>msgpack+gzip</td><td>263.587 seconds</td><td>205 MB</td></tr>
</table>

Conclusion: msgpack is not smaller or faster enough than json. Json is human-readable, and wins.

# TODO

* Import as much as possible from __future__, write python3-compatible code.
* Clean up directory and filename handling
* Add nice output