import threading, time, queue, multiprocessing
from inc import simens_dadm as smns
import uiui as gui
from inc import module_01, module2, module3, module4, module_05, module_06, module08, module_09, module_10, module11, module12
from inc.constants import *

def simens_core(communicator):

    state = 0 # 
    data = [] # list that holds non-upsampled and upsampled data
    current_instance = 0 # 0 for non-upsampled, 1 for upsampled data

    while True:
        #print("Core working")
        x=None
        if not communicator.gui_says.empty():


            x = communicator.gui_says.get()


            if x.module == READ_STR: # Read and reconstruct
                current_instance = 0
                data = []
                communicator.core_says.put('Opening data...')
                data.append(smns.mri_read(x.arguments))
                if isinstance(data[0], smns.mri_struct):
                    communicator.core_says.put('Reconstructing...')
                    data[current_instance] = module_01.run_module(data[current_instance])
                    communicator.core_says.put('Reconstructing done')
                    communicator.core_says.put(smns.simens_msg('data', data[current_instance]))
                else:
                    communicator.core_says.put(READ_ERROR)


            elif x.module == MODULE_2_STR: # Intensity inhomogenity correction
                communicator.core_says.put('Applying intensity inhomogenity correction...')
                data[current_instance] = module2.main2(data[current_instance])
                communicator.core_says.put('Intensity inhomogenity correction applied')
                communicator.core_says.put(smns.simens_msg(MODULE_2_STR, data[current_instance]))


            elif x.module == MODULE_3_STR: # Noise mapping
                communicator.core_says.put('Explicit call for noise map is not supported')


            elif x.module == MODULE_4_STR: # Filtering #1
                communicator.core_says.put('Generating noise maps...')
                data[current_instance] = module3.main3(data[current_instance])
                communicator.core_says.put('Filtering...')
                data[current_instance] = module4.main4(data[current_instance])
                communicator.core_says.put('Filtering done')
                communicator.core_says.put(smns.simens_msg(MODULE_4_STR, data[current_instance]))


            elif x.module == MODULE_5_STR: # Filtering #2
                communicator.core_says.put('Generating noise maps...')
                data[current_instance] = module3.main3(data[current_instance])
                communicator.core_says.put('Filtering...')
                data[current_instance] = module_05.run_module(data[current_instance])
                communicator.core_says.put('Filtering done')
                communicator.core_says.put(smns.simens_msg(MODULE_5_STR, data[current_instance]))


            elif x.module == MODULE_6_STR: # DTI
                #  DODATKOWE ARGUMENTY, GUI NIECHAJ JE OBSŁUŻY
                solver = x.arguments[0]
                fix_method = x.arguments[1]
                communicator.core_says.put('Obtaining DTI biomarkers...')
                try:
                    data[current_instance] = module_06.run_module(mri_diff = data[current_instance], solver = solver, fix_method = fix_method)
                except ValueError:
                    communicator.core_says.put('DTI: Expected MRI_DIFF object instance, received unknown type.')
                else:
                    communicator.core_says.put('DTI complete')
                    communicator.core_says.put(smns.simens_msg(MODULE_6_STR, data[current_instance]))


            elif x.module == MODULE_8_STR: # Skull Stripping
                communicator.core_says.put('Obtaining skull stripping mask...')
                data[current_instance] = module08.main8(data[current_instance])
                communicator.core_says.put('Skull stripping complete')
                communicator.core_says.put(smns.simens_msg(MODULE_8_STR, data[current_instance]))


            elif x.module == MODULE_9_STR: # Segmentation
                communicator.core_says.put('Segmentation running...')
                data[current_instance] = module_09.main9(data[current_instance])
                communicator.core_says.put('Segmentation complete')
                communicator.core_says.put(smns.simens_msg(MODULE_9_STR, data[current_instance]))


            elif x.module == MODULE_10_STR: # Upsampling
                N = x.arguments
                communicator.core_says.put('Upsampling...')
                data.insert(module_10.main10(data[current_instance], N), 1)
                communicator.core_says.put('Upsampling complete')
                current_instance = 1
                communicator.core_says.put(smns.simens_msg(MODULE_10_STR, data[current_instance]))


            elif x.module == MODULE_11_STR: # Brain 3D
                communicator.core_says.put('Brain 3D imaging takes place in GUI!')


            elif x.module == MODULE_12_STR: # Oblique imaging
                communicator.core_says.put('Oblique imaging takes place in GUI!')


            elif x.module == REQUEST_DATA: # Send data to GUI. Useful with skull stripping
                communicator.core_says.put('Sending data with skull...')
                communicator.core_says.put(smns.simens_msg(REQUEST_DATA, data[current_instance]))
                communicator.core_says.put('Done')


            elif x.module == REVERT_UPSAMPLING: # Undo upsampling
                communicator.core_says.put('Falling back to non-upsampled data...')
                current_instance = 0
                if len(data)>1:
                    data.pop()
                communicator.core_says.put(smns.simens_msg(REVERT_UPSAMPLING, data[current_instance]))
                communicator.core_says.put('Done')


            else:
                communicator.core_says.put('Command not recognized!')

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
    