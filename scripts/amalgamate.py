import os
import re
import argparse

def process_file(filepath, out_f, included_files, include_dirs):
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
            # Match #include "..."
            match = re.match(r'^\s*#include\s+"([^"]+)"', line)
            if match:
                inc_file = match.group(1)
                found = False
                for d in include_dirs:
                    full_path = os.path.join(d, inc_file)
                    if os.path.exists(full_path):
                        out_f.write(f"// --- Begin {inc_file} ---\n")
                        process_file(full_path, out_f, included_files, include_dirs)
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
    parser.add_argument("--h_src", required=True, nargs='+', help="Input header files")
    parser.add_argument("--cpp_src", required=True, nargs='+', help="Input cpp files")
    parser.add_argument("--include_dirs", required=True, nargs='+', help="Include directories")

    args = parser.parse_args()

    # Create output directories if they don't exist
    os.makedirs(os.path.dirname(args.h_out), exist_ok=True)
    os.makedirs(os.path.dirname(args.cpp_out), exist_ok=True)

    # Make include_dirs absolute
    include_dirs = [os.path.abspath(d) for d in args.include_dirs]

    # Amalgamate headers
    with open(args.h_out, 'w', encoding='utf-8') as out_f:
        out_f.write("// Amalgamated Header File\n")
        out_f.write("#pragma once\n\n")
        included_files = set()
        for f in args.h_src:
            process_file(os.path.abspath(f), out_f, included_files, include_dirs)

    # Amalgamate cpp
    with open(args.cpp_out, 'w', encoding='utf-8') as out_f:
        out_f.write("// Amalgamated CPP File\n")
        # Include the amalgamated header
        h_out_name = os.path.basename(args.h_out)
        out_f.write(f'#include "{h_out_name}"\n\n')

        included_files = set()
        # Prevent re-including headers already in the amalgamated header
        for f in args.h_src:
             included_files.add(os.path.abspath(f))

        for f in args.cpp_src:
            process_file(os.path.abspath(f), out_f, included_files, include_dirs)

    print(f"Amalgamation complete:\n  Header: {args.h_out}\n  Source: {args.cpp_out}")

if __name__ == "__main__":
    main()
