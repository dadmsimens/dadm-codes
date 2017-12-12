#this is an example test which shjould not be taken seriously
import inc.modules.module_example as module0
import inc.simens_dadm as smns
struct = smns.mri_read('dane/T1_synthetic_normal_1mm_L8_r2')
result1, result2 = module0.mymodulefunction(struct)
print("Results:", result1, result2)