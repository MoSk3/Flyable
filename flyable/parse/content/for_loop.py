import ast
import flyable.code_gen.ref_counter as ref_counter
import flyable.code_gen.caller as caller
import flyable.data.type_hint as hint
import flyable.code_gen.exception as excp
import flyable.code_gen.code_type as code_type
import flyable.data.lang_type as lang_type
import flyable.code_gen.caller as caller


def parse_for_loop(node, visitor):
    code_gen = visitor.get_code_gen()
    builder = visitor.get_builder()

    object_to_iter_on = node.iter

    if __for_node_matches_range_opt(object_to_iter_on):
        args_types = []
        args_values = []
        for e in node.iter.args:
            arg_type, arg_value = visitor.visit_node(e)
            args_types.append(arg_type)
            args_values.append(arg_value)

        all_ints = True
        for type in args_types:
            if not type.is_int():
                all_ints = False
        if all_ints and isinstance(node.target, ast.Name):
            __for_loop_with_range_opt(node, visitor, node.target.id, args_types, args_values)
        else:
            # Call the range object from the builtins module
            builtins_module = builder.load(code_gen.get_build_in_module())
            iter_type, iter_value = caller.call_obj(visitor, "range", builtins_module, lang_type.get_python_obj_type(),
                                                    args_values, args_types)
            __for_loop_with_iterators(node, visitor, iter_type, iter_value)
    else:
        iter_type, iter_value = visitor.visit_node(node.iter)
        __for_loop_with_iterators(node, visitor, iter_type, iter_value)


def __for_node_matches_range_opt(iter_node):
    if isinstance(iter_node, ast.Call) and iter_node.func.id == "range":
        args_size = len(iter_node.args)
        if 0 < args_size <= 3:
            return True
    return False


def __for_loop_with_range_opt(node, visitor, var_name, args_types, args_values):
    builder = visitor.get_builder()
    code_gen = visitor.get_code_gen()

    iter_value = visitor.generate_entry_block_var(lang_type.get_int_type().to_code_type(code_gen))
    var_iter_value = visitor.generate_entry_block_var(lang_type.get_int_type().to_code_type(code_gen))

    new_var = visitor.get_func().get_context().add_var(var_name, lang_type.get_int_type())
    new_var.set_code_gen_value(var_iter_value)

    if len(args_types) == 1:
        builder.store(builder.const_int64(0), iter_value)
        var_reach = args_values[0]
        var_incr = builder.const_int64(1)
    elif len(args_types) == 2:
        builder.store(args_values[0], iter_value)
        var_reach = args_values[1]
        var_incr = builder.const_int64(1)
    elif len(args_types) == 3:
        builder.store(args_values[0], iter_value)
        var_reach = args_values[1]
        var_incr = args_values[2]
    else:
        raise Exception("Number of arguments not expected for a for loop with int opt")

    cond_for_block = builder.create_block()
    content_block_for = builder.create_block()
    content_continue_block = builder.create_block()

    builder.br(cond_for_block)

    builder.set_insert_block(cond_for_block)
    can_go_to_content = builder.lt(builder.load(iter_value), var_reach)
    builder.cond_br(can_go_to_content, content_block_for, content_continue_block)

    builder.set_insert_block(content_block_for)
    builder.store(builder.load(iter_value), var_iter_value)
    visitor.visit(node.body)
    builder.store(builder.add(builder.load(iter_value), var_incr), iter_value)  # Increment the iterator
    builder.br(cond_for_block)

    builder.set_insert_block(content_continue_block)


def __for_loop_with_iterators(node, visitor, iter_type, iter_value):
    code_gen = visitor.get_code_gen()
    builder = visitor.get_builder()

    name = node.target.id
    iter_type, iter_value = visitor.visit_node(node.iter)

    if not hint.is_incremented_type(iter_type):
        ref_counter.ref_incr(builder, iter_type, iter_value)

    new_var = visitor.get_func().get_context().add_var(name, iter_type)
    alloca_value = visitor.generate_entry_block_var(iter_type.to_code_type(code_gen))
    new_var.set_code_gen_value(alloca_value)
    iterable_type, iterator = caller.call_obj(visitor, "__iter__", iter_value, iter_type, [], [])

    block_for = builder.create_block()

    builder.br(block_for)
    builder.set_insert_block(block_for)

    next_type, next_value = caller.call_obj(visitor, "__next__", iterator, iterable_type, [], [])

    if not hint.is_incremented_type(next_type):
        ref_counter.ref_incr(builder, next_type, next_value)

    builder.store(next_value, new_var.get_code_gen_value())

    null_ptr = builder.const_null(code_type.get_py_obj_ptr(code_gen))

    test = builder.eq(next_value, null_ptr)

    block_continue = builder.create_block()
    block_for_in = builder.create_block()
    block_else = builder.create_block() if node.orelse is not None else None
    if node.orelse is None:
        builder.cond_br(test, block_continue, block_for_in)
    else:
        builder.cond_br(test, block_else, block_for_in)

    # Setup the for loop content
    builder.set_insert_block(block_for_in)
    visitor.add_out_block(block_continue)  # In case of a break we want to jump after the for loop
    visitor.visit(node.body)
    ref_counter.ref_decr(visitor, next_type, next_value)
    visitor.pop_out_block()

    builder.br(block_for)

    if node.orelse is not None:
        builder.set_insert_block(block_else)
        excp.py_runtime_clear_error(code_gen, builder)
        visitor.visit(node.orelse)
        builder.br(block_continue)

    builder.set_insert_block(block_continue)
    ref_counter.ref_decr(visitor, iter_type, iter_value)
    excp.py_runtime_clear_error(code_gen, builder)
