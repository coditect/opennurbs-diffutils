import re
import rhino3dm

from ..abstractmodel import Value, RegexParseableValue, FloatValue

from .transform import Transformation


class Color(RegexParseableValue):

    _LABEL = "color"
    _PATTERN = re.compile(r"\s*\((\d+)[,\s]+(\d+)[,\s]+(\d+)[,\s]+(\d+)\)")

    def __str__(self):
        return f"({self.value[0]}, {self.value[1]}, {self.value[2]}, {self.value[3]})"

    @staticmethod
    def _createValueFromMatch(match):
        r = int(match[1])
        g = int(match[2])
        b = int(match[3])
        a = int(match[4])
        return (r, g, b, a)


# class TupleValue(Value)
#     def defineSubclass(self, member_classes: Iterable[Type[Value]], begin="(", end=")", delimiter=","):


class Interval(Value):

    _LABEL = "interval"

    def __str__(self):
        t0 = FloatValue(self.value.T0)
        t1 = FloatValue(self.value.T1)
        return f"[{t0}, {t1}]"

    @classmethod
    def fromString(cls, text):
        try:
            text, count = re.subn(r"^\s*\[\s*", "", text)
            if count != 1:
                raise
            t0, text = FloatValue.fromString(text)
            text, count = re.subn(r"^\s*,\s*", "", text)
            if count != 1:
                raise
            t1, text = FloatValue.fromString(text)
            text, count = re.subn(r"^\s*\]\s*", "", text)
            if count != 1:
                raise
        except:
            raise Exception(f"'{input}' is not a valid {cls._LABEL}")
        interval = rhino3dm.Interval(t0.value, t1.value)
        return cls(interval), text


class Object3d(RegexParseableValue):

    _PATTERN = re.compile(r"\s*\(([-\.\d\.]+)[,\s]+([-\.\d\.]+)[,\s]+([-\.\d\.]+)\)")

    def __str__(self):
        return f"({self.value.X}, {self.value.Y}, {self.value.Z})"


class Point3d(Object3d):

    _LABEL = "3D point"

    @staticmethod
    def _createValueFromMatch(match):
        x = float(match[1])
        y = float(match[2])
        z = float(match[3])
        return rhino3dm.Point3d(x, y, z)


class Vector3d(Object3d):

    _LABEL = "3D vector"

    @staticmethod
    def _createValueFromMatch(match):
        x = float(match[1])
        y = float(match[2])
        z = float(match[3])
        return rhino3dm.Vector3d(x, y, z)


class GeometricValue(Value):
    def __str__(self):
        raise NotImplementedError()

    @classmethod
    def fromString(self, raw):
        raise NotImplementedError()

    @classmethod
    def deltaType(cls):
        return Transformation


class Line(GeometricValue):
    def __eq__(self, other):
        return self.value.From == other.value.From and self.value.To == other.value.To

    def diff(self, other):
        older: rhino3dm.Line = self.value
        newer: rhino3dm.Line = other.value

        vector = rhino3dm.Vector3d(
            newer.From.X - older.From.X,
            newer.From.Y - older.From.Y,
            newer.From.Z - older.From.Z,
        )

        translation = rhino3dm.Transform.Translation(vector)
        dilation = rhino3dm.Transform.Scale(older.From, newer.Length / older.Length)
        rotation = rhino3dm.Transform.Rotation(
            older.Direction, newer.Direction, older.From
        )

        return Transformation(
            rhino3dm.Transform.Multiply(
                rhino3dm.Transform.Multiply(translation, rotation), dilation
            )
        )


class Arc(GeometricValue):
    def __eq__(self, other):
        return (
            self.value.Center == other.value.Center
            and self.value.Radius == other.value.Radius
            and self.value.Plane.ZAxis == other.value.Plane.ZAxis
            and self.value.AngleRadians == other.value.AngleRadians
        )

    def diff(self, other):
        older: rhino3dm.Arc = self.value
        newer: rhino3dm.Arc = other.value

        dilation = rhino3dm.Transform.Scale(older.Center, newer.Radius / older.Radius)
        rotation = rhino3dm.Transform.PlaneToPlane(older.Plane, newer.Plane)

        return Transformation(rhino3dm.Transform.Multiply(dilation, rotation))


# From detector_old.cxx:434-449

# void ComponentChangeDetector::detectChanges(Pair<const ON_ArcCurve*> curves)
# {
# 	auto plane = curves.get(Properties::ArcCurve::Plane.getter);
# 	auto radius = curves.get(Properties::ArcCurve::Radius.getter);

# 	ON_Xform dilation = ON_Xform::ScaleTransformation(plane.older.origin, radius.newer / radius.older);
# 	ON_Xform rotation;
# 	rotation.Rotation(plane.older, plane.newer);

# 	ON_Xform composed = dilation * rotation;

# 	if (!composed.IsIdentity())
# 	{
# 		this->record("Arc", composed);
# 	}
# }
