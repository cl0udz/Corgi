import subprocess
import re

def batch_demangle(input_file, output_file, batch_size=100):
    batch_class_names = []
    demangled_lines = []
    method_names = []

    with open(input_file, 'r') as input_f:
        for line in input_f:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            parts = line.split()
            if len(parts) >= 2:
                class_name = parts[0][2:]
                method_name = parts[1]
                batch_class_names.append(class_name)
                method_names.append(method_name)

                if len(batch_class_names) >= batch_size:
                    # Execute the 'swift demangle' command for the batch
                    demangled_result = subprocess.check_output(['swift', 'demangle', '--compact'] + batch_class_names, text=True)
                    demangled_lines.extend(demangled_result.split('\n')[:-1])

                    batch_class_names = []

        # Execute any remaining class names
        if batch_class_names:
            demangled_result = subprocess.check_output(['swift', 'demangle', '--compact'] + batch_class_names, text=True)
            demangled_lines.extend(demangled_result.split('\n')[:-1])

    # Write all demangled lines to the output file
    with open(output_file, 'w') as output_f:
        cnt = 0
        try:
            for i, line in enumerate(demangled_lines):
                output_f.write(f"-[{line} {method_names[i]}\n")
                cnt = i
        except(IndexError):
            print("IndexError at " + str(cnt))
    

    return True, f"Demangled results written to {output_file}"

if __name__ == "__main__":
    print(batch_demangle("../class_filter_result/wallet-ios-core_origin_class.txt", "../class_filter_result/wallet-ios-demangled.txt"))