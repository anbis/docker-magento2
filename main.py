#!/usr/bin/env python

import os
import ntpath
import subprocess
import shlex


class Utils(object):
    def is_number(self, s):
        if s.find('.') >= 0:
            try:
                return float(s)
            except ValueError:
                return False
        else:
            try:
                return int(s)
            except ValueError:
                return False

    def run(self, command):
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            output = output.decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        rc = process.poll()
        return rc

    def format_print(self, style, text):
        return '\x1b[{0}m{1}\x1b[0m'.format(style, text)


class Choice(Utils):
    """Class to make a choice"""

    def __init__(self, repository=None, child=None):
        self.repository = repository
        self.child = child

        self.selected = None

    def get_selected(self):
        return self.selected

    def get_repository(self):
        return self.repository

    def prepare(self, input_result=None, clear=False):
        self.get_repository().parent = input_result

        if clear:
            self.get_repository().clear()

        if len(self.get_repository().get_objects()) <= 0:
            self.get_repository().prepare()

    def print(self):
        self.get_repository().header()
        self.get_repository().print()
        self.get_repository().help()

    def special_keys(self, choice):
        # Exit
        if choice == 'x':
            return None

        return choice

    def validate(self, choice):
        if choice != '' and 0 < self.is_number(choice) <= self.get_repository().max():
            return True
        else:
            return False

    def pre_execute(self, selected=None):
        os.system('clear')
        print(self.format_print('1;37;44', '  Execute  \n'))
        print(' {} \n'.format(selected))

    def select(self, choice):
        for item in self.get_repository().get_objects().items():
            if item[1].get_index() == self.is_number(choice):
                self.selected = item[1]
                return True

        return False

    def awaiting(self):
        return input(self.format_print('1;5;90', '\nPress [ENTER] to continue...'))

    def process_child(self, result):
        if self.child is not None:
            self.child.process(result)
        else:
            self.awaiting()

    def process(self, input_result=None):
        while True:
            result = None
            self.prepare(input_result=input_result)
            self.print()
            choice = self.input()
            choice = self.special_keys(choice)

            if choice is None:
                return

            if not self.validate(choice):
                continue

            if self.select(choice):
                self.pre_execute(self.get_selected())
                result = self.get_selected().execute()
            else:
                continue

            self.process_child(result)

    def input(self):
        style = '1;37;46'
        return input(self.format_print('1;37;46', '  Please enter:  '))


class ExtendedChoice(Choice):
    """Extended Choice Class"""

    def validate(self, choice):
        if choice.find('.') < 0:
            if choice != '' and 0 < self.is_number(choice) <= self.get_repository().max_group():
                return True
            else:
                return False
        else:
            return Choice.validate(self, choice)

class Base(Utils):
    """Abstract Class"""

    def print(self):
        pass


class AbstractRepository(Base):
    """Abstract Repository Class"""

    objects = {}
    parent = None
    caption = ''
    shortcuts = [
        {'x': 'Exit'}
    ]

    def __repr__(self):
        return self.caption

    def header(self, text=None):
        if text is None:
            text = '  {}  \n'.format(self.caption)

        os.system('clear')
        print(self.format_print('1;37;44', text))

    def help(self):
        text = ''
        text += '\n====================================\n'

        for shortcut in self.shortcuts:
            keys = list(shortcut)
            text += '  {} - {}\n'.format(keys[0], shortcut.get(keys[0]))

        text += '====================================\n'
        print(self.format_print('90', text))

    def clear(self):
        self.objects = {}

    def get_objects(self):
        return self.objects

    def print(self):
        for project in self.get_objects().items():
            project[1].print()

    def add(self, project):
        self.objects[project.get_index()] = project
        return project

    def max(self):
        return list(self.get_objects().items())[-1][1].get_index()

    def prepare(self):
        return self.get_objects()


class AbstractObject(Base):
    """Abstract Object Class"""

    def __init__(self, index, name, parent=None):
        self.index = index
        self.name = name
        self.parent = parent

        self.caption = name

    def __repr__(self):
        style = '32;1'
        return '  {1} - \x1b[{0}m{2}\x1b[0m'.format(style, self.get_index(), self.caption)

    def get_index(self):
        return self.index

    def get_name(self):
        return self.name

    def print(self):
        print(self)

    def execute(self):
        return self


class Project(AbstractObject):
    """Project Class"""

    def __init__(self, index, name, file, parent=None):
        AbstractObject.__init__(self, index, name, parent=parent)

        self.file = file

    def get_file(self):
        return self.file

    def execute(self):
        self.start()
        return AbstractObject.execute(self)

    def start(self):
        os.system('docker-compose -f {} up -d'.format(self.get_file()))

    def stop(self):
        pass

    def recreate(self):
        pass

    def build(self):
        pass


