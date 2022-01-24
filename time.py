# Copyright Pasindu Sewmuthu 2022. MIT license, see LICENSE file.
import codecs

class WholeSub:
    def __init__(self, h, m, s, ms, in_file, out_file, method):
        self.s = 0
        self.m = 0
        self.h = 0
        
        self.diff_h = h
        self.diff_m = m
        self.diff_s = s
        self.diff_ms = ms
        self.method = method
        self.in_file = codecs.open(str(in_file), 'r', 'UTF-8')
        self.out_file = codecs.open(str(out_file), 'w', 'UTF-8')
    
    def process(self):
        for line in self.in_file.readlines():
            line = line.strip()
            
            if ' --> ' in line:
                t = line.split(' --> ')
                t_f = t[0].split(':')
                t_t = t[1].split(':')
                
                self.cur_frm_h = int(t_f[0])
                self.cur_frm_m = int(t_f[1])
                self.cur_frm_s = int(t_f[2].split(',')[0])
                self.cur_frm_ms = int(t_f[2].split(',')[1])
                
                self.cur_to_h = int(t_t[0])
                self.cur_to_m = int(t_t[1])
                self.cur_to_s = int(t_t[2].split(',')[0])
                self.cur_to_ms = int(t_t[2].split(',')[1])
                
                if self.method == 'add':
                    self.frm_reals = self.add()[0]
                    self.to_reals = self.add()[1]
    
    def add(self):
        rea_frm_h = self.cur_frm_h + self.diff_h
        rea_frm_m = self.cur_frm_m + self.diff_m
        rea_frm_s = self.cur_frm_s + self.diff_s
        rea_frm_ms = self.cur_frm_ms + self.diff_ms
        
        rea_to_m = self.cur_to_m + self.diff_m
        rea_to_h = self.cur_to_h + self.diff_h
        rea_to_s = self.cur_to_s + self.diff_s
        rea_to_ms = self.cur_to_ms + self.diff_ms
        
        if (rea_frm_ms // 1000) > 0:
            self.s = rea_frm_ms // 1000
            rea_frm_ms %= 1000
            rea_frm_s += self.s
        
        if (rea_frm_s // 60) > 0:
            self.m = rea_frm_s // 60
            rea_frm_s %= 60
            rea_frm_m += self.m
        
        if (rea_frm_m // 60) > 0:
            self.h = rea_frm_m // 60
            rea_frm_m %= 60
            rea_frm_h += self.h
        
        if (rea_to_ms // 1000) > 0:
            self.s = rea_to_ms // 1000
            rea_to_ms %= 1000
            rea_to_s += self.s
        
        if (rea_to_s // 60) > 0:
            self.m = rea_to_s // 60
            rea_to_s %= 60
            rea_to_m += self.m
        
        if (rea_to_m // 60) > 0:
            self.h = rea_to_m // 60
            rea_to_m %= 60
            rea_to_h += self.h
        
        reals = [[rea_frm_h, rea_frm_m, rea_frm_s, rea_frm_ms], [rea_to_h, rea_to_m, rea_to_s, rea_to_ms]]
        
        return reals
