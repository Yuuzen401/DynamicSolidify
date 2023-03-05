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
    "version": (0, 0, 3),
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

# Updater ops import, all setup in this file.
from . import addon_updater_ops
    
def update_target_obj(scene, context):
    active_index = DynamicSolidifyList.getActiveIndex()
    obj = DynamicSolidifyList.getTargetObj(active_index)
    item_name = DynamicSolidifyConst.ITEM_NAME_INIT if obj is None else obj.name
    DynamicSolidifyList.setItemName(active_index, item_name)

    items = get_target_obj_modifiers_type_solidfy(scene, context)
    if len(items) > 0 :
        DynamicSolidifyList.setTargetObjMod(active_index, items[1][0])
    else :
        DynamicSolidifyList.setTargetObjMod(active_index, items[0][0])
    
def get_target_obj_modifiers_type_solidfy(scene, context):
    items = [(DynamicSolidifyConst.OBJ_MOD_EMPTY, "", "", "", 0)]
    active_index = DynamicSolidifyList.getActiveIndex()
    obj = DynamicSolidifyList.getTargetObj(active_index)
    if obj is not None:
        for i, modifier in enumerate(obj.modifiers):
            if modifier.type == 'SOLIDIFY':
                items.append((str(i), str(i), "", "", i + 1))
    return items

class DynamicSolidifyPropertyGroup(PropertyGroup, DynamicSolidifyList):
    pass

class DynamicSolidifyCollectionPropertyGroup(PropertyGroup, DynamicSolidifyList):

    # enum_method = [
    #     (DynamicSolidifyConst.ENUM_METHOD_THIN_FOR_SHORT, "thin for short", ""),
    #     (DynamicSolidifyConst.ENUM_METHOD_THIN_FOR_LONG, "thin for long", ""),
    # ]

    dsc_item_name : StringProperty(default = DynamicSolidifyConst.ITEM_NAME_INIT, name = "item name")
    dsc_thickness : FloatProperty(name = "Thickness", default = 0.01, min = 0.0, max = 10.0)#, update = update_solidify_modifier)
    dsc_target_obj : PointerProperty(name = "target", type = bpy.types.Object, poll = lambda self, obj: obj.type == 'MESH', update = update_target_obj)
    dsc_target_obj_mod: EnumProperty(
        items = get_target_obj_modifiers_type_solidfy, name = "Modifier Type Solidfy" 
    )
    dsc_distance_multiply : FloatProperty(name = "Multiplication", default = 1, precision = 2)
    dsc_view_distance : FloatProperty(name = "distance", precision = 5, default = DynamicSolidifyConst.VIEW_DISTANCE_INIT)
    # dsc_method : EnumProperty(items = enum_method, name = "Method", default = DynamicSolidifyConst.ENUM_METHOD_THIN_FOR_SHORT)

class DynamicSolidifyOperator(Operator, DynamicSolidifyList):
    bl_idname = "dynamic_solidify.operator"
    bl_label = "Dynamic Solidify"

    index: bpy.props.IntProperty(name = "dynamic_solidify_index", default = -1)

    def execute(self, context):
        dynamic_solidify = DynamicSolidifyList.getInstance(self.index)
        dynamic_solidify.execute()

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            self.execute(context)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

class DynamicSolidifyCollectionAddOperator(Operator, DynamicSolidifyList):
    bl_idname = "dynamic_solidify_collection_add.operator"
    bl_label = ""
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        new_item = context.scene.dynamic_solidfy_collection.add()
        new_item.dsc_item_name = DynamicSolidifyConst.ITEM_NAME_INIT
        index = len(context.scene.dynamic_solidfy_collection) - 1
        context.scene.dynamic_solidfy_collection_active_index = index

        return {'FINISHED'}

class DynamicSolidifyCollectionRemoveOperator(Operator, DynamicSolidifyList):
    bl_idname = "dynamic_solidify_collection_remove.operator"
    bl_label = ""
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.dynamic_solidfy_collection

    def execute(self, context):
        s_list = context.scene.dynamic_solidfy_collection
        index = context.scene.dynamic_solidfy_collection_active_index
        s_list.remove(index)

        index = min(max(0, index - 1), len(s_list) - 1)
        context.scene.dynamic_solidfy_collection_active_index = index

        return {'FINISHED'}

