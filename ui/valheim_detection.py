import psutil
from typing import Optional


def is_valheim_running() -> bool:
    try:
        # Get all running processes
        processes = psutil.process_iter(['pid', 'name', 'exe'])
        
        for proc in processes:
            try:
                # check procs for valheim
                proc_name = proc.info['name'].lower()
                if 'valheim' in proc_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return False
    except Exception as e:
        print(f"Error checking for Valheim process: {e}")
        return False


def get_valheim_process_info() -> Optional[dict]:
    try:
        processes = psutil.process_iter(['pid', 'name', 'exe', 'cmdline'])
        
        for proc in processes:
            try:
                proc_name = proc.info['name'].lower()
                if 'valheim' in proc_name:
                    return {
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'exe': proc.info['exe'],
                        'cmdline': proc.info['cmdline']
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return None
    except Exception as e:
        print(f"Error getting Valheim process info: {e}")
        return None


def valheim_warning_message() -> str:
    info = get_valheim_process_info()
    
    if info:
        return (
            f"WARNING: Valheim is currently running!\n\n"
            f"Process Name: {info['name']}\n"
            f"Process ID: {info['pid']}\n"
            f"Executable: {info['exe']}\n\n"
            f"Please close Valheim before using this editor to avoid potential conflicts."
        )
    else:
        return "Valheim is not currently running."
