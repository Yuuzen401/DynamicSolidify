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
    def existIndex(self, list, index) :
        try:
            list[index]
        except IndexError:
            return False
        return True

    @classmethod
    def emptyIndex(self, index) :
        return index == DynamicSolidifyConst.NO_INDEX

    @classmethod
    def removeInstance(self, scene, index) :
        # 作業用モディファイアを作成する前の状態に戻す
        self.rollbackOriginalSolidifyMod(index)

        # コレクションに設定したモディファイアをリセットする
        DynamicSolidifyModifiers.resetModifiers(scene, index)

        # ハンドルを削除する
        self.instance_list[index].removeHandler()

        # 最後にリストから削除する
        self.instance_list.pop(index)

    @classmethod
    def removeInstanceAll(self, scene) :
        for index in list(self.instance_list.keys()) :
            self.removeInstance(scene, index)

    @classmethod
    def getActiveIndex(self) :
        return bpy.context.scene.dynamic_solidify_collection_active_index

    @classmethod
    def existActiveIndex(self) :
        index = self.getActiveIndex()
        return index > DynamicSolidifyConst.NO_INDEX

    @classmethod
    def getActiveItem(self) :
        active_index = self.getActiveIndex()
        return bpy.context.scene.dynamic_solidify_collection[active_index] if active_index > DynamicSolidifyConst.NO_INDEX else None

    @classmethod
    def setItemName(self, index, item_name) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_item_name = item_name

    @classmethod
    def setTargetObj(self, index, obj) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_target_obj = obj

    @classmethod
    def getTargetObj(self, index) :
        collection = bpy.context.scene.dynamic_solidify_collection
        if self.existIndex(collection, index) :
            return collection[index].dsc_target_obj if index > DynamicSolidifyConst.NO_INDEX else None
        else :
            return None

    @classmethod
    def existTargetObj(self, index):
        obj = self.getTargetObj(index)
        if obj is None :
            False
        for i, item in enumerate(bpy.context.scene.dynamic_solidify_collection) :
            # 一致するオブジェクトのみ。自分自身である場合は除外する。
            if item.dsc_target_obj == obj and not (i == index):
                return True
        return False

    @classmethod
    def getOriginalThickness(self, index) :
        modifiers, modifiers_select_index = DynamicSolidifyModifiers.getNoContextModifiers(index)
        return None if modifiers is None else modifiers[modifiers_select_index].modifier_thickness

    @classmethod
    def setViewDistance(self, index, distance) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_view_distance = distance

    @classmethod
    def getViewDistance(self, index) :
        return round(bpy.context.scene.dynamic_solidify_collection[index].dsc_view_distance if index > DynamicSolidifyConst.NO_INDEX else DynamicSolidifyConst.VIEW_DISTANCE_INIT, 2)

    @classmethod
    def getDistanceMultiply(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_distance_multiply * 0.01 if index > DynamicSolidifyConst.NO_INDEX else 0

    @classmethod
    def getThicknessMinIfDistance(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness_min_if_distance if index > DynamicSolidifyConst.NO_INDEX else 0

    @classmethod
    def setThicknessMax(self, index, thickness) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness_max = thickness

    @classmethod
    def setThicknessMin(self, index, thickness) :
        bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness_min = thickness

    @classmethod
    def getThicknessMax(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness_max if index > DynamicSolidifyConst.NO_INDEX else 0

    @classmethod
    def getThicknessMin(self, index) :
        return bpy.context.scene.dynamic_solidify_collection[index].dsc_thickness_min if index > DynamicSolidifyConst.NO_INDEX else 0

    @classmethod
    def isItemMax(self) :
        return len(bpy.context.scene.dynamic_solidify_collection) >= 10

    @classmethod
    def isItemNone(self) :
        return len(bpy.context.scene.dynamic_solidify_collection) == 0

    @classmethod
    def getOriginalSolidifyMod(self, index) :
        if self.emptyIndex(index) : return None
        obj = self.getTargetObj(index)
        if obj is None:
            return None
        modifiers, modifiers_select_index = DynamicSolidifyModifiers.getNoContextModifiers(index)
        if self.emptyIndex(modifiers_select_index) : return None
        modifier_name = modifiers[modifiers_select_index].modifier_name
        return obj.modifiers.get(modifier_name)

    @classmethod
    def isOriginalThicknessSub(self, index) :
        mod = self.getOriginalSolidifyMod(index)
        return 0 > mod.thickness

    @classmethod
    def isOriginalThicknessSubToSub(self, index, value) :
        """元の厚さがマイナス値である場合はマイナスに変換する
        """
        return value * -1 if self.isOriginalThicknessSub(index) else value

    @classmethod
    def rollbackOriginalSolidifyMod(self, index) :
        """ソリッドモディファイアを複製する前の状態に戻す
        """
        mod = DynamicSolidifyList.getOriginalSolidifyMod(index)
        if mod is not None :
            mod.show_viewport = True
            self.removeDynamicSolidifyMod(index)

    @classmethod
    def getDynamicSolidifyMod(self, index) :
        if self.emptyIndex(index) : return None
        obj = self.getTargetObj(index)
        if obj is None :
            return None
        else :
            return obj.modifiers.get(DynamicSolidifyConst.MODIFIER_NAME)

    @classmethod
    def removeDynamicSolidifyMod(self, index) :
        obj = self.getTargetObj(index)
        for modifier in obj.modifiers :
            if DynamicSolidifyConst.MODIFIER_NAME == modifier.name :
                obj.modifiers.remove(modifier)

    @classmethod
    def setUpObj(self, index):
        # セットアップする前に同じ名前のセットアップしたモディファイアを削除する
        self.removeDynamicSolidifyMod(index)
        obj = self.getTargetObj(index)
        mod = self.getOriginalSolidifyMod(index)
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
        return self.index > DynamicSolidifyConst.NO_INDEX

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
        obj = DynamicSolidifyList.getTargetObj(self.index)
        mod = DynamicSolidifyList.getDynamicSolidifyMod(self.index)

        # 距離を算出するエリアを検索する
        count = 0
        use_space = None
        for area in bpy.context.screen.areas :
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    if str(count) == bpy.context.scene.dynamic_solidify_prop.target_area :
                        use_space = space
                        break
                    count = count + 1

            # スペースが見つかった時点で終了する
            if use_space is not None :
                break

        # 必要なものが全て取得できている場合に処理を実行する
        if obj is not None \
            and mod is not None \
            and use_space is not None :

            v1, _, _, = obj.matrix_world.decompose()
            v2, _, _, = use_space.region_3d.view_matrix.decompose()
            original_thickness = abs(DynamicSolidifyList.getOriginalThickness(self.index))
            distance = abs(distance_3d(v1.x, v1.y, v1.z, v2.x, v2.y, v2.z))

            # オブジェクトと3Dviewの距離を設定する
            DynamicSolidifyList.setViewDistance(self.index, distance)

            # 0にするdistans値を補正する。
            min_distance = DynamicSolidifyList.getThicknessMinIfDistance(self.index)
            distance = distance - min_distance

            # マイナス補正で 0 になった場合は強制的に 0 にする
            if 0 > distance :
                distance = 0
            strength = DynamicSolidifyList.getDistanceMultiply(self.index)

            # 元の厚さで距離から厚さに変換する
            distance_to_thickness = original_thickness * (distance * strength)

            # 上限値と下限値の確認をする
            max_thickness = DynamicSolidifyList.getThicknessMax(self.index)
            min_thickness = DynamicSolidifyList.getThicknessMin(self.index)
            if max_thickness < distance_to_thickness :
                distance_to_thickness = DynamicSolidifyList.isOriginalThicknessSubToSub(self.index, max_thickness)

            elif min_thickness > distance_to_thickness :
                distance_to_thickness = DynamicSolidifyList.isOriginalThicknessSubToSub(self.index, min_thickness)
            else :
                distance_to_thickness = DynamicSolidifyList.isOriginalThicknessSubToSub(self.index, distance_to_thickness)

            # モディファイアの厚さを設定する
            mod.thickness = round(distance_to_thickness, 4)
        
        else :
            # 条件を満たさない場合は強制的に解除する
            DynamicSolidifyList.rollbackOriginalSolidifyMod(self.index)
            self.removeHandler()
            DynamicSolidifyList.setViewDistance(self.index, DynamicSolidifyConst.VIEW_DISTANCE_INIT)

    def execute(self):
        if self.existIndex():
            # enable to disable
            if self.isEnable():
                DynamicSolidifyList.rollbackOriginalSolidifyMod(self.index)
                self.removeHandler()
                DynamicSolidifyList.setViewDistance(self.index, DynamicSolidifyConst.VIEW_DISTANCE_INIT)
            # disable to enable
            else:
                mod = DynamicSolidifyList.getOriginalSolidifyMod(self.index)
                mod.show_viewport = False
                DynamicSolidifyList.setUpObj(self.index)

                # 有効化したときに厚さの最大値が0である場合は元の厚さで設定する
                thickness_max = DynamicSolidifyList.getThicknessMax(self.index)
                if thickness_max == 0 :
                    mod = DynamicSolidifyList.getOriginalSolidifyMod(self.index)
                    DynamicSolidifyList.setThicknessMax(self.index, abs(mod.thickness))

                self.addHandler()

class DynamicSolidifyConst:

    ITEM_NAME_INIT = ""
    OBJ_MOD_EMPTY = "9999"
    VIEW_DISTANCE_INIT = -1
    THICKNESS_MIN = 0
    MODIFIER_NAME = "__DynamicSolidify__"
    COLLECTION_MAX = 10
    NO_INDEX = -1