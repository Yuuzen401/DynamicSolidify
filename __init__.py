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

bl_info = {
    "name": "DynamicSolidify",
    "description": "",
    "author": "Yuuzen401",
    "version": (0, 0, 6),
    "blender": (2, 80, 0),
    "location":  "View3D > Sidebar > DynamicSolidify",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/Yuuzen401/DynamicSolidify",
    "category": "Object"
}

import bpy

from bpy.types import Operator, Panel, UIList, PropertyGroup
from bpy.props import IntProperty, FloatProperty, FloatVectorProperty, BoolProperty, PointerProperty, CollectionProperty, StringProperty, EnumProperty
from .preferences import *
from .helper import *
from .my_dynamic_solidify import DynamicSolidifyConst, DynamicSolidifyList
from .prop_detail import DynamicSolidifyModifiers

# Updater ops import, all setup in this file.
from . import addon_updater_ops
    
def update_target_obj(self, context):
    index = DynamicSolidifyList.getActiveIndex()
    # 既に同じオブジェクトが存在する場合はメッセージを出して元に戻す
    if DynamicSolidifyList.existTargetObj(index) :
        DynamicSolidifyList.setTargetObj(index, None)
        show_message_error("Same object already set")
        return 

    obj = DynamicSolidifyList.getTargetObj(index)
    item_name = DynamicSolidifyConst.ITEM_NAME_INIT if obj is None else obj.name
    DynamicSolidifyList.setItemName(index, item_name)

class DynamicSolidifyPropertyGroup(PropertyGroup, DynamicSolidifyList):
    pass

class DynamicSolidifyTargetListPropertyGroup(PropertyGroup, DynamicSolidifyList):

    dsc_item_name : StringProperty(default = DynamicSolidifyConst.ITEM_NAME_INIT, name = "item name")
    dsc_target_obj : PointerProperty(name = "target", type = bpy.types.Object, poll = lambda self, obj: obj.type == 'MESH', update = update_target_obj)
    dsc_distance_multiply : FloatProperty(name = "", default = 0.1, min = 0.01, max = 1, precision = 2)
    dsc_thickness_max : FloatProperty(name = "", default = 0, min = 0, max = 1000, precision = 4)
    dsc_thickness_min : FloatProperty(name = "", default = 0, min = 0, max = 1000, precision = 4)
    dsc_thickness_min_if_distance : FloatProperty(name = "Thickness Min IF Distance", default = 0, min = 0, max = 100)
    dsc_view_distance : FloatProperty(name = "distance", precision = 5, default = DynamicSolidifyConst.VIEW_DISTANCE_INIT)
    index: IntProperty(name = "dynamic_solidify_index", default = -1)

class DynamicSolidifyOperator(Operator, DynamicSolidifyList):
    """動的ソリッド実行
    """
    bl_idname = "dynamic_solidify.operator"
    bl_label = "Dynamic Solidify"

    # Listから押下したOperatorを識別するためパラメータ
    index: bpy.props.IntProperty(name = "dynamic_solidify_index", default = -1)

    def execute(self, context) :
        dynamic_solidify = DynamicSolidifyList.getInstance(self.index)
        dynamic_solidify.execute()

    def invoke(self, context, event) :
        if context.area.type == 'VIEW_3D':
            self.execute(context)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

class DynamicSolidifyTargetListAddOperator(Operator, DynamicSolidifyList):
    """動的ソリッド対象リスト追加
    """
    bl_idname = "dynamic_solidify_collection_add.operator"
    bl_label = ""
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context) :
        for i in range(10):
            new_item = context.scene.dynamic_solidify_collection.add()
            new_item.dsc_item_name = DynamicSolidifyConst.ITEM_NAME_INIT
            new_item.index = i
        context.scene.dynamic_solidify_collection_active_index = 0
        return {'FINISHED'}

class DynamicSolidifyTargetListRemoveOperator(Operator, DynamicSolidifyList):
    """動的ソリッド対象リスト削除
    """
    bl_idname = "dynamic_solidify_collection_remove.operator"
    bl_label = ""
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    # Listから押下したOperatorを識別するためパラメータ
    index: bpy.props.IntProperty(name = "dynamic_solidify_index", default = -1)

    @classmethod
    def poll(cls, context) :
        return context.scene.dynamic_solidify_collection

    def execute(self, context) :
        # インスタンスを破棄する
        DynamicSolidifyList.removeInstance(context.scene, self.index)

        # 削除するとindexの整合性が取れなくなる
        # collection = context.scene.dynamic_solidify_collection
        # collection.remove(self.index)
        # context.scene.dynamic_solidify_collection_active_index = -1
        return {'FINISHED'}

class DynamicSolidifyGetModListOperator(Operator, DynamicSolidifyList):
    """オブジェクトからモディファイアを取得する
    """
    bl_idname = "dynamic_solidify_get_mod_list.operator"
    bl_label = ""
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context) :
        index = DynamicSolidifyList.getActiveIndex()
        obj = DynamicSolidifyList.getTargetObj(index)
        DynamicSolidifyModifiers.resetModifiers(context.scene, index)
        item_modifiers , _ = DynamicSolidifyModifiers.getModifiers(context.scene, index)
        set_index = -1
        if obj is not None:
            for modifier in obj.modifiers:
                if modifier.type == 'SOLIDIFY' and modifier.show_viewport :
                    new_item = item_modifiers.add()
                    new_item.modifier_name = modifier.name
                    new_item.modifier_thickness = modifier.thickness
                    set_index = 0
        
        DynamicSolidifyModifiers.setModifiersSelectIndex(context.scene, index, set_index)

        return {'FINISHED'}

