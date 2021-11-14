"""


"""

import subprocess
import psutil
import shutil
import os

tmp_input_dir = 'tmp_inputs'
tmp_output_dir = 'tmp_outputs'
cfmid4_folder = '$HOME/cfmid4'


def split_file(mfile, num): 
    with open(mfile) as infp:
        if  os.path.exists(tmp_input_dir):
            shutil.rmtree(tmp_input_dir)
        if  os.path.exists(tmp_output_dir):
            shutil.rmtree(tmp_output_dir)
        os.mkdir(tmp_input_dir)
        os.mkdir(tmp_output_dir)
        files = [open(f'{tmp_input_dir}/{i}.txt', 'w') for i in range(num)]
        for i, line in enumerate(infp):
            files[i % num].write(line)
        for f in files:
            f.close()

def merge_files(num, tmp_dir, ext, outfile):
    if  os.path.exists(outfile):
        shutil.rmtree(outfile)
    with open(outfile, 'w') as out:
        for i in range(num):
            with open(f'{tmp_dir}/{i}.{ext}') as infile:
                for line in infile:
                    out.write(line)


def on_terminate(proc):
      print("process {} terminated".format(proc))
      

def cfmid4_mp(num, sfile, timeout):
    procs_list = []
    for i in range(num):
        command = f'/public/software/singularity/bin/singularity run -i \
{cfmid4_folder}/cfmid4.sif sh -c "cfm-id {cfmid4_folder}/{sfile} AN_ID \
{cfmid4_folder}/{tmp_input_dir}/{i}.txt -1 10 0.001 0.001 \
/trained_models_cfmid4.0/[M+H]+/param_output.log \
/trained_models_cfmid4.0/[M+H]+/param_config.txt Dice 1 \
{cfmid4_folder}/{tmp_output_dir}/{i}.txt \
{cfmid4_folder}/{tmp_output_dir}/{i}.msp" '   
        print(command)
        p = subprocess.Popen(command, shell=True)
        procs_list.append(psutil.Process(p.pid))
    gone, alive = psutil.wait_procs(procs_list, timeout=timeout, callback=on_terminate)


if __name__=="__main__":
    num = 40
    split_file('molecules.txt', num)
    cfmid4_mp(num, 'spectrum.txt', 24*60*60)
    merge_files(num, tmp_output_dir, 'txt', 'results.txt')
    merge_files(num, tmp_output_dir, 'msp', 'spectra.msp')
    