class Container(AbstractObject):
    """Container Class"""


class Command(AbstractObject):
    """Command Class"""

    def __init__(self, index, name, description, parent=None):
        AbstractObject.__init__(self, index, name, parent=parent)

        self.description = description
        self.group = name.split(':', 1)[0]
        self.group_index = None

    def __repr__(self):
        style = '32;1'
        return '  {1} - \x1b[{0}m{2}\x1b[0m {3}'.format(style, self.get_index(), self.caption, self.description)

    def execute(self):
        self.run(
            'docker exec -i {} {} /usr/local/bin/php {} {}'.format(
                self.parent.get_name(), 'su www-data -s', 'bin/magento', self.get_name()
            )
        )
        return AbstractObject.execute(self)


class ProjectRepository(AbstractRepository):
    """Project Repository Class"""

    objects = {}
    parent = None
    caption = 'Projects'

    def get_directory(self):
        """Return workdir path"""
        # return os.getcwd()
        return '/home/andrey/docker'

    def get_yml_files(self, directory, level=0):
        max_level = 2
        all_files = []
        files = os.listdir(path=directory)

        for file in files:
            full_path = os.path.join(directory, file)
            if os.path.isdir(full_path):
                if level >= max_level:
                    return []

                all_files = all_files + self.get_yml_files(full_path, level + 1)
            else:
                if full_path.endswith('docker-compose.yml'):
                    all_files.append(full_path)
                    return all_files

        return all_files

    def prepare(self):
        directory = self.get_directory()
        files = self.get_yml_files(directory)

        for num, file in enumerate(files, start=1):
            yml_path = ntpath.dirname(file)
            name = yml_path.replace(directory, '')
            if name == '':
                name = '/' + ntpath.basename(directory)

            self.add(Project(num, name[1:], file, parent=self.parent))

        return AbstractRepository.prepare(self)


class ContainerRepository(AbstractRepository):
    """Container Repository Class"""

    objects = {}
    parent = None
    caption = 'Containers'
    shortcuts = [
        {'f': 'Force re-create'},
        {'b': 'Build'},
        {'s': 'Stop'},
        {'d': 'Down'},
        {'x': 'Exit'},
    ]

    def prepare(self):
        folder = ntpath.dirname(self.parent.get_file())
        lines = os.popen('cd {} && docker-compose ps'.format(folder)).readlines()
        for num, line in enumerate(lines, start=-1):
            if num <= 0:
                continue

            container = line.split(' ', 1)[0]
            self.add(Container(num, container, parent=self.parent))

        return AbstractRepository.prepare(self)


class CommandRepository(AbstractRepository):
    """Command Repository Class"""

    objects = {}
    parent = None
    caption = 'Commands'
    shortcuts = [
        {'r': 'Reload service'},
        {'p': 'Permission fix'},
        {'h': 'History'},
        {'0': 'Previous command'},
        {'x': 'Exit'},
    ]

    def print(self):
        parent = None
        for item in self.get_objects().items():
            command = item[1]
            if parent != command.group:
                parent = command.group

                style = '33;1'
                print('\x1b[{0}m{1}\x1b[0m'.format(style, parent))

            print(command)

    def max_group(self):
        return list(self.get_objects().items())[-1][1].group_index

    def calculate_keys(self):
        index = 0
        sub = 1
        parent = None
        for item in self.get_objects().items():
            command = item[1]
            if parent != command.group:
                parent = command.group
                sub = 1
                index += 1
            else:
                sub += 1

            command.index = float('{}.{}'.format(index, sub))
            command.group_index = index

    def parse_commands(self):
        lines = os.popen(
            'docker exec -i {} {} /usr/local/bin/php {}'.format(
                self.parent.get_name(), 'su www-data -s', 'bin/magento'
            )).readlines()

        index = 1
        skip = -100
        for num, line in enumerate(lines, start=1):
            line = line.strip()
            if line.find('Available commands:') >= 0 > skip:
                skip = -3

            if skip <= 0:
                skip += 1

                continue
            else:
                parts = line.split(' ', 1)

                if len(parts) < 2:
                    continue

                command = parts[0]
                description = parts[1]
                self.add(Command(index, command, description, parent=self.parent))
                index += 1

    def prepare(self):
        self.parse_commands()
        self.calculate_keys()

        return AbstractRepository.prepare(self)


def main():
    commands = CommandRepository()
    choice_commands = ExtendedChoice(commands)

    containers = ContainerRepository()
    choice_container = Choice(containers, choice_commands)

    projects = ProjectRepository()
    choice_project = Choice(projects, choice_container)
    choice_project.process()


if __name__ == '__main__':
    main()
