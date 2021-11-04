import ast
import copy
from typing import Any, Callable
import flyable.code_gen.code_type as code_type
import flyable.code_gen.code_gen as gen
import flyable.data.lang_type as lang_type
import flyable.code_gen.caller as caller
import flyable.parse.op as parse_op
import flyable.code_gen.runtime as runtime
import flyable.code_gen.ref_counter as ref_counter


def bin_op(visitor, op, type_left, value_left, type_right, value_right):
    builder = visitor.get_builder()

    # Check the primitive type conversion
    if type_left.is_dec():  # If left type is decimal, the right type must also be to return a decimal
        if type_right.is_int() or type_right.is_bool():
            type_right = lang_type.get_dec_type()
            value_right = visitor.get_builder().float_cast(
                value_right, type_right.to_code_type(visitor.get_code_gen()))
    elif type_left.is_int():
        if type_right.is_dec():
            type_left = lang_type.get_dec_type()
            value_left = visitor.get_builder().float_cast(
                value_left, type_left.to_code_type(visitor.get_code_gen()))
        elif type_right.is_bool():
            type_right = lang_type.get_bool_type()
            value_right = visitor.get_builder().int_cast(
                value_left, type_right.to_code_type(visitor.get_code_gen()))
    elif type_left.is_bool():
        if type_right.is_dec():
            type_left = lang_type.get_dec_type()
            value_left = visitor.get_builder().float_cast(
                value_left, type_left.to_code_type(visitor.get_code_gen()))
        elif type_right.is_bool():
            type_right = lang_type.get_bool_type()
            value_right = visitor.get_builder().int_cast(
                value_left, type_right.to_code_type(visitor.get_code_gen()))

    if type_left.is_obj() or type_left.is_python_obj() or type_left.is_collection() or type_right.is_obj() or type_right.is_python_obj() or type_right.is_collection():
        args_types = [type_right]
        args = [value_right]
        result = caller.call_obj(visitor, parse_op.get_op_func_call(
            op), value_left, type_left, args, args_types)
        return result

    if isinstance(op, ast.FloorDiv):
        if type_left.is_int() and type_right.is_int():
            result = builder.div(value_left, value_right)
            return lang_type.get_int_type(), result
        elif type_left.is_dec() or type_right.is_dec():
            # cast in case it's not double
            value_right = builder.float_cast(
                value_right, code_type.get_double())
            # cast in case it's not double
            value_left = builder.float_cast(value_left, code_type.get_double())
            result = builder.div(value_left, value_right)
            result = builder.int_cast(result, code_type.get_int64())
            result = builder.float_cast(result, code_type.get_double())
            return lang_type.get_dec_type(), result
        else:
            """Do something"""

    result_type = copy.copy(type_left)
    result_type.clear_hints()  # Since an op is done we remove the constant value hint
    apply_op: Callable[[Any, Any], Any]  # the binary operator we want to apply

    if isinstance(op, ast.Add):
        apply_op = builder.add
    elif isinstance(op, ast.Sub):
        apply_op = builder.sub
    elif isinstance(op, ast.Mult):
        apply_op = builder.mul
    elif isinstance(op, ast.Div):
        apply_op = builder.div
    elif isinstance(op, ast.Mod):
        apply_op = builder.mod
    else:
        raise ValueError("Unsupported Op " + str(op))

    return result_type, apply_op(value_left, value_right)


def cond_op(visitor, op, type_left, first_value, type_right, second_value):
    builder = visitor.get_builder()
    if type_left.is_obj() or type_left.is_python_obj() or type_left.is_collection() or type_right.is_obj() or type_right.is_python_obj() or type_right.is_collection():

        """
        If one of the two values is a python object then both objects need to be a python object
        """

        args_types = [type_right]
        args = [second_value]

        return caller.call_obj(visitor, parse_op.get_op_func_call(op), first_value, type_left, args, args_types)

    # the binary conditionnal operator we want to apply
    apply_op: Callable[[Any, Any], Any]
    if isinstance(op, ast.And):
        apply_op = builder.op_and
    elif isinstance(op, ast.Or):
        apply_op = builder.op_or
    elif isinstance(op, ast.Eq):
        apply_op = builder.eq
    elif isinstance(op, ast.NotEq):
        apply_op = builder.ne
    elif isinstance(op, ast.Lt):
        apply_op = builder.lt
    elif isinstance(op, ast.LtE):
        apply_op = builder.lte
    elif isinstance(op, ast.Gt):
        apply_op = builder.gt
    elif isinstance(op, ast.GtE):
        apply_op = builder.gte
    else:
        raise NotImplementedError("Compare op not supported")

    return lang_type.get_bool_type(), apply_op(first_value, second_value)


def unary_op(visitor, type, value, op):
    if type.is_obj() or type.is_python_obj() or type.is_collection():
        args_types = [type]
        args = [value]
        return caller.call_obj(visitor, parse_op.get_op_func_call(op), value, type, args, args_types)
    if isinstance(op, ast.Not):
        return unary_op_not(visitor, type, value)
    elif isinstance(op, ast.Invert):
        return unary_op_invert(visitor, type, value)
    elif isinstance(op, ast.UAdd):
        return unary_op_uadd(visitor, type, value)
    elif isinstance(op, ast.USub):
        return unary_op_usub(visitor, type, value)


