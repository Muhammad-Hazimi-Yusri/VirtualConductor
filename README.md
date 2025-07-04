<h3 align="center">
<span>Virtual Conductor</span>
</h3>


<h4 align="center">
The first step towards deep learning based music driven conducting motion generation. 
</h4>

![model pipline](assets/model_pipline.png)

This repository is the official implementation of 
*“**Self-Supervised Music-Motion Synchronization Learning for Music-Driven Conducting Motion Generation**”*, 
by 
[Fan Liu](https://cies.hhu.edu.cn/_s97/2013/0508/c4122a54931/page.psp), 
[Delong Chen](https://chendelong.world), 
[Ruizhi Zhou](https://github.com/ZhouRuiZhi), 
Sai Yang, and Feng Xu. 
This repository also provide the access to the ***ConductorMotion100*** dataset, which consists of 100 hours of orchestral conductor motions and aligned music Mel spectrogram.

The above figure gives a high-level illustration of the proposed two-stage approach. The contrastive learning and generative learning stage are bridged by transferring learned music and motion encoders, as noted in dotted lines. Our approach can generate plausible, diverse, and music-synchronized conducting motion.


**Updates**🔔

- **Mar 2021.** [Demo Video (preliminary version)](https://www.bilibili.com/video/BV1pB4y1P7oh) released at bilibili.
- **Apr 2021.** [ICME 2021 Demo Video](https://www.bilibili.com/video/BV1aX4y1g7wh) released at bilibili.
- **Apr 2021.** [Demo Video (with Dynamic Frequency Domain Decomposition)](https://www.bilibili.com/video/BV1Zy4y1W7Qq) released.
- **Jun 2021.** The [recording](https://www.bilibili.com/video/BV1yK4y137Xk) of graduation thesis defense released. The graduation thesis is awarded as Outstanding Graduation Thesis of Hohai University (河海大学优秀毕业论文) and First-class Outstanding Graduation Thesis of Jiangsu Province (江苏省优秀毕业论文一等奖)!
- **Jul 2021.** The _VirtualConductor_ project is awarded as [Best Demo](http://2021.ieeeicme.org/2021.ieeeicme.org/best_demo_awards.html) of IEEE International Conference on Multimedia and Expo (ICME) 2021!
- **Mar 2022.** _ConductorMotion100_ is made publicly available, as a track in the [“Prospective Cup” competition (远见杯)](https://prospective.tocenet.org/)  hold by JSCS ([江苏省计算机学会]((https://www.jscs.org.cn/x1.php?id=770))). Please see [here](/ProspectiveCup/README.md) for details.
- **May 2022.** Our paper is published at _Journal of Computer Science and Technology (JCST)_. Check our [paper](https://link.springer.com/article/10.1007/s11390-022-2030-z)!
- **Nov 2022.** Code for JCST paper is released.

# My (mhby1g21) Contributions & PHENICX Dataset Usage Guide

This section documents additional tools and scripts for working with the PHENICX-conduct dataset (researching its capabilities to work with original VirtualConductor framework), as well as how to set up the environment and run training/testing (VirtualConductor) on both HPC and WSL. If you are taking over this project, please read carefully!

## Environment Setup

**Clone the repository and enter the directory:**
```bash
git clone https://github.com/ChenDelong1999/VirtualConductor.git
cd VirtualConductor
```

**Create and activate a conda environment (for WSL or HPC):**
```bash
# For WSL
conda env create -f environment_wsl.yml
conda activate VirtualConductor_wsl

# For HPC
conda env create -f environment_hpc.yml
conda activate VirtualConductor_latest
```

**Install extra Python dependencies (for PHENICX datasets, can be in separate venv):**
```bash
pip install librosa matplotlib scipy tqdm moviepy opencv-python tensorboard playwright
playwright install
```

## PHENICX Dataset Scripts

- **Automated Download of Repovizz Fragments:**
  - Script: `PHENICX_dataset/download_all_missing_dataset.py`
  - Automates downloading all missing PHENICX-conduct fragments from Repovizz using Playwright.
  - If you encounter a Cloudflare/CAPTCHA page, the script will open a browser window and prompt you to solve it manually.
  - **Usage:**
    ```bash
    python PHENICX_dataset/download_all_missing_dataset.py
    ```
  - Downloaded zips will be saved in `PHENICX_dataset/raw_example/`.

- **Plotting All Subjects' Motions:**
  - Script: `PHENICX_dataset/raw_main_audio_and_mocap_only/plot_all_subjects_motion.py`
  - Visualizes all available subject/fragment folders in 3D.
  - **Usage:**
    ```bash
    python PHENICX_dataset/raw_main_audio_and_mocap_only/plot_all_subjects_motion.py
    ```

- **Manual Test Plot for a Single Subject/Fragment:**
  - Script: `PHENICX_dataset/raw_main_audio_and_mocap_only/subject01_frag01_take03/testplot_manual.py`
  - Visualizes motion for a single subject/fragment.
  - **Usage:**
    ```bash
    python PHENICX_dataset/raw_main_audio_and_mocap_only/subject01_frag01_take03/testplot_manual.py
    ```

## Training and Testing on HPC/WSL

- **Environment Setup:**
  - Use the appropriate `environment_hpc.yml` or `environment_wsl.yml` as above.
  - For GPU jobs, ensure your environment includes the correct CUDA toolkit.

- **Running on HPC (SLURM):**
  - Use the provided SLURM scripts (`submit_test_train.sh`, `submit_test_train_gan.sh`) as templates.
  - Example SLURM job submission:
    ```bash
    sbatch submit_test_train.sh
    ```
  - These scripts activate the conda environment, set CUDA variables, and run your training or test scripts.
  - For more details on job submission, conda environments, and SLURM usage, see the [HPC Community Wiki](https://sotonac.sharepoint.com/teams/HPCCommunityWiki).

- **Running on WSL:**
  - Activate your environment:
    ```bash
    conda activate VirtualConductor_wsl
    ```
  - Run training or test scripts as usual:
    ```bash
    python M2SNet_train.py --dataset_dir <Your Dataset Dir>
    python test_unseen.py --model 'checkpoints/M2SGAN/M2SGAN_official_pretrained.pt'
    ```

---

# Original Getting Started

## Install

- Clone this repo:

    ```bash
    git clone https://github.com/ChenDelong1999/VirtualConductor.git
    cd VirtualConductor
    ```

- Create a conda virtual environment and activate it:

    ```bash
    conda create -n VirtualConductor python=3.6 -y
    conda activate VirtualConductor
    ```

- Install `CUDA Toolkit 11.3` ([link](https://developer.nvidia.com/cuda-11.3.0-download-archive)) and `cudnn==8.2.1` [(link)](https://developer.nvidia.com/rdp/cudnn-archive), then install `PyTorch==1.10.1`:

    ```bash
    conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch -y
    # if you prefer other cuda versions, please choose suitable pytorch versions
    # see: https://pytorch.org/get-started/locally/
    ```

- Install other requirements:

    ```bash
    conda install ffmpeg -c conda-forge -y
    pip install librosa matplotlib scipy tqdm moviepy opencv-python tensorboard
    ```

## Test on Your Own Music 🎶

- Copy your music file to `/test/test_samples/` folder. We have prepared some for you. 
- You need the pretrained weights of a  M<sup>2</sup>S-GAN to generate motions. We have prepared a pretrained checkpoint, which is placed at `checkpoints/M2SGAN/M2SGAN_official_pretrained.pt`. 
- Now, by run the following comment, the `test_unseen.py` will do the following:
  1. enumerate all samples in `/test/test_samples/` folder, 
  2. extract Mel spectrogram from music, 
  3. generate conducting motions, and 
  4. save result videos to `/test/result/`

      ```bash
      python test_unseen.py --model 'checkpoints/M2SGAN/M2SGAN_official_pretrained.pt'
      ```

## Data Preparation (*ConductorMotion100*)

The ConductorMotion100 dataset can be downloaded in the following ways:

- The training set：https://pan.baidu.com/s/1Pmtr7V7-9ChJqQp04NOyZg?pwd=3209
- The validation set：https://pan.baidu.com/s/1B5JrZnFCFvI9ABkuJeWoFQ?pwd=3209 
- The test set：https://pan.baidu.com/s/18ecHYk9b4YM5YTcBNn37qQ?pwd=3209 

You can also access the dataset via [**Google Drive**](https://drive.google.com/drive/folders/1I2eFM-vEbqVXtD4sUPmGFSeNZeu_5JMu?usp=sharing)

There are 3 splits of *ConductorMotion100*: train, val, and test. They respectively correspond to 3 `.rar` files. After extract them to `<Your Dataset Dir>` folder, the file structure will be:

```
tree <Your Dataset Dir>
<Your Dataset Dir>
    ├───train
    │   ├───0
    │   │       mel.npy
    │   │       motion.npy
    |  ...
    │   └───5268
    │           mel.npy
    │           motion.npy
    ├───val
    │   ├───0
    │   │       mel.npy
    │   │       motion.npy
    |  ...
    │   └───290
    │           mel.npy
    │           motion.npy
    └───test
        ├───0
        │       mel.npy
        │       motion.npy
       ...
        └───293
                mel.npy
                motion.npy
```

Each `mel.npy` and `motion.npy` are corresponded to <u>60 seconds</u> of Mel spectrogram and motion data. Their sampling rates are respectively <u>90 Hz</u> and <u>30 Hz</u>. The Mel spectrogram has 128 frequency bins, therefore `mel.shape = (5400, 128)`. The motion data contains 13 2d keypoints, therefore `motion.shape = (1800, 13, 2)`

We provide codes to load and visualize the dataset, as in `utils/dataset.py`. You can run this file by:

```bash
python utils/dataset.py --dataset_dir <Your Dataset Dir>
```

Then the script will enumerate all the samples in the dataset. You will get:

![matshow](assets/matshow.png)

![motion_plot](assets/motion_plot.png)

## Training

During training, use `tensorboard --logdir runs` to set up tensorboard logging. Model checkpoints will be saved to `/checkpoints/` folder.

- **Step 1**

  - Start contrastive learning stage, train the M<sup>2</sup>S-Net:

      ```bash
      python M2SNet_train.py --dataset_dir <Your Dataset Dir>
      ```

      It takes ~36 hours with a Titan Xp GPU. With tensorboard (`tensorboard --logdir runs`), you can visualize the training procedure:

      ![M2SNet-tensorboard](assets/M2SNet-tensorboard.png)

      We also provide the visualization of the features extracted by M<sup>2</sup>S-Net
      ![M2SNet-features](assets/M2SNet-features.png)
    
      <!-- Easy: 0.73337 | Hard: 0.67346 | Super-hard: 0.62021 -->

- **Step 2 (optional)**
  - Train a M2S-Net on test set to calculate the 'sync error' (see our paper for more details):

    ```bash
    python M2SNet_train.py --dataset_dir <Your Dataset Dir> --mode hard_test
    ```
    The training takes ~2.5 hours.
    ![img.png](assets/M2SNet-tensorboard-hard-test.png)
  
    <!-- Easy: 0.59187 | Hard: 0.56757 | Super-hard: 0.53661 -->

- **Step 3**
  - Start generative learning stage, train the M<sup>2</sup>S-GAN:

     ```bash
     python M2SGAN_train.py --dataset_dir <Your Dataset Dir>
     ```
    The training takes ~28 hours with a Titan Xp GPU.
    ![img.png](assets/M2SGAN-tensorboard.png)
  
    <!-- MPE: 0.76339 | RDE: 0.58609 | SCE: 1.88849 -->

## Prospective Cup (首届国际“远见杯”元智能数据挑战大赛)

For more details of the "Prospective Cup" competition, please see [**here**](ProspectiveCup/README.md).

## License

Copyright (c) 2022 Delong Chen. Contact me for commercial use (or rather any use that is not academic research) (email: chendelong@hhu.edu.cn). Free for research use, as long as proper attribution is given and this copyright notice is retained.

## **Papers**

1. Delong Chen, Fan Liu*, Zewen Li, Feng Xu. [VirtualConductor: Music-driven Conducting Video Generation System](https://arxiv.org/abs/2108.04350). _IEEE International Conference on Multimedia and Expo (ICME) 2021, [Demo Track (Best Demo)](http://2021.ieeeicme.org/2021.ieeeicme.org/best_demo_awards.html)._

   ```bibtex
   @article{chen2021virtualconductor,
     author    = {Delong Chen and
                  Fan Liu and
                  Zewen Li and
                  Feng Xu},
     title     = {VirtualConductor: Music-driven Conducting Video Generation},
     journal   = {CoRR},
     volume    = {abs/2108.04350},
     year      = {2021},
     url       = {https://arxiv.org/abs/2108.04350},
     eprinttype = {arXiv},
     eprint    = {2108.04350}
   }
   ```

2. Fan Liu, Delong Chen*, Ruizhi Zhou, Sai Yang, and Feng Xu. [Self-Supervised Music-Motion Synchronization Learning for Music-Driven Conducting Motion Generation](https://link.springer.com/article/10.1007/s11390-022-2030-z). _Journal of Computer Science and Technology_.

   ```bibtex
    @article{liu2022self,
      author    = {Fan Liu and
                   Delong Chen and
                   Ruizhi Zhou and
                   Sai Yang and
                   Feng Xu},
      title     = {Self-Supervised Music Motion Synchronization Learning for Music-Driven
                   Conducting Motion Generation},
      journal   = {Journal of Computer Science and Technology},
      volume    = {37},
      number    = {3},
      pages     = {539--558},
      year      = {2022},
      url       = {https://doi.org/10.1007/s11390-022-2030-z},
      doi       = {10.1007/s11390-022-2030-z}
    }
   ```

