_base_ = 'mmdet::pascal_voc/faster-rcnn_r50-caffe-c4_ms-18k_voc0712.py'
# https://github.com/open-mmlab/mmdetection/blob/main/configs/pascal_voc/faster-rcnn_r50-caffe-c4_ms-18k_voc0712.py


metainfo = {
    'classes':
    ('cabinet', 'sofa', 'slippers', 'bed', 'table', 'feces', 'closetool', 'stool', 'curtain', 'book', 'wire', 'trashcan', 'carpet', 'socks'),
    # palette is a list of color tuples, which is used for visualization.
    'palette': [(106, 0, 228), (119, 11, 32), (165, 42, 42), (0, 0, 192), (197, 226, 255), (0, 60, 100), (0, 0, 142), (255, 77, 255), (153, 69, 1), (120, 166, 157), (0, 182, 199), (0, 226, 252), (182, 182, 255), (0, 0, 230)]
}

data_preprocessor = dict(
    type='DetDataPreprocessor',
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    bgr_to_rgb=True,
    pad_size_divisor=32)

norm_cfg = dict(type='SyncBN', requires_grad=True)
model = dict(
    backbone=dict(
        frozen_stages=-1,
        norm_cfg=norm_cfg,
        norm_eval=False,
        style='pytorch',
        init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet50')),
    roi_head=dict(
        shared_head=dict(
            type='ResLayerExtraNorm',
            norm_cfg=norm_cfg,
            norm_eval=False,
            style='pytorch'),
        bbox_head=dict(num_classes=20)))

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='RandomChoiceResize',
        scales=[(1333, 480), (1333, 512), (1333, 544), (1333, 576),
                (1333, 608), (1333, 640), (1333, 672), (1333, 704),
                (1333, 736), (1333, 768), (1333, 800)],
        keep_ratio=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PackDetInputs')
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', scale=(1333, 800), keep_ratio=True),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor'))
]
dataset_type = 'VOCDataset'
data_root = '/mnt/e/data/VOCdevkit/'
dataset_name = 'small_amount_of_indoor_new_20220228'

train_dataloader = dict(
    sampler=dict(type='InfiniteSampler', shuffle=True),
    dataset=dict(
        _delete_=True,
        type='ConcatDataset',
        datasets=[
            dict(
                type=dataset_type,
                data_root=data_root,
                metainfo=metainfo,
                ann_file=f'{dataset_name}/ImageSets/Main/trainval.txt',
                data_prefix=dict(sub_data_root=f'{dataset_name}/'),
                filter_cfg=dict(filter_empty_gt=True, min_size=32),
                pipeline=train_pipeline)
        ]))

val_dataloader = dict(
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        metainfo=metainfo,
        ann_file=f'{dataset_name}/ImageSets/Main/test.txt',
        data_prefix=dict(sub_data_root=f'{dataset_name}/'),
        test_mode=True,
        pipeline=test_pipeline))

test_dataloader = val_dataloader

train_cfg = dict(type='IterBasedTrainLoop', max_iters=24000, val_interval=600)

param_scheduler = [
    dict(
        type='LinearLR', start_factor=0.001, by_epoch=False, begin=0, end=100),
    dict(
        type='MultiStepLR',
        begin=0,
        end=24000,
        by_epoch=False,
        milestones=[18000, 22000],
        gamma=0.1)
]

val_evaluator = dict(type='VOCMetric', metric='mAP', eval_mode='11points')
test_evaluator = val_evaluator

default_hooks = dict(checkpoint=dict(by_epoch=False, interval=600))

log_processor = dict(by_epoch=False)

custom_imports = dict(
    imports=['mmselfsup.models.utils.res_layer_extra_norm'],
    allow_failed_imports=False)

load_from = 'work_dirs/benchmarks/faster-rcnn_r50-c4_ms-24k_voc0712_use_amicro_indoor_small_dataset/iter_3600.pth'