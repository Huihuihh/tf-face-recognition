#!/bin/bash
cd $CODE_PATH/facenet
export PYTHONPATH=$CODE_PATH/facenet/src

python $CODE_PATH/facenet/src/train_softmax.py \
--logs_base_dir /tmp/log \
--models_base_dir $MODEL_PATH \
--data_dir $DATASET_PATH \
--image_size 160 \
--model_def models.inception_resnet_v1 \
--lfw_dir $LFW_DATASET_DIR \
--optimizer ADAM \
--learning_rate $LEARNING_RATE \
--max_nrof_epochs $MAX_NROF_EPOCHS \
--keep_probability 0.8 \
--random_crop \
--random_flip \
--use_fixed_image_standardization \
--learning_rate_schedule_file data/learning_rate_schedule_classifier_casia.txt \
--weight_decay 5e-4 \
--embedding_size 512 \
--lfw_distance_metric 1 \
--lfw_use_flipped_images \
--lfw_subtract_mean \
--validation_set_split_ratio 0.05 \
--validate_every_n_epochs 5 \
--prelogits_norm_loss_factor 5e-4 \
--epoch_size $EPOCH_SIZE \
--gpu_memory_fraction 0.8
