import argparse
import os
import platform
import sys

from misc import activate_venv

if __name__ == '__main__' or True:
    if activate_venv():
        ap = argparse.ArgumentParser()
        ap.add_argument("-c", "--console", action='store_true', help='Start program in CLI mode')
        ap.add_argument('-i', '--in', help='Input file name. Works only with CLI')
        ap.add_argument('-o', '--out', default=None, help='Output folder name. Works only with CLI')
        ap.add_argument('--index', help='Name of index column. Works only with CLI')
        ap.add_argument('--columns', choices=range(1, 4), help='Filter data columns:\n'
                                                               '\t1. All\n'
                                                               '\t2. Intensity\n'
                                                               '\t3. Concentration.\n'
                                                               'Works only with CLI. Not compatible with --regcolumns')
        ap.add_argument('--regcolumns', help='Filter data columns by regexp. Works only with CLI. '
                                             'Not compatible with --columns')
        ap.add_argument('--groupcolumns', nargs='*', help='Create gropus of columns to calculate mean column. '
                                                          'Groups should be separated by " ",'
                                                          ' column names should be separated by ",". '
                                                          'Ex. column1,column2 column2,column3 column4 '
                                                          'creates 3 mean columns. Works only with CLI')
        ap.add_argument('--center', action='store_true', help='Mean center data. Works only with CLI')
        ap.add_argument('--standarize', action='store_true', help='Standarize data. Works only with CLI')
        ap.add_argument('--axis', choices=range(0, 2), help='Axis to compress:\n'
                                                            '\t1. Columns\n'
                                                            '\t0. Rows.\n'
                                                            'Works only with CLI')
        ap.add_argument('--algorithm', choices=['eig', 'svd', 'qrsvd'], help='Choose decomposition algorithm')
        ap.add_argument('--n_components', type=int, help='Number of components to projection')
        ap.add_argument('--plot', action='store_true', help='Plot the PCA data')
        ap.add_argument("-g", "--gui", action='store_true', help='Start program in GUI mode')

        if len(sys.argv)==1:
            ap.print_help(sys.stderr)
            sys.exit(1)

        args = vars(ap.parse_args())
        if args['console'] and not args['gui']:
            if args['regcolumns'] and args['columns']:
                print('Something went wrong. You passed --regcolumns and --columns which is ambiguous.')
                sys.exit(-1)
            if args['in'] and not os.path.isfile(args['in']):
                print('Something went wrong. Input file {} does not exist.'.format(args['in']))
                sys.exit(-1)
            if args['out'] and not os.path.isdir(args['out']):
                print('Something went wrong. Output directory {} does not exist.'.format(args['out']))
                sys.exit(-1)

            from start_console import start_cli
            start_cli(args['in'], args['out'], args['index'], args['columns'], args['regcolumns'], args['groupcolumns'],
                      args['center'], args['standarize'], args['axis'], args['algorithm'], args['n_components'],
                      args['plot'])

        elif not args['console'] and args['gui']:
            from start_gui import start_gui

            start_gui()
        else:
            print('Something went wrong. You passed -g and -c or none of them what is ambiguous.')
            ap.print_help(sys.stderr)
            sys.exit(-1)

    else:
        configure_script = {'linux': 'Please source configure.sh',
                            'windows': 'Please run configure.bat',
                            'darwin': 'Please source configure.sh. OSX in not fully supported.'}
        try:
            message = configure_script[platform.system().lower()]
        except KeyError:
            message = "Unsupported operating system."
        finally:
            print("Something went wrong. You dont have virtualenv in programdir.",
                "{}".format(message))
            sys.exit(-1)
