#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def generate_ninja_file(output_path, target_size_mb=10):
    header_template = """# Generated build.ninja file for testing
cxx = clang++
cc = clang
ar = ar
cflags = -Wall -Wextra -O2
ldflags = -lpthread

rule cc
  command = $cc $cflags -MMD -MF $out.d -c $in -o $out
  deps = gcc
  depfile = $out.d
  description = CC $out

rule cxx
  command = $cxx $cflags -MMD -MF $out.d -c $in -o $out
  deps = gcc
  depfile = $out.d
  description = CXX $out

rule link
  command = $cxx $ldflags -o $out $in
  description = LINK $out

rule ar
  command = rm -f $out && $ar crs $out $in
  description = AR $out

"""

    target_size = target_size_mb * 1024 * 1024

    with open(output_path, 'w') as f:
        f.write(header_template)
        current_size = len(header_template)

        file_index = -1
        module_index = -1

        while current_size < target_size:
            file_index += 1
            module_index += 1
            module_name = f"module{module_index:04d}"

            for file_type in ['core', 'util', 'test', 'impl']:
                c_file = f"""
build obj/{module_name}/{file_type}{file_index:04d}.o: cc src/{module_name}/{file_type}{file_index:04d}.c
  includes = -I./include -I./src/{module_name}
"""
                cpp_file = f"""
build obj/{module_name}/{file_type}{file_index:04d}.cc.o: cxx src/{module_name}/{file_type}{file_index:04d}.cc
  includes = -I./include -I./src/{module_name}
"""
                f.write(c_file)
                f.write(cpp_file)
                current_size += len(c_file) + len(cpp_file)
            lib_build = f"""
build lib/{module_name}/lib{module_name}.a: ar obj/{module_name}/core{file_index:04d}.o obj/{module_name}/util{file_index:04d}.o obj/{module_name}/impl{file_index:04d}.o
"""
            f.write(lib_build)
            current_size += len(lib_build)
            test_build = f"""
build bin/{module_name}/test_{file_index:04d}: link obj/{module_name}/test{file_index:04d}.o obj/{module_name}/test{file_index:04d}.cc.o lib/{module_name}/lib{module_name}.a
"""
            f.write(test_build)
            current_size += len(test_build)
            phony = f"""
build {module_name}: phony bin/{module_name}/test_{file_index:04d}
"""
            f.write(phony)
            current_size += len(phony)

        default_target = "\ndefault"
        for i in range(module_index + 1):
            default_target += f" module{i:04d}"
        f.write(default_target)
        f.write("\n")

        print(f"Generated build.ninja file at: {output_path}")
        print(f"Final size: {current_size / 1024 / 1024:.2f}MB")
        print(f"Total modules: {module_index + 1}")
        print(f"Files per module: {file_index}")


if __name__ == "__main__":
    import sys
    output_file = "build.ninja" if len(sys.argv) < 2 else sys.argv[1]
    target_mb = 10 if len(sys.argv) < 3 else int(sys.argv[2])
    generate_ninja_file(output_file, target_mb)
