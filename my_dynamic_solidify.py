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
from .prop_detail import DynamicSolidifyModifiers

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
    def setThickness(self, index, thickness) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness = thickness

    @classmethod
    def getThickness(self, index) :
        modifiers, modifiers_select_index = DynamicSolidifyModifiers.getNoContextModifiers(index)
        return None if modifiers is None else modifiers[modifiers_select_index].modifier_thickness

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
    def getThicknessMultiplyMin(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness_multiply_min if index > -1 else 0

    @classmethod
    def getThicknessMinIfDistance(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness_min_if_distance if index > -1 else 0

    @classmethod
    def getThicknessMax(self, index) :
        return round(self.getThickness(index) * self.getThicknessMultiplyMax(index), 2)

    @classmethod
    def getThicknessMin(self, index) :
        return round(self.getThickness(index) * self.getThicknessMultiplyMin(index), 2)

    @classmethod
    def isItemMax(self) :
        return len(bpy.context.scene.dynamic_solidify_collection) >= 10

    @classmethod
    def getSolidifyMod(self, index):
        obj = self.getTargetObj(index)
        if obj is None:
            return None
        modifiers, modifiers_select_index = DynamicSolidifyModifiers.getNoContextModifiers(index)
        modifier_name = modifiers[modifiers_select_index].modifier_name
        return obj.modifiers.get(modifier_name)

    @classmethod
    def getDynamicSolidifyMod(self, index):
        obj = self.getTargetObj(index)
        return obj.modifiers.get(DynamicSolidifyConst.MODIFIER_NAME)

    @classmethod
    def removeDynamicSolidifyMod(self, index):
        obj = self.getTargetObj(index)
        for modifier in obj.modifiers :
            if DynamicSolidifyConst.MODIFIER_NAME == modifier.name :
                obj.modifiers.remove(modifier)

    @classmethod
    def setUpObj(self, index):
        obj = self.getTargetObj(index)
        mod = self.getSolidifyMod(index)
        new_mod = obj.modifiers.new(DynamicSolidifyConst.MODIFIER_NAME, mod.type)
        for prop in dir(mod):
            if prop.startswith((
                "bevel_convex",
                "edge_crease_inner",
                "edge_crease_outer",
                "edge_crease_rim",
                "invert_vertex_group",
                "material_offset",
                "material_offset_rim",
                "nonmanifold_boundary_mode",
                "nonmanifold_merge_threshold",
                "nonmanifold_thickness_mode",
                "offset",
                "rim_vertex_group",
                "shell_vertex_group",
                "solidify_mode",
                "thickness",
                "thickness_clamp",
                "thickness_vertex_group",
                "use_even_offset",
                "use_flat_faces",
                "use_flip_normals",
                "use_quality_normals",
                "use_rim",
                "use_rim_only",
                "use_thickness_angle_clamp",
                "vertex_group",
            )) :
                    setattr(new_mod, prop, getattr(mod, prop))
        orig_mod_index = obj.modifiers.find(mod.name)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_move_to_index(modifier = DynamicSolidifyConst.MODIFIER_NAME, index = orig_mod_index + 1)

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
        mod = DynamicSolidifyList.getDynamicSolidifyMod(self.index)
        if mod is not None:
            space_view_3d = get_space_view_3d()
            v1, _, _, = bpy.context.active_object.matrix_world.decompose()
            v2, _, _, = space_view_3d.region_3d.view_matrix.decompose()
            distance = distance_3d(v1.x, v1.y, v1.z, v2.x, v2.y, v2.z)
            thickness = DynamicSolidifyList.getThickness(self.index)
            distance_to_thickness = thickness * (distance * DynamicSolidifyList.getDistanceMultiply(self.index))
            max_thickness = DynamicSolidifyList.getThicknessMax(self.index)

            # 上限値の確認をする
            if abs(max_thickness) < abs(distance_to_thickness) :
                distance_to_thickness = max_thickness

            # 指定した距離が実値の距離より大きい状態になった場合は厚さを下限値にする
            if DynamicSolidifyList.getThicknessMinIfDistance(self.index) >= abs(distance) :
                distance_to_thickness = DynamicSolidifyList.getThicknessMin(self.index)

            # モディファイアの厚さを設定する
            mod.thickness = round(distance_to_thickness, 2)

            # オブジェクトと3Dviewの距離を設定する
            DynamicSolidifyList.setViewDistance(self.index, abs(distance))

    def execute(self):
        if self.existIndex():
            # enable to disable
            if self.isEnable():
                DynamicSolidifyList.getSolidifyMod(self.index).show_viewport = True
                DynamicSolidifyList.removeDynamicSolidifyMod(self.index)
                self.removeHandler()
                DynamicSolidifyList.setViewDistance(self.index, DynamicSolidifyConst.VIEW_DISTANCE_INIT)
            # disable to enable
            else:
                DynamicSolidifyList.getSolidifyMod(self.index).show_viewport = False
                DynamicSolidifyList.removeDynamicSolidifyMod(self.index)
                DynamicSolidifyList.setUpObj(self.index)
                self.addHandler()

class DynamicSolidifyConst:

    ITEM_NAME_INIT = "empty object"
    OBJ_MOD_EMPTY = "9999"
    VIEW_DISTANCE_INIT = -1
    THICKNESS_MIN = 0
    MODIFIER_NAME = "__DynamicSolidify__"