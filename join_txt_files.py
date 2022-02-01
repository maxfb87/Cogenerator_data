import os
import glob

def join_txt_files():
    """
    This function joint different .txt files into one file.
    These files must contain the thermal data.
    Folders containing files has to be named as "STC COLL" and "STC CSA"
    """

    folders = ["STC COLL", "STC CSA"] #TODO Make this variables
    base_cwd = os.getcwd()

    for folder in folders:
        path = os.path.join(base_cwd, folder)
        os.chdir(path)

        txt_files = glob.glob("GIORNALIERA*.txt")
        txt_resume_file_name = "resume_thermal_energy" + folder + ".txt"

        file = open(txt_resume_file_name,"w+")
        file.close()

        output_file = open(txt_resume_file_name, "a")

        for file in txt_files:
            print(file)
            input_file = open(file,"r")
            lines = input_file.readlines()
            for line in lines[4:]:
                output_file.writelines(line)
            
        output_file.close()
        input_file.close()
