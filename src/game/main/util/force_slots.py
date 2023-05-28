"""
Code from https://stackoverflow.com/questions/56579348/how-can-i-force-subclasses-to-have-slots
"""

class Slots(type):
    @classmethod
    def __prepare__(metaclass, name, bases, **kwds):
        # calling super is not strictly necessary because
        #  type.__prepare() simply returns an empty dict.
        # But if you plan to use metaclass-mixins then this is essential!
        super_prepared = super().__prepare__(metaclass, name, bases, **kwds)
        super_prepared['__slots__'] = ()
        return super_prepared


if __name__ == '__main__':
    pass
