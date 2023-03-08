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
from bpy.types import PropertyGroup, UIList
from bpy.props import StringProperty, IntProperty, CollectionProperty, FloatProperty

class DynamicSolidifyModifiers():

    @classmethod
    def get_UL_Modifiers(self, layout, scene, index) :
        if index > 10 :
            return None
        elif index == 0 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_0", scene, "dynamic_solidify_modifiers_select_index_0")
        elif index == 1 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_1", scene, "dynamic_solidify_modifiers_select_index_1")
        elif index == 2 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_2", scene, "dynamic_solidify_modifiers_select_index_2")
        elif index == 3 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_3", scene, "dynamic_solidify_modifiers_select_index_3")
        elif index == 4 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_4", scene, "dynamic_solidify_modifiers_select_index_4")
        elif index == 5 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_5", scene, "dynamic_solidify_modifiers_select_index_5")
        elif index == 6 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_6", scene, "dynamic_solidify_modifiers_select_index_6")
        elif index == 7 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_7", scene, "dynamic_solidify_modifiers_select_index_7")
        elif index == 8 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_8", scene, "dynamic_solidify_modifiers_select_index_8")
        elif index == 9 :
            return layout.template_list("DynamicSolidify_UL_Modifiers", "", scene, "dynamic_solidify_modifiers_9", scene, "dynamic_solidify_modifiers_select_index_9")

    @classmethod
    def getModifiers(self, scene, index) :
        if index > 10 :
            return (None, None)
        elif index == 0 :
            return (scene.dynamic_solidify_modifiers_0, scene.dynamic_solidify_modifiers_select_index_0)
        elif index == 1 :
            return (scene.dynamic_solidify_modifiers_1, scene.dynamic_solidify_modifiers_select_index_1)
        elif index == 2 :
            return (scene.dynamic_solidify_modifiers_2, scene.dynamic_solidify_modifiers_select_index_2)
        elif index == 3 :
            return (scene.dynamic_solidify_modifiers_3, scene.dynamic_solidify_modifiers_select_index_3)
        elif index == 4 :
            return (scene.dynamic_solidify_modifiers_4, scene.dynamic_solidify_modifiers_select_index_4)
        elif index == 5 :
            return (scene.dynamic_solidify_modifiers_5, scene.dynamic_solidify_modifiers_select_index_5)
        elif index == 6 :
            return (scene.dynamic_solidify_modifiers_6, scene.dynamic_solidify_modifiers_select_index_6)
        elif index == 7 :
            return (scene.dynamic_solidify_modifiers_7, scene.dynamic_solidify_modifiers_select_index_7)
        elif index == 8 :
            return (scene.dynamic_solidify_modifiers_8, scene.dynamic_solidify_modifiers_select_index_8)
        elif index == 9 :
            return (scene.dynamic_solidify_modifiers_9, scene.dynamic_solidify_modifiers_select_index_9)

    @classmethod
    def setModifiersSelectIndex(self, scene, index, modifiers_select_index) :
        if index > 10 :
            pass
        elif index == 0 :
            scene.dynamic_solidify_modifiers_select_index_0 = modifiers_select_index
        elif index == 1 :
            scene.dynamic_solidify_modifiers_select_index_1 = modifiers_select_index
        elif index == 2 :
            scene.dynamic_solidify_modifiers_select_index_2 = modifiers_select_index
        elif index == 3 :
            scene.dynamic_solidify_modifiers_select_index_3 = modifiers_select_index
        elif index == 4 :
            scene.dynamic_solidify_modifiers_select_index_4 = modifiers_select_index
        elif index == 5 :
            scene.dynamic_solidify_modifiers_select_index_5 = modifiers_select_index
        elif index == 6 :
            scene.dynamic_solidify_modifiers_select_index_6 = modifiers_select_index
        elif index == 7 :
            scene.dynamic_solidify_modifiers_select_index_7 = modifiers_select_index
        elif index == 8 :
            scene.dynamic_solidify_modifiers_select_index_8 = modifiers_select_index
        elif index == 9 :
            scene.dynamic_solidify_modifiers_select_index_9 = modifiers_select_index

    @classmethod
    def getNoContextModifiers(self, index) :
        return self.getModifiers(bpy.context.scene, index)

    @classmethod
    def resetModifiers(self, scene, index) :
        modifiers , modifiers_select_index = self.getModifiers(scene, index)
        if modifiers is None :
            return
        for modifier in modifiers:
            index = len(modifiers) - 1
            modifiers.remove(index)
        self.setModifiersSelectIndex(scene, index, -1)

    @classmethod
    def register(self):
        bpy.utils.register_class(DynamicSolidifyModifiersPropertyGroup)
        bpy.utils.register_class(DynamicSolidify_UL_Modifiers)
        bpy.types.Scene.dynamic_solidify_modifiers_0 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_1 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_2 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_3 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_4 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_5 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_6 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_7 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_8 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_9 = CollectionProperty(type = DynamicSolidifyModifiersPropertyGroup)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_0 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_1 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_2 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_3 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_4 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_5 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_6 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_7 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_8 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)
        bpy.types.Scene.dynamic_solidify_modifiers_select_index_9 = IntProperty(name = "dynamic_solidify_modifiers_select_index", default = -1)

    @classmethod
    def unregister(self):
        bpy.utils.unregister_class(DynamicSolidifyModifiersPropertyGroup)
        bpy.utils.unregister_class(DynamicSolidify_UL_Modifiers)
        del bpy.types.Scene.dynamic_solidify_modifiers_0
        del bpy.types.Scene.dynamic_solidify_modifiers_1
        del bpy.types.Scene.dynamic_solidify_modifiers_2
        del bpy.types.Scene.dynamic_solidify_modifiers_3
        del bpy.types.Scene.dynamic_solidify_modifiers_4
        del bpy.types.Scene.dynamic_solidify_modifiers_5
        del bpy.types.Scene.dynamic_solidify_modifiers_6
        del bpy.types.Scene.dynamic_solidify_modifiers_7
        del bpy.types.Scene.dynamic_solidify_modifiers_8
        del bpy.types.Scene.dynamic_solidify_modifiers_9
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_0
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_1
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_2
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_3
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_4
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_5
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_6
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_7
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_8
        del bpy.types.Scene.dynamic_solidify_modifiers_select_index_9

class DynamicSolidifyModifiersPropertyGroup(PropertyGroup):
    modifier_name : StringProperty(name = "Modifier")
    modifier_thickness : FloatProperty(name = "Modifier Thickness")

class DynamicSolidify_UL_Modifiers(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align = True)
        row.prop(item, "modifier_name", text = "", emboss = False, icon = 'OBJECT_DATAMODE')
        row.label(text = str(item.modifier_thickness))