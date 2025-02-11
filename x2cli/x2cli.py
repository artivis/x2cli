#!/usr/bin/python3

import argparse
import os
from datetime import date
from pathlib import Path

from jinja2 import Environment, PackageLoader


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('project_name', help='The project name.', type=str)
    parser.add_argument(
        '-o',
        '--output-dir',
        default=os.getcwd(),
        help='The output directory for the project. Default to current path.',
    )
    parser.add_argument(
        '--no-suffix',
        action='store_true',
        help="Do not add the 'cli' suffix to the project name."
    )
    parser.add_argument(
        '-c',
        '--command',
        nargs='+',
        default=[],
        help="A list of commands to bootstrap. "
        "To create a verb, append it to its corresponding command separated by semicolon. "
        "E.g. 'file:list' creates the 'file' command and it associated 'list' verb."
    )

    return parser.parse_args()


def command_to_dict(commands):
    result_dict = {}

    for command in commands:
        key, value = command.split(':', 1) if ':' in command else (command, None)

        values = value.split(',') if value else []

        if key not in result_dict:
            result_dict[key] = values
        else:
            result_dict[key].extend(values)

    return result_dict


def write_file(path, content):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(content)


def ensure_newline(s):
    if s and not s.endswith("\n"):
        return s + "\n"
    return s


def main():
    args = get_args()

    cli_command = args.project_name
    project_name = args.project_name
    if not args.no_suffix:
        project_name += 'cli'

    output_path = os.path.join(args.output_dir, project_name)

    # if os.path.exists(output_path):
    #     raise ValueError(f"Output directory '{output_path}' already exists.")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_loader = PackageLoader('x2cli', Path('templates') / 'x2cli')
    env = Environment(loader=file_loader)

    year = str(date.today().year)
    command_dict = command_to_dict(args.command)

    for template_name in env.list_templates():
        template = env.get_template(template_name)
        render = template.render(
            {
                'cli_command': cli_command,
                'commands': command_dict,
                'project_name': project_name,
                'year': year,
            }
        )

        template_path = Path(template_name.replace('x2cli', project_name))

        template_output_path = output_path / template_path.parent

        if not os.path.exists(template_output_path):
            os.makedirs(template_output_path)

        render = ensure_newline(render)
        write_file(template_output_path / template_path.stem, render)

    file_loader = PackageLoader('x2cli', Path('templates') / 'command')
    env = Environment(loader=file_loader)

    # command_dict = command_to_dict(args.command)

    command_init_render = env.get_template('command__init__.py.j2').render({'year': year})
    command_init_render = ensure_newline(command_init_render)
    verb_init_render = env.get_template('verb__init__.py.j2').render({'project_name': project_name, 'year': year})
    verb_init_render = ensure_newline(verb_init_render)
    command_template = env.get_template('command.py.j2')
    verb_template = env.get_template('verb.py.j2')
    for command, verbs in command_dict.items():
        render = command_template.render(
            {
                'project_name': project_name,
                'cli_command': cli_command,
                'command': command,
                'year': year,
            }
        )

        command_file = f'{command}.py'
        command_output_path = os.path.join(
            output_path, 'src', f'{cli_command}{command}', 'command'
        )
        command_output_file = os.path.join(command_output_path, command_file)

        if not os.path.exists(command_output_path):
            os.makedirs(command_output_path)

        render = ensure_newline(render)
        write_file(command_output_file, render)

        write_file(os.path.join(command_output_path, '__init__.py'), command_init_render)

        for verb in verbs:
            verb_file = f'{verb}.py'
            verb_output_path = os.path.join(
                output_path, 'src', f'{cli_command}{command}', 'verb'
            )
            verb_output_file = os.path.join(verb_output_path, verb_file)

            if not os.path.exists(verb_output_path):
                os.makedirs(verb_output_path)

            write_file(os.path.join(verb_output_path, '__init__.py'), verb_init_render)

            render = verb_template.render(
                {
                    'project_name': project_name,
                    'cli_command': cli_command,
                    'verb': verb,
                    'year': year,
                }
            )

            render = ensure_newline(render)
            write_file(verb_output_file, render)


if __name__ == '__main__':
    main()
