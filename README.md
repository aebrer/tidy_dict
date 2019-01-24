# NestedDict()

* By default, a non-existing key creates another NestedDict at that key.
* Check for non-existence carefully:
    * usually it's enough to say `if key in NestedDict`
    * but there are no missing key errors
* Prints in a non-garbage way.
