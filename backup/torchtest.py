import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
print(torch.version.cuda)
print(torch.__version__)
print(torch.cuda.is_available())


#appium --allow-insecure adb_shell
#emulator -avd Pixel_8_Pro_NoWin -no-window -no-boot-anim -no-snapshot