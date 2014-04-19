#!/usr/bin/env python
import roslib; roslib.load_manifest('projected_interface_builder')
from projected_interface_builder.projected_interface import ProjectedInterface
from projected_interface_builder.data_structures import PolygonInfo
import rospy
import decoder

from sound_play.libsoundplay import SoundClient

class Numchat(ProjectedInterface):
    def __init__(self, polygon_file):
        super(Numchat, self).__init__(polygon_file)
        self.sound_client = SoundClient()
        self.decoder = decoder.Decoder('/home/lazewatd/dev/numchat/Data/map.txt')
        self.seq = ''
        for box in range(1,10):
            self.register_callback(str(box), self.click)
            self.register_hover_callback(str(box), self.hover)

    def remove_dupes(self, seq):
        last = ''
        fixed = ''
        for el in seq:
            if last != el:
                fixed += el
            last = el
        return fixed

    def click(self, poly):
        if not self.seq:
            self.seq += poly.id
        else:
            clean = self.remove_dupes(self.seq)
            print clean
            words = self.decoder.getWords(clean)
            print words
            self.sound_client.say(words[0])
            self.seq = ''

    def hover(self, poly):
        if poly.id == '1':
            self.seq = ''

        elif self.seq:
            self.seq += poly.id

if __name__ == '__main__':
    import sys
    if len(rospy.myargv()) != 2:
        print 'Usage: projected_letterboard.py interface_file'
        sys.exit(1)

    interface_file = rospy.myargv()[1]
    rospy.init_node('letterboard_interface')
    interf = Numchat(interface_file)
    interf.start()
    rospy.spin()
    interf.maybe_write_changes()