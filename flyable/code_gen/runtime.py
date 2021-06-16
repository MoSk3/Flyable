from flyable.code_gen.code_type import CodeType
from flyable.code_gen.code_gen import CodeFunc
import flyable.code_gen.code_type as code_type
from flyable.code_gen.code_gen import *

"""
Module to call runtimes functions
"""


def create_unicode(code_gen, builder, str):
    """
    Generate an external call to the python function to create a string
    """
    from_string = code_gen.get_or_create_func("PyUnicode_FromString", CodeType(CodeType.CodePrimitive.INT8).get_ptr_to()
    [CodeType(CodeType.CodePrimitive.INT8).get_ptr_to()])
    return builder.call(from_string, [str])


def malloc_call(code_gen, builder, value_size):
    """
    Generate an external call to the Python runtime memory allocator
    """
    malloc_func = code_gen.get_or_create_func("PyMem_Malloc", CodeType(CodeType.CodePrimitive.INT8).get_ptr_to(),
                                              [CodeType(CodeType.CodePrimitive.INT64)], Linkage.EXTERNAL)
    return builder.call(malloc_func, [value_size])


def py_runtime_get_string(code_gen, builder, value):
    str_ptr = builder.ptr_cast(builder.global_str(value), code_type.get_int8_ptr())
    args_type = [code_type.get_int8_ptr(), code_type.get_int64()]
    new_str_func = code_gen.get_or_create_func("PyUnicode_FromStringAndSize", code_type.get_int8_ptr(), args_type,
                                               Linkage.EXTERNAL)
    return builder.call(new_str_func, [str_ptr, builder.const_int64(len(value))])


def py_runtime_init(code_gen, builder):
    init_func = code_gen.get_or_create_func("Py_Initialize", code_type.get_void(), [], Linkage.EXTERNAL)
    return builder.call(init_func, [])


def py_runtime_object_print(code_gen, builder, obj):
    print_func = code_gen.get_or_create_func("__flyable__print", code_type.get_int32(),
                                             [code_type.get_int8_ptr()], Linkage.EXTERNAL)
    return builder.call(print_func, [obj])


def py_runtime_ImportModule(code_gen, builder, name):
    imp_func = code_gen.get_or_create_func("PyImport_ImportModule",
                                           CodeType(CodeType.CodePrimitive.INT8).get_ptr_to(),
                                           [CodeType(CodeType.CodePrimitive.INT8).get_ptr_to()],
                                           CodeFunc.Linkage.EXTERNAL)
    return builder.call(imp_func, [name_c_str])


def value_to_pyobj(code_gen, builder, value, value_type):
    if value_type.is_int():
        py_func = code_gen.get_or_create_func("PyLong_FromLongLong", code_type.get_int8_ptr(),
                                              [CodeType(CodeType.CodePrimitive.INT64)], Linkage.EXTERNAL)
        return builder.call(py_func, [value])
    elif value_type.is_dec():
        py_func = code_gen.get_or_create_func("PyFloat_FromDouble",
                                              CodeType(CodeType.CodePrimitive.INT8).get_ptr_to()
                                              [CodeType(CodeType.CodePrimitive.DOUBLE)])
        return builder.call(py_func, [value])
    elif value_type.is_bool():
        # TODO : Directly use the global var to avoid the func call
        py_func = code_gen.get_or_create_func("PyBool_FromLong", code_type.get_int8_ptr(), [code_type.get_int1()],
                                              Linkage.EXTERNAL)
        return builder.call(py_func, [value])
    elif value_type.is_obj():
        return value


def py_runtime_obj_len(code_gen, builder, value):
    func_name = "PyObject_Length"
    py_func = code_gen.get_or_create_func(func_name, code_type.get_int64(), [code_type.get_int8_ptr()],
                                          Linkage.EXTERNAL)
    return builder.call(py_func, [value])
