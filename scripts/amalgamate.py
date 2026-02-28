import os
import re
import argparse

def process_file(filepath, out_f, included_files, include_dirs, system_includes):
    """Recursively process a file, replacing #include with file contents."""
    if not os.path.exists(filepath):
        print(f"Warning: File not found {filepath}")
        return

    # To avoid cyclic inclusion
    if os.path.abspath(filepath) in included_files:
        return
    included_files.add(os.path.abspath(filepath))

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Skip #pragma once
            if re.match(r'^\s*#pragma\s+once\b', line):
                continue

            # Match #include <...>
            sys_match = re.match(r'^\s*#include\s+<([^>]+)>', line)
            if sys_match:
                system_includes.add(sys_match.group(1))
                continue

            # Match #include "..."
            match = re.match(r'^\s*#include\s+"([^"]+)"', line)
            if match:
                inc_file = match.group(1)
                found = False
                for d in include_dirs:
                    full_path = os.path.join(d, inc_file)
                    if os.path.exists(full_path):
                        out_f.write(f"// --- Begin {inc_file} ---\n")
                        process_file(full_path, out_f, included_files, include_dirs, system_includes)
                        out_f.write(f"// --- End {inc_file} ---\n")
                        found = True
                        break
                if not found:
                    print(f"Warning: Included file not found {inc_file} (searched in {include_dirs})")
                    # Keep original include if not found locally
                    out_f.write(line)
            else:
                out_f.write(line)

def main():
    parser = argparse.ArgumentParser(description="Amalgamate C++ sources into single files.")
    parser.add_argument("--h_out", required=True, help="Output single header file")
    parser.add_argument("--cpp_out", required=True, help="Output single cpp file")
    parser.add_argument("--h_src", nargs='*', default=[], help="Input header files")
    parser.add_argument("--cpp_src", nargs='*', default=[], help="Input cpp files")
    parser.add_argument("--include_dirs", nargs='*', default=[], help="Include directories")

    args = parser.parse_args()

    # Create output directories if they don't exist
    os.makedirs(os.path.dirname(args.h_out), exist_ok=True)
    os.makedirs(os.path.dirname(args.cpp_out), exist_ok=True)

    # Make include_dirs absolute
    include_dirs = [os.path.abspath(d) for d in args.include_dirs]

    # First, collect all contents and system includes
    h_content = []
    cpp_content = []
    h_system_includes = set()
    cpp_system_includes = set()

    # Amalgamate headers
    # Use a temporary file to capture content without system includes at the top
    temp_h_path = args.h_out + ".tmp"
    with open(temp_h_path, 'w', encoding='utf-8') as out_f:
        included_files = set()
        for f in args.h_src:
            process_file(os.path.abspath(f), out_f, included_files, include_dirs, h_system_includes)

    # Read back the temporary header content
    with open(temp_h_path, 'r', encoding='utf-8') as f:
        h_content = f.read()
    os.remove(temp_h_path)

    # Write final amalgamated header
    with open(args.h_out, 'w', encoding='utf-8') as out_f:
        out_f.write("// Amalgamated Header File\n")
        out_f.write("#pragma once\n\n")

        # Write sorted system includes
        for sys_inc in sorted(h_system_includes):
            out_f.write(f"#include <{sys_inc}>\n")
        if h_system_includes:
            out_f.write("\n")

        out_f.write(h_content)

    # Amalgamate cpp
    temp_cpp_path = args.cpp_out + ".tmp"
    with open(temp_cpp_path, 'w', encoding='utf-8') as out_f:
        included_files = set()
        # Prevent re-including headers already in the amalgamated header
        for f in args.h_src:
             included_files.add(os.path.abspath(f))

        for f in args.cpp_src:
            process_file(os.path.abspath(f), out_f, included_files, include_dirs, cpp_system_includes)

    # Read back the temporary cpp content
    with open(temp_cpp_path, 'r', encoding='utf-8') as f:
        cpp_content = f.read()
    os.remove(temp_cpp_path)

    # Write final amalgamated cpp
    with open(args.cpp_out, 'w', encoding='utf-8') as out_f:
        out_f.write("// Amalgamated CPP File\n")

        # Write sorted system includes
        # We don't need to write system includes that are already in the header
        unique_cpp_system_includes = cpp_system_includes - h_system_includes
        for sys_inc in sorted(unique_cpp_system_includes):
            out_f.write(f"#include <{sys_inc}>\n")
        if unique_cpp_system_includes:
            out_f.write("\n")

        # Include the amalgamated header
        h_out_name = os.path.basename(args.h_out)
        out_f.write(f'#include "{h_out_name}"\n\n')

        out_f.write(cpp_content)

    print(f"Amalgamation complete:\n  Header: {args.h_out}\n  Source: {args.cpp_out}")

if __name__ == "__main__":
    main()
