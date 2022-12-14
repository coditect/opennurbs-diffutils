from pathlib import Path
from rhino3dm import File3dm

from ..abstractmodel import ModelDelta, ModelType, Pair, Session

from .entity_types import ENTITY_TYPES
from .properties import ModelProperties
from .tables import ALL_TABLES

# from wrapt import ObjectProxy

# class ModelWrapper(ObjectProxy):
#     @property
#     def model(self):
#         return self


FILE3DM_TYPE = ModelType(ALL_TABLES, ENTITY_TYPES, ModelProperties)


class File3dmDelta(ModelDelta):
    def __init__(self, type=FILE3DM_TYPE):
        super().__init__(type)

    def comparePaths(self, paths: Pair[Path], session: Session):
        olderModel = File3dm.Read(str(paths[0]))
        if olderModel is None:
            raise ValueError(f"Failed to read file {paths[0]}")

        newerModel = File3dm.Read(str(paths[1]))
        if newerModel is None:
            print(f"Failed to read file {paths[1]}")
            exit(1)

        # olderModel = ModelWrapper(olderModel)
        # newerModel = ModelWrapper(newerModel)
        self.compare((olderModel, newerModel), session)
        self.setFilePaths(paths)