class DynamicSolidifyCollectionLayout(UIList, DynamicSolidifyList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        dynamic_solidify = DynamicSolidifyList.getInstance(index)

        row = layout.row(align = True)
        row.prop(item, "dsc_item_name", text = "", emboss = False, icon = 'OBJECT_DATAMODE')        
        text = "ON" if dynamic_solidify.isEnable() else "OFF"
        depress = True if dynamic_solidify.isEnable() else False
        op = row.operator(DynamicSolidifyOperator.bl_idname, text = text, depress = depress)
        op.index = index

class DynamicSolidifyPanel(Panel, DynamicSolidifyList):
    bl_label = "DynamicSolidify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DynamicSolidify"

    def draw(self, context):
        layout = self.layout
        layout.separator()
        row = layout.row()
        row = row.row(align = True)
        row.operator(DynamicSolidifyCollectionAddOperator.bl_idname, icon = "ADD")
        row.operator(DynamicSolidifyCollectionRemoveOperator.bl_idname, icon = "REMOVE")
        row = row.column()
        row = layout.row()
        len_item = len(context.scene.dynamic_solidfy_collection)
        template_list_rows = 5 if 5 > len_item else len_item
        row.template_list(
            "DynamicSolidifyCollectionLayout", "", context.scene, "dynamic_solidfy_collection", context.scene, "dynamic_solidfy_collection_active_index", rows = template_list_rows)

        # -----------------------------------------------------------
        if DynamicSolidifyList.existActiveIndex() == False:
            return
        item = DynamicSolidifyList.getActiveItem()

        box = layout.box()
        box.scale_y = 1.5
        row = box.row()
        row.prop(item, "dsc_target_obj", text = "target")

        # オブジェクトが設定済である場合に以下のレイアウトを設定する
        if item.dsc_target_obj is not None:
            row = box.row()
            row.label(text = "Modifier Solidify Index")
            row = box.row()
            sp = row.split(align = True, factor = 0.3)
            sp.prop(item, "dsc_target_obj_mod" , text = "")

            # モディファイアが設定済である場合、モディファイアの名称を表示する
            if item.dsc_target_obj_mod:
                dsc_target_obj_mod = int(item.dsc_target_obj_mod)
                if int(DynamicSolidifyConst.OBJ_MOD_EMPTY) == dsc_target_obj_mod:
                    text = "EMPTY"
                else:
                    text = item.dsc_target_obj.modifiers[dsc_target_obj_mod].name
                sp.label(text = text, icon = "MOD_SOLIDIFY")

            # 厚さに関する設定を行う
            row = box.row()
            # row.prop(item, "dsc_method")
            # row = box.row()
            row.prop(item, "dsc_thickness", text = "Thickness")
            row = box.row()
            row.prop(item, "dsc_distance_multiply", text = "Multiply")
            if DynamicSolidifyConst.VIEW_DISTANCE_INIT == item.dsc_view_distance:
                text = "Distance : None"
            else :
                text = "Distance : " + str(item.dsc_view_distance)
            row = box.row()
            row.label(text = text)

        # -----------------------------------------------------------

classes = (
    DynamicSolidifyPropertyGroup,
    DynamicSolidifyCollectionPropertyGroup,
    DynamicSolidifyPanel,
    DynamicSolidifyPreferences,
    DynamicSolidifyOperator,
    DynamicSolidifyCollectionAddOperator,
    DynamicSolidifyCollectionRemoveOperator,
    DynamicSolidifyUpdaterPanel,
    DynamicSolidifyCollectionLayout,
    )

def register():
    addon_updater_ops.register(bl_info)
    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # Avoid blender 2.8 warnings.
        bpy.utils.register_class(cls)
    bpy.types.Scene.dynamic_solidify_prop = PointerProperty(type = DynamicSolidifyPropertyGroup)
    bpy.types.Scene.dynamic_solidfy_collection = CollectionProperty(type = DynamicSolidifyCollectionPropertyGroup)
    bpy.types.Scene.dynamic_solidfy_collection_active_index = bpy.props.IntProperty(
        name = "dynamic_solidfy_collection_active_index", default = -1)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.dynamic_solidify_prop
    del bpy.types.Scene.dynamic_solidfy_collection 
    del bpy.types.Scene.dynamic_solidfy_collection_active_index

    addon_updater_ops.unregister()

if __name__ == "__main__":
    register()