import os 
import psutil
import time
import pickle
class Process():
    def __init__(self, name="", path="", time_running = 0, actual_process_object = None):
        self.name = name
        self.path= path
        self.time_running = time_running


def remove_repeat_processes(processes):
  proper_processes = []
  proper_process_names = []
  for index, process in enumerate(processes):
    try:
      if not(process.name() in proper_process_names):
        proper_processes.append(process)
        proper_process_names.append(process.name())
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

  return proper_processes


def get_all_running_processes():
    process_list = []
    removed_process_list = remove_repeat_processes(psutil.process_iter())
    for process in removed_process_list:
        try:
            name = process.name()
            path = process.exe()
            process_list.append(Process(name, path, actual_process_object=process))

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return process_list


def get_all_running_process_paths():
    path_list = []
    process_list = remove_repeat_processes(psutil.process_iter())
    for process in process_list:
        try:
            path_list.append(process.exe())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return path_list


def get_process_paths(process_list):
    path_list = []
    for process in (process_list):
        try:
            path_list.append(process.exe())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return path_list
    

def add_processes(old_processes : list, old_process_paths : list, time_incriment : float or int = 5):
    process_paths = get_all_running_process_paths()
    new_processes = get_all_running_processes()
    for index, process_path in enumerate(process_paths):
        if process_path in old_process_paths:
            old_processes[old_process_paths.index(process_path)].time_running += round(time_incriment)
        else:
            old_processes.append(new_processes[index])
            old_process_paths.append(process_paths[index])
    return old_processes, old_process_paths


def get_all_process_times(processes):
  process_times = []
  for process in processes:
    process_times.append(process.time_running)
  return process_times


def test():
  running_processes = get_all_running_processes()
  running_process_paths = get_all_running_process_paths()
  for position, process in enumerate(add_processes(running_processes, get_process_paths(running_process_paths))):
    print(f"object : {process} \nname : {process.name}\npath : {process.path}\ntime running : {process.time_running}\nposition : {position}\n{'-'*10}")


def dump(process_list, process_path_list):
  with open("process_data.dat", "wb+") as file:
    pickle.dump(process_list, file)
  with open("process_list_data.dat", "wb+") as file:
    pickle.dump(process_path_list, file)
    
    
def load():
  with open("process_data.dat", "rb") as file:
    process_data = pickle.load(file)
  with open("process_list_data.dat", "rb") as file:
    process_list_data = pickle.load(file)  
  return process_data, process_list_data


def initiate():
  current_directory = os.listdir()
  if not ("process_data.dat" in current_directory and "process_list_data.dat" in current_directory):
    current_processes = get_all_running_processes()
    current_process_paths = get_all_running_process_paths()
    dump(current_processes, current_process_paths)


def dump_readable(text):
  with open("data.txt", "w+") as data:
    data.write(text)


def main():
  initiate()
  initial_process_list, initial_process_path_list = load()
  start = time.time()
  end = time.time()
  read_string = ''
  while 1:
    for i in range(10):
      start2 = time.time()
      time.sleep(0)
      initial_process_list, initial_process_path_list = add_processes(initial_process_list, initial_process_path_list, time_incriment=(end - start))
      read_string = []
      for process in initial_process_list:
        read_string.append(f'name : {process.name}\nTime running : {process.time_running}\npath : {process.path}\n{"-"*10}\n')
        time.sleep(.05)
      dump_readable("".join(read_string))
      start = end
      end = time.time()
      print(f"Total time : {time.time() - start2}")
      dump(initial_process_list, initial_process_path_list)

if __name__ == "__main__":
  main()
