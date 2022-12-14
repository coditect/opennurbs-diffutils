import re
import rhino3dm
from ..abstractmodel import Delta, FloatValue


# PATTERN = re.compile(r"transform\(([-\.0-9]+)([^-\.0-9]+([-\.0-9]+))*\)", re.IGNORECASE)


class Transformation(Delta):

    __slots__ = "_transform"

    def __init__(self, transform: rhino3dm.Transform):
        self._transform = transform

    def __str__(self):
        values = [str(v) for v in self._transform.ToFloatArray(True)]
        return "transform(" + ", ".join(values) + ")"

    def __eq__(self, other):
        return (
            self._transform.M00 == other._transform.M00
            and self._transform.M01 == other._transform.M01
            and self._transform.M02 == other._transform.M02
            and self._transform.M03 == other._transform.M03
            and self._transform.M10 == other._transform.M10
            and self._transform.M11 == other._transform.M11
            and self._transform.M12 == other._transform.M12
            and self._transform.M13 == other._transform.M13
            and self._transform.M20 == other._transform.M20
            and self._transform.M21 == other._transform.M21
            and self._transform.M22 == other._transform.M22
            and self._transform.M23 == other._transform.M23
            and self._transform.M30 == other._transform.M30
            and self._transform.M31 == other._transform.M31
            and self._transform.M32 == other._transform.M32
            and self._transform.M33 == other._transform.M33
        )

    @classmethod
    def fromString(cls, raw: str):
        remainder = raw
        if raw.startswith("transform("):
            values = []
            while not re.match(r"[^-\.\d]*\)", remainder):
                remainder = re.sub(r"^[^-\.\d\)]*", "", remainder, 1)
                value, remainder = FloatValue.fromString(remainder)
                values.append(value)
            if len(values) == 16:
                t = rhino3dm.Transform(1)
                t.M00 = values[0].value
                t.M01 = values[1].value
                t.M02 = values[2].value
                t.M03 = values[3].value
                t.M10 = values[4].value
                t.M11 = values[5].value
                t.M12 = values[6].value
                t.M13 = values[7].value
                t.M20 = values[8].value
                t.M21 = values[9].value
                t.M22 = values[10].value
                t.M23 = values[11].value
                t.M30 = values[12].value
                t.M31 = values[13].value
                t.M32 = values[14].value
                t.M33 = values[15].value
                return Transformation(t), remainder

        raise Exception("Not a valid transformation")

    def apply(self, geometry, session):
        result = geometry.value.Transform(self._transform)
        if result is True:
            return geometry
        return geometry.__class__(result)

    def reverse(self):
        ok, inverse = self._transform.TryGetInverse()
        if ok:
            return Transformation(inverse)
        raise Exception("Unable to calculate inverse of transform")
