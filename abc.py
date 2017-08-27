import os
import subprocess
import glob


def get_filepaths(directory, ext="idl"):
    # Load all file with extension `ext` in `directory`
    file_paths = []
    for file in os.listdir(directory):
        if file == "glue.cpp":
            pass
        if file.endswith(ext):
            file_paths.append(os.path.join(directory, file))  # Add it to the list.
    return file_paths  # Self-explanatory.


def emcc_home():
    """ Find directory containing emcc.
    """
    home = os.environ.get('EMCC_HOME')
    if home is not None:
        return home
    else:
        print "Error: EMCC_HOME is not set"
        return "./"

        
def gen(proj_dir, cfg_name):
    """generate file glue (glue.cpp and glue.js: Call  tools/webidl_binder.py thienanh.idl glue

    :param proj_dir:    absolute path to project
    :param cfg_name:    config name (? - unused)
    :returns:           True if successful
    """
    file_idls = get_filepaths(proj_dir)
    binder = os.path.join(emcc_home(), "tools/webidl_binder.py")
    # It seems that webidl_binder only receive 1 idl file, not a list of all 
    # idl file, need to double-check.
    cmd = 'python {} {} glue'.format(binder, ' '.join(file_idls))
    
    print cmd
    
    #Call to run cmd to create glue file
    #p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    
    #Create wrapper file, include all .h file in directory and include glue.cpp
    proj_name = os.path.basename(os.path.abspath(proj_dir))
    wrapper_file = os.path.join(proj_dir, proj_name + "_wrapper.cpp")
    
    print "Generating {}...".format(wrapper_file)
    
    with open(wrapper_file, "w") as f:
        for header in get_filepaths(proj_dir, "h"):
            f.write('#include "{}"\n'.format(os.path.basename(header)))
        f.write('#include "glue.cpp"\n')

    # call build (?)
    build(proj_dir, proj_name, get_filepaths(proj_dir, "cpp"))

    return True


def build(proj_dir, proj_name, cpp_files):
    """ Call: emcc thienanh.cpp thienanh_wapper.cpp --post-js glue.js -o thienanh.js
    """
    
    emcc = os.path.join(emcc_home(), "emcc")
    
    # No need for wrapper file as it is already included in cpp_files
    cmd = "{} {} --post-js glue.js -o {}".format(
        emcc,
        " ".join(cpp_files),
        os.path.join(proj_dir, proj_name + '.js'))
    
    print cmd
    # run cmd

    return True


# for testing    
if __name__ == "__main__":
    gen("../../hellohmt", "")

