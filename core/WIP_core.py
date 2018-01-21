import threading, time, queue, multiprocessing
from inc import simens_dadm as smns
import uiui as gui
from inc import module_01


def simens_core(communicator):

    state = 0;
    

    while True:
        print("Core working")
        x=None
        if not communicator.gui_says.empty():
            x = communicator.gui_says.get()
            if x.module == "read":
                communicator.core_says.put('Opening data...')
                mri_data = smns.mri_read(x.arguments)
                communicator.core_says.put('Reconstructing...')
                mri_data = module_01.run_module(mri_data)
                communicator.core_says.put('Reconstructing done')
                smns.simens_msg('data', mri_data)
        else:
            time.sleep(0.5)




def simri_run(exit_ev):
 
    communicator = smns.simens_communicator(exit_ev)

    core_th = threading.Thread(target=simens_core, args=(communicator,))
    gui_th = threading.Thread(target=gui.launch_gui, args=(communicator,))
    
    core_th.start()
    gui_th.start()

    gui_th.join()
    communicator.exit_event.set()
    core_th.join()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    exit_eve = multiprocessing.Event()
    main_process = multiprocessing.Process(target = simri_run, args = (exit_eve,))
    main_process.start()
    while True:
        if exit_eve.is_set():
            print("Terminating the program main process.")
            main_process.terminate()
            break
        else:
            time.sleep(0.1)
    