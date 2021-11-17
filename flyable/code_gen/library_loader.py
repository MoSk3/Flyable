import os
import platform

"""
Module related to the dynamic loading of the native code generation layer
"""

import ctypes as ctypes


def __load_lib():
    path = dir_path = os.path.dirname(os.path.realpath(__file__))
    lib_path = ""
    if platform.uname()[0] == "Windows":
        path += "\\..\\dyn_lib\\win64"
        lib_path = "FlyableCodeGen.dll"
        os.add_dll_directory(path)
        return ctypes.CDLL(lib_path)
    elif platform.uname()[0] == "Linux":
        lib_name = "libFlyableCodeGen.so"
        path += "/../dyn_lib/linux64/"
        lib_path = path
        return load_lib_and_dependecies(lib_path, lib_name)
    else:
        raise OSError("OS not supported")


def call_code_generation_layer(writer, output):
    lib = __load_lib()
    gen_func = lib.flyable_codegen_run
    buffer_size = len(writer)
    native_buffer = (ctypes.c_char * buffer_size).from_buffer(writer.get_data())
    output_c_str = ctypes.c_char_p(output.encode("utf-8"))
    gen_func(native_buffer, ctypes.c_int32(buffer_size), output_c_str)


def load_lib_and_dependecies(path, lib):
    try:
        return ctypes.CDLL(path + lib)
    except OSError as excp:
        # Get the name of the library not found
        error_msg = excp.args[0]
        # Should crash for any errors that are not missing object file
        # errors, since we can't handle them
        if not "cannot open shared" in error_msg:
            # https://stackoverflow.com/questions/24752395/python-raise-from-usage
            # Helps to avoid a massive error message due to recursive calls
            raise excp from None
        lib_load = error_msg.split(" ")[0]
        lib_load = lib_load[0:-1]
        # Now load it
        load_lib_and_dependecies(path, lib_load)
    # Make sure to still return a value if we handled an exception
    return load_lib_and_dependecies(path, lib)
