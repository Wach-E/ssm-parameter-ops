from dotenv import load_dotenv
from tabulate import tabulate

import argparse
import boto3
import os

load_dotenv()

aws_region = os.getenv('REGION')
config_path = os.getenv('SSM_PARAMS_PATH')
params_tld = os.getenv('PROJECT')

parser = argparse.ArgumentParser(description='''
SSM Automation Tool is used to list the current parameters in AWS SSM Parameter Store and perform a bulk upload of the contents within a .env file whose location is specified by path.
''')

parser.add_argument('first_operation', type=str, help='list all parameters in AWS SSM Parameter Store')
parser.add_argument('second_operation', nargs='?', type=str, help='upload config keypairs to AWS SSM Parameter Store')

args = parser.parse_args()

arg1 = args.first_operation
arg2 = args.second_operation

ssm = boto3.client('ssm', region_name=aws_region)

def list_parameters():
    paginator = ssm.get_paginator('describe_parameters')
    parameter_iterator = paginator.paginate()

    table = []
    for response in parameter_iterator:
        parameters = response['Parameters']
        for parameter in parameters:
            name = parameter['Name']
            type = parameter['Type']
            version = parameter['Version']
            table.append([name, type, version])
    headers = ['Name', 'Type', 'Version']
    table_str = tabulate(table, headers, tablefmt='grid')
    print(table_str)


def upload_parameters_from_file(path, params_tld):
    with open(path, 'r') as params:
        for line in params:
            line = line.strip()
            if line:
                parameter_name, parameter_value = line.split('=', 1) # setting the maxsplit parameter to 1 to accomodate values with `=` present
                parameter_name = f"{params_tld}/{parameter_name}"
                response = ssm.put_parameter(
                    Name = parameter_name,
                    Value = parameter_value,
                    Type = 'SecureString',
                    Overwrite = True,
                    Tier = 'Standard',
                    DataType = 'text'
                )
                
                print(f"Parameter '{parameter_name}' added successfully.")

def ops(ops_arg):
    if ops_arg == 'list':
        print("Current parameters...")            
        return list_parameters()
    elif ops_arg == 'upload':
        print("Uploading config...")
        return upload_parameters_from_file(config_path, params_tld)
        
def ops_response(first_op,second_op=None):  
    ops(first_op)
    if second_op != None:
        ops(second_op)

def main():
    if (arg1 in ['list', 'upload']) and (arg2==None):
        ops_response(arg1)
    elif arg1 in ['list', 'upload'] and (arg2 != None) and (arg1 != arg2):
        ops_response(arg1,arg2)
    else:
        print('''You need to specify at least 1 argument list or upload.
              \n If you must specify two, they need to be mutually exclusive''')


if __name__ == '__main__':
    main()


    
