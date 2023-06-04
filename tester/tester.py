import os

test_folder_path = "./tests"
result_folder_path = "./results"
command = "python3 bimaru.py < " + test_folder_path + "/"

test_folder = os.listdir(test_folder_path)
in_files = []

for file in test_folder:
    if file.endswith(".txt"):
        in_files.append(file)

in_files.sort()

for in_file in in_files:
    os.system(command + in_file + " > " + result_folder_path + "/" + in_file[:-4] + ".myout")
    os.system("diff " + result_folder_path + "/" + in_file[:-4] + ".myout " + test_folder_path + "/" + in_file[:-4] + ".out")