def unary_op_not(visitor, type, value):
    if type.is_obj() or type.is_python_obj() or type.is_collection():
        args_types = [type]
        args = [value]
        return caller.call_obj(visitor, "__not__", value, type, args, args_types)
    
    builder = visitor.get_builder()
    bool_type = lang_type.get_bool_type()
    
    const: Any
    if type.is_int():
        const = builder.const_int64(0)
    elif type.is_dec():
        const = builder.const_float64(0.0)
    elif type.is_bool():
        const = builder.const_int1(0)
    else:
        raise TypeError()
    
    return bool_type, builder.eq(value, const)


def unary_op_invert(visitor, type, value):
    if type.is_obj() or type.is_python_obj() or type.is_collection():
        args_types = [type]
        args = [value]
        return caller.call_obj(visitor, "__not__", value, type, args, args_types)
    elif type.is_int():
        return lang_type.get_int_type(), visitor.get_builder().eq(value, visitor.get_builder().const_int64(0))
    elif type.is_dec():
        return unary_op_invert(visitor, lang_type.get_int_type(),
                               visitor.get_builder().int_cast(value, code_type.get_int64()))
    elif type.is_bool():
        return lang_type.get_int_type(), visitor.get_builder().eq(value, visitor.get_builder().const_int1(0))


def unary_op_uadd(visitor, type, value):
    if type.is_obj() or type.is_python_obj() or type.is_collection():
        args_types = [type]
        args = [value]
        return caller.call_obj(visitor, "__pos__", value, type, args, args_types)
    elif type.is_int():
        abs_args = [code_type.get_int64(), code_type.get_int1()]
        abs_func = visitor.get_code_gen().get_or_create_func("llvm.abs.i64", code_type.get_int64(), abs_args,
                                                             gen.Linkage.EXTERNAL)
        return visitor.get_builder().call(abs_func, [value, visitor.get_builder().const_int1(0)])
    elif type.is_dec():
        abs_args = [code_type.get_double()]
        abs_func = visitor.get_code_gen().get_or_create_func("llvm.fabs.f64", code_type.get_double(), abs_args,
                                                             gen.Linkage.EXTERNAL)
        return visitor.get_builder().call(abs_func, [value])
    elif type.is_bool():
        return lang_type.get_int_type(), visitor.get_builder().eq(value, visitor.get_builder().const_int1(0))


def unary_op_usub(visitor, type, value):
    if type.is_obj() or type.is_python_obj() or type.is_collection():
        args_types = [type]
        args = [value]
        return caller.call_obj(visitor, "__neg__", value, type, args, args_types)
    elif type.is_int():
        abs_args = [code_type.get_int64(), code_type.get_int1()]
        abs_func = visitor.get_code_gen().get_or_create_func("llvm.abs.i64", code_type.get_int64(), abs_args,
                                                             gen.Linkage.EXTERNAL)
        result = visitor.get_builder().call(
            abs_func, [value, visitor.get_builder().const_int1(0)])
        return lang_type.get_int_type(), visitor.get_builder().neg(result)
    elif type.is_dec():
        abs_args = [code_type.get_double()]
        abs_func = visitor.get_code_gen().get_or_create_func("llvm.fabs.f64", code_type.get_double(), abs_args,
                                                             gen.Linkage.EXTERNAL)
        result = visitor.get_builder().call(abs_func, [value])
        return lang_type.get_dec_type(), visitor.get_builder().neg(result)
    elif type.is_bool():
        raise NotImplementedError()
        # return lang_type.get_int_type(), result


def bool_op(visitor, op, left_type, left_value, right_type, right_value):
    if isinstance(op, ast.And):
        return bool_op_and(visitor, left_type, left_value, right_type, right_value)
    elif isinstance(op, ast.Or):
        return bool_op_or(visitor, left_type, left_value, right_type, right_value)
    else:
        raise NotImplementedError(str(op))


def bool_op_and(visitor, left_type, left_value, right_type, right_value):
    if left_type.is_obj() or left_type.is_python_obj() or left_type.is_collection():
        args_types = [right_type]
        args = [right_value]
        return caller.call_obj(visitor, "__and__", left_value, left_type, args, args_types)
    elif left_type.is_primitive():
        return lang_type.get_bool_type(), visitor.get_builder()._and(left_value, right_value)
    elif left_type.is_obj() or left_type.is_python_obj() or left_type.is_list() or left_type.is_dict():
        types = [right_type]
        values = [right_value]
        return caller.call_obj(visitor, "__and__", left_value, left_type, values, types)
    else:
        raise NotImplementedError()


def bool_op_or(visitor, left_type, left_value, right_type, right_value):
    if left_type.is_obj() or left_type.is_python_obj() or left_type.is_collection():
        args_types = [right_type]
        args = [right_value]
        return caller.call_obj(visitor, "__or__", left_value, left_type, args, args_types)
    elif left_type.is_primitive():
        return lang_type.get_bool_type(), visitor.get_builder()._or(left_value, right_value)
    elif left_type.is_obj() or left_type.is_python_obj() or left_type.is_list() or left_type.is_dict():
        types = [right_type]
        values = [right_value]
        return caller.call_obj(visitor, "__or__", left_value, left_type, values, types)
    else:
        raise NotImplementedError()
