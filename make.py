import os
import stat
import datetime
import subprocess

SOURCE_NODE = 0
OBJECT_NODE = 1

def get_mtime(file_path):
    return os.stat(file_path)[stat.ST_MTIME]

class Node:
    def __init__(self, node_type, dep_nodes, update_fn, not_update_fn, target_file_path):
        self.node_type = node_type
        self.dep_nodes = dep_nodes
        self.update_fn = update_fn
        self.not_update_fn = not_update_fn

        self.target_file_path = target_file_path

    def exists(self):
        return os.path.isfile(self.target_file_path)

    def newer_than(self, node):
        assert(node.exists())
        return get_mtime(self.target_file_path) > get_mtime(node.target_file_path)

    def update(self):
        if self.node_type == SOURCE_NODE:
            return False

        is_update_needed = not self.exists()
        if self.dep_nodes:
            for dep_node in self.dep_nodes:
                updated = dep_node.update()
                is_update_needed = is_update_needed or updated or not self.newer_than(dep_node)

        if is_update_needed:
            if self.update_fn:
                self.update_fn()
            return True
        else:
            if self.not_update_fn:
                self.not_update_fn()
            return False

def get_src_dep_file_paths(src_file_path, include_arguments, obj_file_name):
    res = subprocess.run(['g++',  '-MM', src_file_path] + include_arguments, stdout = subprocess.PIPE, check = True, encoding = 'utf-8')
    dep_file_paths = res.stdout.strip().replace('\\', '').replace('\n', '').split()
    assert(dep_file_paths[0].rstrip(':')==obj_file_name)
    del dep_file_paths[0]
    assert(dep_file_paths[0]==src_file_path)
    return dep_file_paths

def create_compile_obj_fn(obj_file_path, src_file_path, include_arguments, flags):
    def compile_obj_fn():
        print('compiling {0} ...'.format(obj_file_path))
        subprocess.run(['g++'] + flags + ['-c', src_file_path] + include_arguments + ['-o', obj_file_path], check = True)
    return compile_obj_fn

def create_link_executable_fn(executable_file_path, obj_file_paths):
    def link_executable_fn():
        print('linking {0} ...'.format(executable_file_path))
        subprocess.run(['g++'] + obj_file_paths + ['-o', executable_file_path], check = True)
    return link_executable_fn

def create_print_up_to_date_fn(file_path):
    def print_up_to_date_fn():
        print('up-to-date {0} ...'.format(file_path))
    return print_up_to_date_fn

def clean(dst_path):
    for dir_name in ('debug', 'release'):
        dir_path = os.path.join(dst_path, dir_name)
        if os.path.isdir(dir_path):
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                assert(file_path.endswith(('.o', '.exe')))
                print('deleting {0} ...'.format(file_path))
                os.remove(file_path)
            os.rmdir(dir_path)

if __name__ in '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices = ['debug', 'release', 'clean'], help='make mode')
    args = parser.parse_args()

    if args.mode == 'clean':
        print('== clean ==')
    else:
        print('== build {0} =='.format(args.mode))

    dir_path = os.path.dirname(__file__)
    if dir_path:
        os.chdir(dir_path)
    assert(os.path.isfile('make.py'))

    with open('make.ini') as f:
        items = json.load(f)

    try:
        for item in items:
            executable_file_name = item['target']
            dst_path = item['dst_path']
            src_file_paths = item['srcs']
            include_paths = item['include_paths']
            assert(executable_file_name.endswith('.exe'))
            assert(os.path.isdir(dst_path))
            assert(all(e.endswith('.cpp') for e in src_file_paths))
            assert(all(os.path.isdir(e) for e in include_paths))

            if args.mode == 'clean':
                clean(dst_path)
            else:
                print('build {0}:'.format(executable_file_name))

                dst_path = os.path.join(dst_path, args.mode)
                if not os.path.isdir(dst_path):
                    os.mkdir(dst_path)
                executable_file_path = os.path.join(dst_path, executable_file_name)

                include_arguments = ['-I'+e for e in include_paths]
                flags = ['-g'] if args.mode == 'debug' else ['-O2', '-DNDEBUG']

                executable_dep_nodes = []
                obj_file_paths = []
                for src_file_path in src_file_paths:
                    obj_file_name = os.path.basename(src_file_path).replace('.cpp', '.o')
                    obj_file_path = os.path.join(dst_path, obj_file_name)
                    obj_file_paths.append(obj_file_path)
                    obj_dep_file_paths = get_src_dep_file_paths(src_file_path, include_arguments, obj_file_name)
                    obj_dep_nodes = [Node(node_type = SOURCE_NODE, dep_nodes = None, update_fn = None, not_update_fn = None, target_file_path = e) for e in obj_dep_file_paths]
                    obj_node = Node(node_type = OBJECT_NODE, dep_nodes = obj_dep_nodes, update_fn = create_compile_obj_fn(obj_file_path, src_file_path, include_arguments, flags), not_update_fn = create_print_up_to_date_fn(obj_file_path), target_file_path = obj_file_path)
                    executable_dep_nodes.append(obj_node)
                executable_node = Node(node_type = OBJECT_NODE, dep_nodes = executable_dep_nodes, update_fn = create_link_executable_fn(executable_file_path, obj_file_paths), not_update_fn = create_print_up_to_date_fn(executable_file_path), target_file_path = executable_file_path)

                executable_node.update()
    except subprocess.CalledProcessError:
        pass