class DynamicSolidify_UL_TargetListLayout(UIList, DynamicSolidifyList):
    """動的ソリッド対象リストUI
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index) :
        dynamic_solidify = DynamicSolidifyList.getInstance(index)
        row = layout.row()
        col = row.column()
        col.prop(item, "dsc_item_name", text = "", emboss = False, icon = 'OBJECT_DATAMODE')        

        col = row.column()
        text = "ON" if dynamic_solidify.isEnable() else "OFF"
        depress = True if dynamic_solidify.isEnable() else False
        op = col.operator(DynamicSolidifyOperator.bl_idname, text = text, depress = depress)
        op.index = index
        if 0 > DynamicSolidifyModifiers.getModifiersSelectIndex(index):
            col.enabled = False
        col = row.column()
        op = col.operator(DynamicSolidifyTargetListRemoveOperator.bl_idname, icon = "REMOVE")
        op.index = index

class DynamicSolidify_PT_Panel(Panel, DynamicSolidifyList):
    bl_label = "DynamicSolidify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DynamicSolidify"

    def draw(self, context):
        index = DynamicSolidifyList.getActiveIndex()
        item = DynamicSolidifyList.getActiveItem()
        layout = self.layout
        layout.separator()
        row = layout.row()
        col = row.column()
        col.operator(DynamicSolidifyTargetListAddOperator.bl_idname, text = "Start", icon = "ADD")
        if DynamicSolidifyList.isItemNone() == False :
            col.enabled = False
        row = layout.row()
        len_item = len(context.scene.dynamic_solidify_collection)
        template_list_rows = 5 if 5 > len_item else len_item
        row.template_list(
            "DynamicSolidify_UL_TargetListLayout", "", context.scene, "dynamic_solidify_collection", context.scene, "dynamic_solidify_collection_active_index", rows = template_list_rows)

        # -----------------------------------------------------------
        if DynamicSolidifyList.existActiveIndex() == False :
            return

        row = layout.row()
        row.prop(item, "dsc_target_obj", text = "")

        # オブジェクトが設定済である場合に以下のレイアウトを設定する
        if item.dsc_target_obj is not None:
            row = layout.row()
            row.operator(DynamicSolidifyGetModListOperator.bl_idname, text = "Get Only View Solidify", icon = "MOD_SOLIDIFY")
            dynamic_solidify = DynamicSolidifyList.getInstance(index)

            # インスタンスが存在する　かつ　ハンドラが起動している場合は使用不可にする
            if dynamic_solidify is not None :
                if dynamic_solidify.isEnable() :
                   row.enabled = False

            row = layout.row()
            DynamicSolidifyModifiers.get_UL_Modifiers(row, context.scene, index)

            mod = DynamicSolidifyList.getDynamicSolidifyMod(index)
            if mod is not None :
                # 厚さに関する設定を行う
                row = layout.row()
                row.prop(item, "dsc_distance_multiply", text = "Strength")
                row = layout.row()
                row.prop(item, "dsc_thickness_max", text = "Max")
                row = layout.row()
                row.prop(item, "dsc_thickness_min", text = "Min")
                row = layout.row()
                row.prop(item, "dsc_thickness_min_if_distance", text = "Min Distance")
                if DynamicSolidifyConst.VIEW_DISTANCE_INIT == DynamicSolidifyList.getViewDistance(index) :
                    text = "Distance : None"
                else :
                    text = "Distance : " + str(DynamicSolidifyList.getViewDistance(index))
                row = layout.row()
                row.label(text = text)

        # -----------------------------------------------------------

classes = (
    DynamicSolidifyPropertyGroup,
    DynamicSolidifyTargetListPropertyGroup,
    DynamicSolidify_PT_Panel,
    DynamicSolidifyPreferences,
    DynamicSolidifyOperator,
    DynamicSolidifyTargetListAddOperator,
    DynamicSolidifyTargetListRemoveOperator,
    DynamicSolidifyGetModListOperator,
    DynamicSolidifyUpdaterPanel,
    DynamicSolidify_UL_TargetListLayout,
    )

def register():
    DynamicSolidifyModifiers.register()
    addon_updater_ops.register(bl_info)
    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # Avoid blender 2.8 warnings.
        bpy.utils.register_class(cls)
    bpy.types.Scene.dynamic_solidify_prop = PointerProperty(type = DynamicSolidifyPropertyGroup)
    bpy.types.Scene.dynamic_solidify_collection = CollectionProperty(type = DynamicSolidifyTargetListPropertyGroup)
    bpy.types.Scene.dynamic_solidify_collection_active_index = IntProperty(name = "dynamic_solidify_collection_active_index", default = -1)

def unregister():
    DynamicSolidifyModifiers.unregister()
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.dynamic_solidify_prop
    del bpy.types.Scene.dynamic_solidify_collection 
    del bpy.types.Scene.dynamic_solidify_collection_active_index

    addon_updater_ops.unregister()

if __name__ == "__main__":
    register()