<img src="logo.png" width:100px >    

## SigmaCCS

This is the code repo for the paper *Highly accurate and large-scale collision cross section prediction with graph neural network for compound identification*.  We developed a method named Structure included graph merging with adduct method for CCS prediction ([SigmaCCS](sigma)), and a [dataset](https://doi.org/10.5281/zenodo.5501673) including 282 million CCS values for three different ion adducts ([M+H]+, [M+Na]+ and [M-H]-) of 94 million compounds. For each molecule, there are "Pubchem ID", "SMILES", "InChi", "Inchikey", "Molecular Weight", "Exact Mass", "Formula" and predicted CCS values of three adduct ion types. 

### Package required: 
We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html) and [pip](https://pypi.org/project/pip/).
- [python3](https://www.python.org/) 
- [rdkit](https://rdkit.org/)    
- [tensorflow](https://www.tensorflow.org) 
- [spektral](https://graphneural.network/) 

By using the [`requirements/conda/environment.yml`](requirements/conda/environment.yml), [`requirements/pip/requirements.txt`](requirements/pip/requirements.txt) file, it will install all the required packages.

## Data pre-processing
SigmaCCS is a model for predicting CCS based on graph neural networks, so we need to convert SMILES strings to Graph. The related method is shown in [`sigma/GraphData.py`](simgma/GraphData.py)           

**1.** Generate 3D conformations of molecules. 

    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    ps = AllChem.ETKDGv3()
    ps.randomSeed = -1
    ps.maxAttempts = 1
    ps.numThreads = 0
    ps.useRandomCoords = True
    re = AllChem.EmbedMultipleConfs(mol, numConfs = 1, params = ps)
    re = AllChem.MMFFOptimizeMoleculeConfs(mol, numThreads = 0)
- [ETKDGv3](https://www.rdkit.org/docs/source/rdkit.Chem.rdDistGeom.html?highlight=etkdgv3#rdkit.Chem.rdDistGeom.ETKDGv3) Returns an EmbedParameters object for the ETKDG method - version 3 (macrocycles).
- [EmbedMultipleConfs](https://www.rdkit.org/docs/source/rdkit.Chem.rdDistGeom.html?highlight=embedmultipleconfs#rdkit.Chem.rdDistGeom.EmbedMultipleConfs), use distance geometry to obtain multiple sets of coordinates for a molecule.
- [MMFFOptimizeMoleculeConfs](https://www.rdkit.org/docs/source/rdkit.Chem.rdForceFieldHelpers.html?highlight=mmffoptimizemoleculeconfs#rdkit.Chem.rdForceFieldHelpers.MMFFOptimizeMoleculeConfs), uses MMFF to optimize all of a molecule’s conformations   

**2.** Save relevant parameters. For details, see [`sigma/parameter.py`](sigma/parameter.py).    
- adduct set  
- atoms set   
- Minimum value in atomic coordinates   
- Maximum value in atomic coordinates   

**3.** Generate the Graph dataset. Generate the three matrices used to construct the Graph:    
(1) *node feature matrix*, (2) *adjacency matrix*, (3) *edge feature matrix*.       

    adj, features, edge_features = convertToGraph(smiles, Coordinate, All_Atoms)
    DataSet = MyDataset(features, adj, edge_features, ccs)
*Optionnal args*
- All_Atoms : The set of all elements in the dataset
- Coordinate : Array of coordinates of all molecules
- features : Node feature matrix
- adj : Adjacency matrix
- edge_features : Edge feature matrix

## Model training
Train the model based on your own training dataset with [Model_train](https://github.com/zmzhang/SigmaCCS/blob/main/sigma/sigma.py#L52) function.

    Model_train(ifile, ParameterPath, ofile, ofileDataPath, EPOCHS, BATCHS, Vis, All_Atoms=[], adduct_SET=[])

*Optionnal args*
- ifile : File path for storing the data of smiles and adduct.
- ofile : File path where the model is stored.
- ParameterPath : Save path of related data parameters.
- ofileDataPath : File path for storing model parameter data.

## Predicting CCS
The CCS prediction of the molecule is obtained by feeding the Graph and Adduct into the already trained SigmaCCS model with [Model_prediction](https://github.com/zmzhang/SigmaCCS/blob/main/sigma/sigma.py#L6) function.

    Model_prediction(ifile, ParameterPath, mfileh5, ofile, Isevaluate = 0)

*Optionnal args*
- ifile : File path for storing the data of smiles and adduct
- ParameterPath : File path for storing model parameter data
- mfileh5 : File path where the model is stored
- ofile : Path to save ccs prediction values

## Usage
The example codes for usage is included in the [test.ipynb](test.ipynb)

## Others
The following files are in the [others](others) folder:
- [Attribute Analysis.ipynb](others/Attribute%20Analysis.ipynb). analyze the attribute importance
- [UMAP.ipynb](others/UMAP.ipynb). visualize the learned representation with UMAP
- [UMAPDataset.py](others/UMAPDataset.py). for generating graph datasets.
- [theoretical calculation.ipynb](others/theoretical%20calculation.ipynb). investigate of the relationship between SigmaCCS and theoretical calculation
- [Filtering.ipynb](others/Filtering.ipynb). Filtering of target unknown molecules based on the CCS and *mz* of the molecules
- *[CFM-ID4](others/CFM-ID4)*. the code for generating MS/MS spectra with CFM-ID 4.0.
- *[GNN-RT](others/GNN-RT)*:
    - [README.md](others/GNN-RT/README.md)
- *[model](model)*:
    - model.h5
- *[data](others/data)*:
    - *Attribute importance data*
        - *Attribute importance* (data.csv)
        - *Coordinate data* (Store the 3D coordinate data of all molecules in data.csv)
    - *UMAP data*
        - data.csv
        - data_molvec.npy (Molecular vectors of all molecules)
        - data-UMAP-EUC-60.npy
        - *Coordinate data* (Store the 3D coordinate data of all molecules in data.csv)
    - *theoretical calculation data*
        - data.csv
        - LJ_data.csv (Get the LJ interaction parameters of different elements according to LJ_data.csv)
        - *Coordinate data* (Store the 3D coordinate data of all molecules in data.csv)
    - *Filtering data* 
        - data.csv 

### Package required: 
- [UMAP](https://github.com/lmcinnes/umap) 0.5.1

## Slurm script
slurm script for generating CCS of PubChem in HPC cluster.
The following files are in the [`slurm`](slurm) folder
- mp.py
- multiple_job.sh (Batch generation of slurm script files)
- normal_job.sh (Submit the slurm script for the mp.py file)

## Information of maintainers
- zmzhang@csu.edu.cn
- youjiazhang126@163.com
- renfengguo05@foxmail.com
