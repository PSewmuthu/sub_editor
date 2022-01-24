# Copyright Pasindu Sewmuthu 2022. MIT license, see LICENSE file.
import codecs

class WholeSub:
    def __init__(self, h, m, s, ms, in_file, out_file, method):
        self.s = 0
        self.m = 0
        self.h = 0
        self.error = 0
        
        self.diff_h = h
        self.diff_m = m
        self.diff_s = s
        self.diff_ms = ms
        self.method = method
        self.in_file = codecs.open(in_file, 'r', 'UTF-8')
        self.out_file = codecs.open(out_file, 'w', 'UTF-8')
        
        self.process()
    
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
                    reals = self.add()
                    
                    self.frm_reals = reals[0]
                    self.to_reals = reals[1]
                elif self.method == 'substract':
                    reals = self.substract()
                    
                    if self.error != 0:
                        break
                    
                    self.frm_reals = reals[0]
                    self.to_reals = reals[1]
                else:
                    print('Method is not correct!')
                    break
                
                self.out_file.write(f"{self.frm_reals[0]}:{self.frm_reals[1]}:{self.frm_reals[2]},{self.frm_reals[3]} --> {self.to_reals[0]}:{self.to_reals[1]}:{self.to_reals[2]},{self.to_reals[3]}\r\n")
            else:
                self.out_file.write(f"{line}\r\n")
    
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
    
    def substract(self):
        if self.cur_frm_ms < self.diff_ms:
            if (self.cur_frm_s == 0) and (self.cur_frm_m == 0) and (self.cur_frm_h == 0):
                print('Cannot substract the amount of time given by you!')
                self.error = 1
            elif (self.cur_frm_s == 0) and (self.cur_frm_m == 0):
                self.cur_frm_h -= 1
                self.cur_frm_m += 59
                self.cur_frm_s += 59
                self.cur_frm_ms += 1000
            elif self.cur_frm_s == 0:
                self.cur_frm_m -= 1
                self.cur_frm_s += 59
                self.cur_frm_ms += 1000
            else:
                self.cur_frm_s -= 1
                self.cur_frm_ms += 1000
        rea_frm_ms = self.cur_frm_ms - self.diff_ms
        
        if self.cur_frm_s < self.diff_s:
            if (self.cur_frm_m == 0) and (self.cur_frm_h == 0):
                print('Cannot substract the amount of time given by you!')
                self.error = 1
            elif self.cur_frm_m == 0:
                self.cur_frm_h -= 1
                self.cur_frm_m += 59
                self.cur_frm_s += 60
            else:
                self.cur_frm_m -= 1
                self.cur_frm_s += 60
        rea_frm_s = self.cur_frm_s - self.diff_s
        
        if self.cur_frm_m < self.diff_m:
            if self.cur_frm_h == 0:
                print('Cannot substract the amount of time given by you!')
                self.error = 1
            else:
                self.cur_frm_h -= 1
                self.cur_frm_m += 60
        rea_frm_m = self.cur_frm_m - self.diff_m
        
        if self.cur_frm_h < self.diff_h:
            print('Cannot substract the amount of time given by you!')
            self.error = 1
        rea_frm_h = self.cur_frm_h - self.diff_h
        
        if self.cur_to_ms < self.diff_ms:
            if (self.cur_to_s == 0) and (self.cur_to_m == 0) and (self.cur_to_h == 0):
                print('Cannot substract the amount of time given by you!')
                self.error = 1
            elif (self.cur_to_s == 0) and (self.cur_to_m == 0):
                self.cur_to_h -= 1
                self.cur_to_m += 59
                self.cur_to_s += 59
                self.cur_to_ms += 1000
            elif self.cur_to_s == 0:
                self.cur_to_m -= 1
                self.cur_to_s += 59
                self.cur_to_ms += 1000
            else:
                self.cur_to_s -= 1
                self.cur_to_ms += 1000
        rea_to_ms = self.cur_to_ms - self.diff_ms
        
        if self.cur_to_s < self.diff_s:
            if (self.cur_to_m == 0) and (self.cur_to_h == 0):
                print('Cannot substract the amount of time given by you!')
                self.error = 1
            elif self.cur_to_m == 0:
                self.cur_to_h -= 1
                self.cur_to_m += 59
                self.cur_to_s += 60
            else:
                self.cur_to_m -= 1
                self.cur_to_s += 60
        rea_to_s = self.cur_to_s - self.diff_s
        
        if self.cur_to_m < self.diff_m:
            if self.cur_to_h == 0:
                print('Cannot substract the amount of time given by you!')
                self.error = 1
            else:
                self.cur_to_h -= 1
                self.cur_to_m += 60
        rea_to_m = self.cur_to_m - self.diff_m
        
        if self.cur_to_h < self.diff_h:
            print('Cannot substract the amount of time given by you!')
            self.error = 1
        rea_to_h = self.cur_to_h - self.diff_h
        
        reals = [[rea_frm_h, rea_frm_m, rea_frm_s, rea_frm_ms], [rea_to_h, rea_to_m, rea_to_s, rea_to_ms]]
        
        return reals
    
    def __del__(self):
        self.in_file.close()
        self.out_file.close()

if __name__ == '__main__':
    method = input('Enter the subtitle time change method: (a for add or s for substract) ')
    time = input('Enter the time you want to add or substract: (as hh:mm:ss,ms) ')
    in_file = input('Enter the subtitle file name and location to change the time line: (ex: /folder/sub.srt) ')
    out_file = input('Enter the changed subtitle file name and location to save: (ex: /folder/out.srt) ')
    
    if method in ('a', 'ad', 'add'):
        method = 'add'
    elif method in ('s', 'su', 'sub', 'subs', 'subst', 'substr', 'substra', 'substrac', 'substract'):
        method = 'substract'
    else:
        print('Method is not correct!')
    
    time = time.split(':')
    sec = time[2].split(',')
    
    WholeSub(time[0], time[1], sec[0], sec[1], in_file, out_file, method)
