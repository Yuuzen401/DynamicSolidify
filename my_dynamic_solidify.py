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
    def removeInstance(self) :
        collection = bpy.context.scene.dynamic_solidify_collection
        # listの中にあるindexがcollectionに存在しない場合は削除する
        for key in list(self.instance_list) :
            is_pop = True
            for item_i, item in enumerate(collection) :
                if key == item_i :
                    is_pop = False
                    break
            if is_pop :
                self.instance_list[key].removeHandler()
                self.instance_list.pop(key)

    @classmethod
    def getActiveIndex(self) :
        return bpy.context.scene.dynamic_solidify_collection_active_index

    @classmethod
    def existActiveIndex(self) :
        index = self.getActiveIndex()
        return index > -1

    @classmethod
    def getActiveItem(self) :
        active_index = self.getActiveIndex()
        return bpy.context.scene.dynamic_solidify_collection[active_index] if active_index > -1 else None

    @classmethod
    def setItemName(self, index, item_name) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_item_name = item_name

    @classmethod
    def getTargetObj(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_target_obj if index > -1 else None

    @classmethod
    def setTargetObjMod(self, index, mod_name) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_target_obj_mod = mod_name

    @classmethod
    def getTargetObjMod(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_target_obj_mod

    @classmethod
    def setThickness(self, index, thickness) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness = thickness

    @classmethod
    def getThickness(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness if index > -1 else None

    @classmethod
    def setViewDistance(self, index, distance) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_view_distance = distance

    @classmethod
    def getViewDistance(self, index) :
        return round(bpy.context.scene.dynamic_solidify_collection[index].dsc_view_distance if index > -1 else DynamicSolidifyConst.VIEW_DISTANCE_INIT, 2)

    @classmethod
    def getDistanceMultiply(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_distance_multiply if index > -1 else 0

    @classmethod
    def getThicknessMultiplyMax(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness_multiply_max if index > -1 else 0

    @classmethod
    def getThicknessMax(self, index) :
        return round(self.getThickness(index) * self.getThicknessMultiplyMax(index), 2)

    # @classmethod
    # def enumMethodToMath(self, index) :
    #     dsc_method = bpy.context.scene.dynamic_solidify_collection[index].dsc_method
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

    def addHandler(self) :
        handler = bpy.types.SpaceView3D.draw_handler_add(self.draw, (), 'WINDOW', 'POST_VIEW')
        self.setHandler(handler)

    def removeHandler(self):
        handler = self.getHandler()
        if handler is not None :
            bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
            self.setHandler(None)

    def draw(self):
        mod = DynamicSolidifyList.getSolidifyMod(self.index)
        if mod is not None:
            space_view_3d = get_space_view_3d()
            v1, _, _, = bpy.context.active_object.matrix_world.decompose()
            v2, _, _, = space_view_3d.region_3d.view_matrix.decompose()
            distance = distance_3d(v1.x, v1.y, v1.z, v2.x, v2.y, v2.z)
            thickness = DynamicSolidifyList.getThickness(self.index)
            distance_to_thickness = thickness * (distance * DynamicSolidifyList.getDistanceMultiply(self.index))
            max_thickness = DynamicSolidifyList.getThicknessMax(self.index)

            # 上限値の確認をする
            distance_to_thickness = max_thickness if abs(max_thickness) < abs(distance_to_thickness) else distance_to_thickness

            # 下限値の確認をする
            distance_to_thickness = DynamicSolidifyConst.THICKNESS_MIN if DynamicSolidifyConst.THICKNESS_MIN > abs(distance_to_thickness) else distance_to_thickness

            # モディファイアの厚さを設定する
            mod.thickness = round(distance_to_thickness, 2)

            # オブジェクトと3Dviewの距離を設定する
            DynamicSolidifyList.setViewDistance(self.index, abs(distance))

    def execute(self):
        if self.existIndex():
            # enable to disable
            if self.isEnable():
                self.removeHandler()
                DynamicSolidifyList.setViewDistance(self.index, DynamicSolidifyConst.VIEW_DISTANCE_INIT)
            # disable to enable
            else:
                self.addHandler()

class DynamicSolidifyConst:

    ITEM_NAME_INIT = "empty object"
    OBJ_MOD_EMPTY = "9999"
    VIEW_DISTANCE_INIT = -1
    THICKNESS_MIN = 0
    # ENUM_METHOD_THIN_FOR_SHORT = "THIN_FOR_SHORT"
    # ENUM_METHOD_THIN_FOR_LONG = "THIN_FOR_LONG"
    