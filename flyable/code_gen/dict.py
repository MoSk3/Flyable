import flyable.code_gen.code_type as code_type
import flyable.code_gen.code_gen as gen


def python_dict_new(code_gen, builder):
    func = code_gen.get_or_create_func("PyDict_New", code_type.get_py_obj_ptr(code_gen), [], gen.Linkage.EXTERNAL)
    return builder.call(func, [])


def python_dict_set_item(code_gen, builder, dict, key, value):
    func = code_gen.get_or_create_func("PyDict_SetItem", code_type.get_int32(),
                                       [code_type.get_py_obj_ptr(code_gen)] * 3, gen.Linkage.EXTERNAL)
    return builder.call(func, [dict, key, value])


def python_dict_len(code_gen, builder, dict):
    args_types = [code_type.get_py_obj_ptr(code_gen)]
    func = code_gen.get_or_create_func("PyDict_Size", code_type.get_int64(), args_types, gen.Linkage.EXTERNAL)
    return builder.call(func, [dict])
