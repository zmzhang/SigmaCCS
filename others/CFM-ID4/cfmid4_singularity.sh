
#Create image
cd ~
mkdir cfmid4
cd cfmid4
/public/software/singularity/bin/singularity pull cfmid4.sif docker://wishartlab/cfmid

#Run command in image
/public/software/singularity/bin/singularity exec cfmid4.sif cfm-train --help 
/public/software/singularity/bin/singularity run -i cfmid4.sif sh -c "cd /trained_models_cfmid4.0/[M+H]+; ls"
/public/software/singularity/bin/singularity shell cfmid4.sif


#Test CFM-ID 4.0
/public/software/singularity/bin/singularity run -i $HOME/cfmid4/cfmid4.sif sh -c "cfm-id $HOME/cfmid4/spectrum.txt AN_ID $HOME/cfmid4/molecules.txt -1 10 0.001 0.001 /trained_models_cfmid4.0/[M+H]+/param_output.log /trained_models_cfmid4.0/[M+H]+/param_config.txt Dice 1 results.txt insilico_spectra.msp"

