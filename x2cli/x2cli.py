#!/usr/bin/python3

import argparse
import os
from importlib.resources import files
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, PackageLoader


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('project_name', help='The project name.', type=str)

    args = parser.parse_args()

    file_loader = PackageLoader('x2cli', 'templates')
    env = Environment(loader=file_loader)

    project_name = args.project_name + 'cli'

    output_path = os.path.join(os.getcwd(), project_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for template_name in env.list_templates():
        template = env.get_template(template_name)
        render = template.render({'cli_root': args.project_name})

        template_path = Path(
            template_name.removeprefix('x2cli/').replace('x2cli', project_name)
        )

        template_output_path = output_path / template_path.parent

        if not os.path.exists(template_output_path):
            os.makedirs(template_output_path)

        with open(template_output_path / template_path.stem, 'w') as f:
            f.write(render)


if __name__ == '__main__':
    main()
