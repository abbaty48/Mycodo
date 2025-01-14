# -*- coding: utf-8 -*-
"""Generate markdown file of Action information to be inserted into the manual."""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, "../../..")))

from collections import OrderedDict
from mycodo.config import INSTALL_DIRECTORY
from mycodo.scripts.generate_doc_output import generate_controller_doc
from mycodo.utils.function_actions import parse_function_action_information

save_path = os.path.join(INSTALL_DIRECTORY, "docs/Supported-Actions.md")

actions_info = OrderedDict()
mycodo_info = OrderedDict()


def repeat_to_length(s, wanted):
    return (s * (wanted//len(s) + 1))[:wanted]


if __name__ == "__main__":
    for action_id, action_data in parse_function_action_information(exclude_custom=True).items():
        name_str = ""
        if 'manufacturer' in action_data and action_data['manufacturer']:
            name_str += "{}".format(action_data['manufacturer'])
        if 'name' in action_data and action_data['name']:
            name_str += ": {}".format(action_data['name'])
        if 'library' in action_data and action_data['library']:
            name_str += ": {}".format(action_data['library'])

        if ('manufacturer' in action_data and
                action_data['manufacturer'] in ['Linux', 'Mycodo', 'Raspberry Pi', 'System']):

            if name_str in mycodo_info and 'dependencies_module' in mycodo_info[name_str]:
                # Multiple sets of dependencies, append library
                mycodo_info[name_str]['dependencies_module'].append(action_data['dependencies_module'])
            else:
                # Only one set of dependencies
                mycodo_info[name_str] = action_data
                if 'dependencies_module' in action_data:
                    mycodo_info[name_str]['dependencies_module'] = [action_data['dependencies_module']]  # turn into list
        else:
            if name_str in actions_info and 'dependencies_module' in actions_info[name_str]:
                # Multiple sets of dependencies, append library
                actions_info[name_str]['dependencies_module'].append(action_data['dependencies_module'])
            else:
                # Only one set of dependencies
                actions_info[name_str] = action_data
                if 'dependencies_module' in action_data:
                    actions_info[name_str]['dependencies_module'] = [action_data['dependencies_module']]  # turn into list

    mycodo_info = dict(OrderedDict(sorted(mycodo_info.items(), key = lambda t: t[0])))
    actions_info = dict(OrderedDict(sorted(actions_info.items(), key = lambda t: t[0])))

    list_actions = [
        (mycodo_info, "Built-In Actions (System)"),
        (actions_info, "Built-In Actions (Devices)")
    ]

    with open(save_path, 'w') as out_file:
        out_file.write("Actions allow certain Functions to influence other parts of Mycodo and the computer system.\n\n")
        out_file.write("Supported Actions are listed below.\n\n")
        for each_list in list_actions:
            if not each_list[0]:
                continue

            out_file.write("## {}\n\n".format(each_list[1]))

            for each_id, each_data in each_list[0].items():
                name_str = ""
                if 'name' in each_data and each_data['name']:
                    name_str += "{}".format(each_data['name'])

                out_file.write("### {}\n\n".format(name_str))

                if 'manufacturer' in each_data and each_data['manufacturer']:
                    out_file.write("- Manufacturer: {}\n".format(each_data['manufacturer']))

                if 'library' in each_data and each_data['library']:
                    out_file.write("- Libraries: {}\n".format(each_data['library']))

                generate_controller_doc(out_file, each_data)
