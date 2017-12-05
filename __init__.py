from binaryninja import *

class myNotification(BinaryDataNotification):
    def __init__(self, view):
        self.view = view
        pass
    def data_written(self, view, offset, length):
        pass
    def data_inserted(self, view, offset, length):
        pass
    def data_removed(self, view, offset, length):
        pass
    def function_added(self, view, func):
        pass
    def function_removed(self, view, func):
        pass
    def function_updated(self, view, func):
        process_names(view, func)
        pass
    def data_var_added(self, view, var):
        pass
    def data_var_removed(self, view, var):
        pass
    def data_var_updated(self, view, var):
        pass
    def string_found(self, view, string_type, offset, length):
        pass
    def string_removed(self, view, string_type, offset, length):
        pass
    def type_defined(self, view, name, type):
        pass
    def type_undefined(self, view, name, type):
        pass

wrapper_types = (MediumLevelILOperation.MLIL_ZX, MediumLevelILOperation.MLIL_SX)

def has_acceptable_src(il_instruction):
    src = il_instruction.src
    while src.operation in wrapper_types:
        src = src.src
    return src.operation == MediumLevelILOperation.MLIL_VAR

def get_src_name(il_instruction):
    src = il_instruction.src
    if src.operation == MediumLevelILOperation.MLIL_VAR:
        return src.src.name
    elif src.operation in wrapper_types:
        while src.operation in wrapper_types:
            src = src.src
        return src.src.name

def get_vars(bv, current_function):
    dests = list()
    mlil = current_function.medium_level_il
    for i in current_function.mlil_instructions:
        if len(i.operands) < 2:
            continue
        if not isinstance(i.operands[1], MediumLevelILInstruction):
            continue
        if i.operation != MediumLevelILOperation.MLIL_SET_VAR:
            continue
        if not has_acceptable_src(i):
            continue
        if i.dest not in dests:
            dests.append(i.dest)
            yield i.dest


def process_names(bv, current_function):
    for d in get_vars(bv, current_function):
        defs = current_function.medium_level_il.get_var_definitions(d)
        uses = current_function.medium_level_il.get_var_uses(d)
        if len(defs) == 1:
            definition = list(current_function.mlil_instructions)[defs[0]]
            src_name = get_src_name(definition)
            print "{}, {} should be named {}".format(defs[0], d.name, src_name)
            d.name = src_name
            current_function.create_auto_var(d, d.type, d.name)

def register_stuff(bv):
    notification = myNotification(bv)
    bv.register_notification(notification)

PluginCommand.register("Auto-rename Variables", "", register_stuff)
