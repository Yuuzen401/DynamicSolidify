# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from .helper import *

class DynamicSolidifyList():

    instance_list = {}
    index = -1

    @classmethod
    def setInstance(self, index) :
        if 0 > index :
            return None
        self.instance_list[index] = DynamicSolidify(index)

    @classmethod
    def getInstance(self, index) :
        if 0 > index :
            return None
        instance = self.instance_list[index] if index in self.instance_list.keys() else None
        if instance is None:
            self.setInstance(index)
            instance = self.instance_list[index]
        return instance

    @classmethod
    def getActiveIndex(self) :
        return bpy.context.scene.dynamic_solidfy_collection_active_index

    @classmethod
    def existActiveIndex(self) :
        index = self.getActiveIndex()
        return index > -1

    @classmethod
    def getActiveItem(self) :
        active_index = self.getActiveIndex()
        return bpy.context.scene.dynamic_solidfy_collection[active_index] if active_index > -1 else None

    @classmethod
    def setItemName(self, index, item_name) :
        bpy.context.scene.dynamic_solidfy_collection[index].dsc_item_name = item_name

    @classmethod
    def getTargetObj(self, index) :
        return bpy.context.scene.dynamic_solidfy_collection[index].dsc_target_obj if index > -1 else None

    @classmethod
    def setTargetObjMod(self, index, mod_name) :
        bpy.context.scene.dynamic_solidfy_collection[index].dsc_target_obj_mod = mod_name

    @classmethod
    def getTargetObjMod(self, index) :
        return bpy.context.scene.dynamic_solidfy_collection[index].dsc_target_obj_mod

    @classmethod
    def getThickness(self, index) :
        return bpy.context.scene.dynamic_solidfy_collection[index].dsc_thickness if index > -1 else None

    @classmethod
    def setViewDistance(self, index, distance) :
        bpy.context.scene.dynamic_solidfy_collection[index].dsc_view_distance = distance

    @classmethod
    def getViewDistance(self, index) :
        return bpy.context.scene.dynamic_solidfy_collection[index].dsc_view_distance if index > -1 else DynamicSolidifyConst.VIEW_DISTANCE_INIT

    @classmethod
    def getDistanceMultiply(self, index) :
        return bpy.context.scene.dynamic_solidfy_collection[index].dsc_distance_multiply if index > -1 else 0

    # @classmethod
    # def enumMethodToMath(self, index) :
    #     dsc_method = bpy.context.scene.dynamic_solidfy_collection[index].dsc_method
    #     if DynamicSolidifyConst.ENUM_METHOD_THIN_FOR_SHORT == dsc_method :
    #         return -1
    #     elif DynamicSolidifyConst.ENUM_METHOD_THIN_FOR_LONG == dsc_method :
    #         return 1
    #     else :
    #         return 0

    @classmethod
    def getSolidifyMod(self, index):
        obj = self.getTargetObj(index)
        if obj is None:
            return None
        mod_index = int(self.getTargetObjMod(index))
        for i, mod in enumerate(obj.modifiers):
            if i == mod_index:
                return mod
        return None

class DynamicSolidify:

    handler = None

    def __init__(self, index):
        self.index = index

    def existIndex(self) :
        return self.index > -1

    def setHandler(self, handler) :
        self.handler = handler

    def getHandler(self) :
        return self.handler

    def isEnable(self):
        return True if self.getHandler() else False

    def __handle_add(self) :
        handler = bpy.types.SpaceView3D.draw_handler_add(self.__draw, (), 'WINDOW', 'POST_VIEW')
        self.setHandler(handler)

    def __handle_remove(self):
        handler = self.getHandler()
        bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        self.setHandler(None)
        DynamicSolidifyList.setViewDistance(self.index, DynamicSolidifyConst.VIEW_DISTANCE_INIT)

    def __draw(self):
        mod = DynamicSolidifyList.getSolidifyMod(self.index)
        if mod is not None:
            space_view_3d = get_space_view_3d()
            v1, _, _, = bpy.context.active_object.matrix_world.decompose()
            v2, _, _, = space_view_3d.region_3d.view_matrix.decompose()
            distance = distance_3d(v1.x, v1.y, v1.z, v2.x, v2.y, v2.z)
            mod.thickness = DynamicSolidifyList.getThickness(self.index) * (distance * DynamicSolidifyList.getDistanceMultiply(self.index))
            DynamicSolidifyList.setViewDistance(self.index, abs(distance))

    def execute(self):
        if self.existIndex():
            # enable to disable
            if self.isEnable():
                self.__handle_remove()
            # disable to enable
            else:
                self.__handle_add()

class DynamicSolidifyConst:

    ITEM_NAME_INIT = "empty object"
    OBJ_MOD_EMPTY = "9999"
    VIEW_DISTANCE_INIT = -1
    # ENUM_METHOD_THIN_FOR_SHORT = "THIN_FOR_SHORT"
    # ENUM_METHOD_THIN_FOR_LONG = "THIN_FOR_LONG"
    