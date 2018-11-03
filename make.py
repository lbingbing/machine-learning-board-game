import os
import stat
import datetime
import subprocess

def chdir():
    dir_path = os.path.dirname(__file__)
    if dir_path:
        os.chdir(dir_path)

def mkdir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

def get_mtime(file_path):
    return os.stat(file_path)[stat.ST_MTIME]

def is_recompile_needed(src_file_path, obj_file_path):
    if not os.path.isfile(obj_file_path):
        return True
    obj_mtime = get_mtime(obj_file_path)
    res = subprocess.run(['g++',  '-MM', src_file_path], stdout = subprocess.PIPE, check = True, encoding = 'utf-8')
    dep_file_names = res.stdout.strip().split()
    assert(dep_file_names[0].rstrip(':')==os.path.basename(obj_file_path))
    del dep_file_names[0]
    assert(dep_file_names[0]==src_file_path)
    for dep_file_name in dep_file_names:
        if obj_mtime <= get_mtime(dep_file_name):
            return True
    return False

def build(flags, src_file_paths, obj_file_paths, executable_file_path):
    relink_needed = False
    for src_file_path, obj_file_path in zip(src_file_paths, obj_file_paths):
        if is_recompile_needed(src_file_path, obj_file_path):
            print('compiling {0} ...'.format(obj_file_path))
            res = subprocess.run(['g++'] + flags + ['-c', src_file_path, '-o', obj_file_path], check = True)
            relink_needed = True
        else:
            print('up-to-date {0} ...'.format(obj_file_path))
    if not os.path.isfile(executable_file_path) or relink_needed:
        print('linking {0} ...'.format(executable_file_path))
        res = subprocess.run(['g++'] + list(map(str, obj_file_paths)) + ['-o', executable_file_path], check = True)
    else:
        print('up-to-date {0} ...'.format(executable_file_path))

def clean():
    for dir_path in ('debug', 'release'):
        if os.path.isdir(dir_path):
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                print('deleting {0} ...'.format(file_path))
                assert(file_path.endswith(('.o', '.exe')))
                os.remove(file_path)
            os.rmdir(dir_path)

if __name__ in '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices = ['debug', 'release', 'clean'], help='make mode')
    args = parser.parse_args()

    chdir()
    assert(os.path.isfile('make.py'))

    if args.mode == 'clean':
        clean()
    else:
        mkdir(args.mode)
        with open('make.ini') as f:
            targets = json.load(f)
        try:
            print('== build {0} =='.format(args.mode))
            for target in targets:
                src_file_names = target['srcs']
                executable_file_name = target['executable']
                assert(all(src_file_name.endswith('.cpp') for src_file_name in src_file_names))
                assert(executable_file_name.endswith('.exe'))

                flags = ['-g'] if args.mode == 'debug' else ['-O2', '-DNDEBUG']
                print('{0}:'.format(executable_file_name))
                src_file_paths = src_file_names
                obj_file_paths = [os.path.join(args.mode, src_file_name.replace('.cpp', '.o')) for src_file_name in src_file_names]
                executable_file_path = os.path.join(args.mode, executable_file_name)
                build(flags, src_file_paths, obj_file_paths, executable_file_path)
        except subprocess.SubprocessError as e:
            pass

