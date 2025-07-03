#!/bin/bash
#SBATCH --job-name=traingan   #test_unseen
#SBATCH --nodes=1                  # Request 1 node
#SBATCH --ntasks=1                 # Request 1 task
#SBATCH --partition=lyceum          # Your partition name
#SBATCH --gres=gpu:1                # Request 1 GPU
#SBATCH --mem=32G                   # Request 32GB RAM  
#SBATCH --cpus-per-task=4           # Request 4 CPUs
#SBATCH --time=55:00:00             #  time limit
#SBATCH --output=traingan_%j.out # Output file (%j = job ID)
#SBATCH --error=traingan_%j.err  # Error file
#SBATCH --mail-type=ALL             # Email notifications (optional)
#SBATCH --mail-user=mhby1g21@soton.ac.uk  # Your email (optional)

# Print job info
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $SLURM_NODELIST"
echo "Starting at: $(date)"

# Activate your conda environment
source ~/.bashrc
conda activate VirtualConductor_latest

# Set environment variables to avoid issues
export CUDA_LAUNCH_BLOCKING=1
export OMP_NUM_THREADS=1
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Change to your working directory
cd VirtualConductor  # Update this path!

# Check CUDA availability first
echo "Checking CUDA availability..."
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU count:', torch.cuda.device_count())"

# Run the test script
#echo "Starting test_unseen.py..."
#python admin_test_unseen.py --model 'checkpoints/M2SGAN/M2SGAN_official_pretrained.pt'

echo "Starting M2SGAN_train.py..."
python M2SGAN_train.py --dataset_dir dataset

echo "Job finished at: $(date)"