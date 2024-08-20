#unvco_datain_upload.py
#module for upload of unavco datain files
#depends on access to the curl utility

curl_options = "-LSs"
base = "https://data-in.unavco.org/pub/"

def validate_options(options):
    program_configs = dict()
    workdir = dirname(__file__)
    if (exists(join(workdir,"unavco_datain_upload.conf"))):
        with open(join(workdir,"unavco_datain_upload.conf"),"r") as configurations:
            for line in configurations:
                if ("=" in line):
                    tokens = line.split("=")
                    program_configs[tokens[0]] = [tokens[1].rstrip()] 

    if ( not options['directory'] == None ):
        program_configs['directory'] = options['directory']
    elif ( not 'directory' in program_configs.keys() ):
            print ("Directory is not specified by command line or in the .conf file: EXITING")
            exit()

    if ( not options['area'] == None ):
        program_configs['area'] = options['area']
    elif ( not 'area' in program_configs.keys() ):
            print ("Area is not specified by command line or in the .conf file: EXITING")
            exit()

    if ( not options['username'] == None ):
        program_configs['username'] = options['username']
    elif ( not 'username' in program_configs.keys() ):
            print ("User name is not specified by command line or in the .conf file: EXITING")
            exit()

    if (options['progress'] == None ):
        program_configs['progress'] = False
    else:
        program_configs['progress'] = options['progress']

    results = Popen(["which","curl"],stdout=PIPE,stderr=PIPE)
    output,errors = results.communicate()
    if ( "curl" in output.decode("utf-8").rstrip()):
         program_configs['curl'] = output.decode("utf-8").rstrip()
    elif ( not 'curl' in program_configs.keys() ):
         print ("The curl command is not found in the path or the .conf file: EXITING")

    return program_configs

def get_token(configs,single):
    if (type(configs['area']) is str):
        url = join(base,configs['area'],configs['directory']) + "?username=" + \
            configs['username']
    else:
        url = join(base,configs['area'][0],configs['directory'][0]) + "?username=" + \
            configs['username'][0]
    results = Popen([configs['curl'],curl_options,url],stdout=PIPE,stderr=PIPE)
    output,errors = results.communicate()
    if (not output.decode("utf-8").rstrip() == ""):
        return output.decode("utf-8").rstrip()
    else:
        print("Error reaching the service host {}".format(errors.decode("utf-8").rstrip()))
        return str(0)

def push_file(configs,single,ul_token):
    filedesig = basename(single)
    if (type(configs['area']) is str):
        url = join(base,configs['area'],configs['directory']) + "/?username=" + \
            configs['username'] + "&authkey=" + ul_token
    else:
        url = join(base,configs['area'][0],configs['directory'][0]) + "/?username=" + \
            configs['username'][0] + "&authkey=" + ul_token
    upload = "data_source=@" + single + ";filename=" + filedesig + ";"

    if (configs['progress']):
        progress_options = "-L#"
       
        results = Popen([configs['curl'],progress_options,'-o','/dev/null','-F',upload,url],
            stdout=stdout, stderr=stderr, bufsize=0)

        while (results.poll() == None):
             try:
             #    results.wait(timeout=5)
             #except TimeoutExpired:
                 update = results.stderr.flush()
                 print(update)
             except AttributeError:
                 pass

        output,errors = results.communicate()
                 
             
#        if (not 'pub' in output.decode("utf-8")):
#            print ("Error uploading {} : {} {}".format(single,output.decode("utf-8").rstrip(),
#                errors.decode("utf-8").rstrip()))
    else:
        results = Popen([configs['curl'],curl_options,"-F",upload,url],stdout=PIPE,
            stderr=PIPE)
        output,errors = results.communicate()
        if (not errors.decode("utf-8").rstrip() == ""):
            print ("Error uploading {} : {} {}".format(single,output.decode("utf-8").rstrip(),
                errors.decode("utf-8").rstrip()))

def upload_files(configs,files):
    for single in files:
        ul_token = ""
        if (exists(single)):
            ul_token = get_token(configs,single)
            if (len(ul_token)==32):
                push_file(configs,single,ul_token)
            else:
                print(ul_token)
                exit()
        else:
            print ("Can't locate file {}".format(single))
            

def _process(options):
    configs = validate_options(options)
    upload_files(configs,options['files'])
    print ("Completed upload of files: {}".format(options['files']))

if (__name__ == '__main__'):
    from argparse import ArgumentParser
    from os.path import exists,join,basename,dirname,abspath
    from subprocess import Popen,PIPE,TimeoutExpired
    from sys import stdout,stderr

    parser = ArgumentParser(description="Upload module to batch load files to the UNAVCO(C)TM datain server")
    parser.add_argument("-area","-a",choices=["incoming","ps_in","dropoff"],nargs=1,required=False,
        help="User name associated with the upload account")
    parser.add_argument("-username","-u",nargs=1,required=False,
        help="User name associated with the upload account")
    parser.add_argument("-directory","-d",nargs=1,required=False,
        help="Directory target for file delivery and sorting")
    parser.add_argument("-progress","-p",action='store_true',required=False,
        help="Progress Indicator")
    parser.add_argument("files",nargs="+",
        help="List of files to upload to the UNAVOC(C)TM datain server")
    options = parser.parse_args()

    _process(vars(options))

