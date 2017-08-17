import os
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

        #handle filename with stream already
        if ':' in os.path.basename(fn):
            n = fn.rfind(':')
            fn = fn[:n]

        st = ADS(fn)

        ITEMS_TOP = [
            'Open stream (%d items)...'% len(st.streams),
            'Add empty stream...', 
            'Add stream from file...', 
            'Delete stream...'
            ]
                
        res = dlg_menu(MENU_LIST, ITEMS_TOP, caption='NTFS Streams')
        if res is None: return
        
        if res==0:
            items = st.streams
            if not items:
                msg_status('No streams')
                return
            res = dlg_menu(MENU_LIST, items)
            if res is None: return
            res = items[res]
            
            file_open(st.full_filename(res))
            
        if res==1:
            res = dlg_input('Stream name:', '')
            if not res: return
            st.add_stream_from_file(None, res)
            msg_status('Stream added: '+res)
            
        if res==2:
            res = dlg_input('Stream name:', '')
            if not res: return
            filename = dlg_file(True, '', '', '')
            if not filename: return
            st.add_stream_from_file(filename, res)
            msg_status('Stream added from file: '+res)

        if res==3:
            if not st.has_streams():
                msg_status('No streams')
                return
            res = dlg_menu(MENU_LIST, st.streams, caption='Delete stream')
            if res is None: return
            res = st.streams[res]
            st.delete_stream(res)
            msg_status('Stream deleted: '+res)
           
