from __future__ import print_function, division, absolute_import
import numbers
import collections
import math

import forest

import explorers.envs


defcfg = forest.Tree()
defcfg._describe('xmin',      instanceof=numbers.Real)
defcfg._describe('xmax',      instanceof=numbers.Real)
defcfg._describe('obj_x',     instanceof=numbers.Real)
defcfg._describe('obj_width', instanceof=numbers.Real)
defcfg._describe('obj_y',     instanceof=numbers.Real)
defcfg._freeze(True)


class PushArrayStraightCollides(explorers.envs.Environment):

    defcfg = defcfg

    def __init__(self, cfg):
        self._cfg = cfg
        self._cfg._update(defcfg)
        self._cfg.s_channels = [explorers.envs.Channel('obj_x', (self._cfg.xmin, self._cfg.xmax)),
                                explorers.envs.Channel('obj_y', (0, 100)),
                                explorers.envs.Channel('obj_col', (0, 100))]
        self._cfg.m_channels = [explorers.envs.Channel('x', (self._cfg.xmin, self._cfg.xmax)),
                                explorers.envs.Channel('y', (0, 10)),
                                explorers.envs.Channel('speed', (0, 10))]
        self.m_channels = self._cfg.m_channels
        self.s_channels = self._cfg.s_channels
        self._obj_xmin = self._cfg.obj_x - self._cfg.obj_width/2
        self._obj_xmax = self._cfg.obj_x + self._cfg.obj_width/2

    @property
    def cfg(self):
        return self._cfg

    def execute(self, order):
        if (self._obj_xmin <= order['x'] <= self._obj_xmax and
            self._cfg['obj_y'] <= order['y']): # collision
            obj_x = self._cfg['obj_x']
            obj_y = self._cfg['obj_y'] + order['speed']
            effect = collections.OrderedDict((('obj_x', obj_x), ('obj_y', obj_y), ('obj_col', 100)))
        else:
            effect = collections.OrderedDict((('obj_x', self._cfg.obj_x), ('obj_y', self._cfg.obj_y), ('obj_col', 0)))
        return {'order': order, 'feedback': effect}

    def close(self):
        pass

class PushArrayStraight(PushArrayStraightCollides):

    def __init__(self, cfg):
        super(PushArrayStraight, self).__init__(cfg)
        self._cfg.s_channels = self._cfg.s_channels[:2]
        self.s_channels = self.s_channels[:2]

    def execute(self, order):
        feedback = super(PushArrayStraight, self).execute(order)
        feedback['feedback'].pop('obj_col')
        return feedback

class PushArrayAngle(PushArrayStraight):

    def execute(self, order):
        if (self._obj_xmin <= order['x'] <= self._obj_xmax and
            self._cfg['obj_y'] <= order['y']): # collision
            theta = math.atan2(self._cfg['obj_x'] - order['x'], self._cfg['obj_y'])
            print
            obj_x = self._cfg['obj_x'] + math.sin(theta)*order['speed']
            obj_y = self._cfg['obj_y'] + math.cos(theta)*order['speed']
            effect = collections.OrderedDict((('obj_x', obj_x), ('obj_y', obj_y)))

        else:
            effect = collections.OrderedDict((('obj_x', self._cfg.obj_x), ('obj_y', self._cfg.obj_y)))
        return {'order': order, 'feedback': effect}

    def close(self):
        pass
