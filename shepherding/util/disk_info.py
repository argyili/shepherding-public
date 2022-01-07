import os
import shutil

'''
Warning about disk size and usage
'''

def get_dir_size(path='.'):
    '''
    Return recursive directory size
    '''
    if not os.path.exists(path):
        print('%s: No such file or directory: %s' % path)
        return 0

    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += get_dir_size(entry.path)
    except FileNotFoundError as e:
        print(e)
    finally:
        return total

def warn_directory_size(path, limit_gb=100):
    '''
    Warning when directory size is large
    '''
    dir_size = get_dir_size(path)
    limit = limit_gb *1000 *1000 *1000
    if dir_size > limit:
        dir_size = dir_size /1024 /1024 /1024
        print("Warning: {} is {:.0f}GB".format(path, dir_size))
    else:
        pass

def warn_disk_usage(mount_point='/', limit_percentage=90):
    '''
    Warning when directory size percentage is large
    '''
    total, used, available = shutil.disk_usage(mount_point)
    use_parcentage = used/total * 100
    if use_parcentage > limit_percentage:
        print("Warning: use percent of mount point \"{}\" is {:.2f}%".format(mount_point, use_parcentage))
    else:
        pass
