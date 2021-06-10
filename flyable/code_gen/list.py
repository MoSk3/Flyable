"""
Module with routines to handle Python and Flyable list
"""

from flyable.code_gen.code_type import CodeType
import flyable.code_gen.code_type as code_type

def instanciate_pyton_list(code_gen,builder,len):
    new_list_args_types = [code_type.get_int64()]
    new_list_func = code_gen.get_or_create_func("PyList_New", CodeType(CodeType.CodePrimitive.INT8).get_ptr_to(),
                                                new_list_args_types)
    return builder.call(new_list_func,[len])

def python_list_set(code_gen,builder,list,index,item):
    set_item_args_types = [code_type.get_int8_ptr(),code_type.get_int64(),code_type.get_int8_ptr()]
    set_item_func = code_gen.get_or_create_func("PyList_SetItem",code_type.get_int32(),set_item_args_types)
    return builder.call(set_item_func,[list,item,item])