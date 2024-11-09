if [ $# == 0 ] 
then
    SEED=42
    LR=2e-5
else
    SEED=$1
    LR=$2
fi

work_path=exps/MLEE_large/CsEAE
mkdir -p $work_path

CUDA_VISIBLE_DEVICES=0 python -u engine.py \
    --model_type=amr \
    --dataset_type=MLEE \
    --model_name_or_path=../plm/bart-large \
    --role_path=./data/MLEE/MLEE_role_name_mapping.json \
    --prompt_path=./data/prompts/prompts_MLEE_full.csv \
    --seed=$SEED \
    --output_dir=$work_path \
    --learning_rate=$LR \
    --max_steps=10000 \
    --max_enc_seq_length 500 \
    --max_prompt_seq_length 80 \
    --bipartite
