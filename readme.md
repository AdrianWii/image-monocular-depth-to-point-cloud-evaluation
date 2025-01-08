# Evaluation of outdoor 3D reconstruction using Monocular Depth Estimation and Photogrammetry Point Cloud

[![DOI](https://zenodo.org/badge/851808883.svg)](https://doi.org/10.5281/zenodo.14617926)

<!-- ![Cover Image](cover.png) -->

## Authors

**Adrian Widlak** and **Jerzy Orlof**  
**Faculty of Computer Science and Telecommunications**  
Cracow University of Technology, Cracow, Poland  

**Piotr Sulikowski**  
**West Pomeranian University of Technology in Szczecin**  
Faculty of Information Technology and Computer Science  

📧 Email: [adrian.widlak@pk.edu.pl](mailto:adrian.widlak@pk.edu.pl)


## Overview

This repository contains data and code for evaluating 3D reconstruction methods using monocular depth estimation and photogrammetry. The data includes
single outdoor images used for generating point clouds through monocular depth estimation models as well as a set of images with a resolution of 480x853 pixels, used to create reference point clouds via photogrammetry techniques.
Scripts and tools for processing the images, generating point clouds are also included.

## Repository Structure


This repository contains all the necessary files and resources for the research project:

- **/ENVIRONMENT**  
  Contains a `.yaml` configuration file for setting up the proper Python environment using Anaconda.

- **/POINT CLOUD**  
  Includes generated point clouds based on Monocular Depth Estimation (MDE) models such as GLPN, ZOE, and DPT.

- **/OUTDOOR IMAGES**  
  A collection of outdoor images used for photogrammetry-based 3D reconstruction.

- **/SCRIPTS**  
  Contains Python scripts for generating point clouds based on single-image depth assessment.


## Citation

If you use this data in your research, please cite the following article:

```bibtex

@article{Widlak2025,
  title     = {Evaluation of outdoor 3D reconstruction using Monocular Depth Estimation and Photogrammetry Point Cloud},
  author    = {Adrian Widłak and Jerzy Orlof and Piotr Sulikowski},
  year      = {2025},
  note      = {To appear in IEEE Transactions on Geoscience and Remote Sensing [if applicable]},
}

```