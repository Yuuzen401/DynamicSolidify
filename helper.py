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
import math

# アクティブなエリアのSpaceView3Dを取得する
def get_space_view_3d():
    aria = bpy.context.area
    for space in aria.spaces:
        if space.type == 'VIEW_3D':
            return space
    else:
        return None

def show_message_info(message):
    def draw(self, context):
        self.layout.label(text = message)
    bpy.context.window_manager.popup_menu(draw, title = "Message", icon = "INFO")

def show_message_error(message):
    def draw(self, context):
        self.layout.label(text = message)
    bpy.context.window_manager.popup_menu(draw, title = 'Error', icon = 'ERROR')

def distance_3d(x1, y1, z1, x2, y2, z2):
    """3次元上での頂点と頂点の距離を求める
    :param Float x1 始点のx
    :param Float y1 始点のy
    :param Float z1 始点のz
    :param Float x2 終点のx
    :param Float y2 終点のy
    :param Float z2 終点のz
    :return Float 距離
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def floor_helper(value, n):
    """独自の切り捨て関数を定義
    :param Float 数値
    :param Int n 切り捨てしたい桁
    """
    return math.floor(value * 10 ** n) / (10 ** n)
    