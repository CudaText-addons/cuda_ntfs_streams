from cudatext import *

try:
    from .pyads import ADS
except:
    ADS = None
    msg_box('NTFS Streams plugin requires Windows', MB_OK+MB_ICONERROR)

class Command:
    def dialog(self):
        if not ADS: return
        fn = ed.get_filename()
        if not fn:
            msg_status('NTFS Streams: need named file')
            return
            
        st = ADS(fn)
        print(st.streams)
        