## 依赖
- `python3.7.6`
- `openvino_2020.1.023`
- `NCS2`
- `Ubuntu18.04`

## 生成openvino需要的模型文件

- 将train之后得到的pb文件进行转换

`python /opt/intel/openvino_2020.1.023/deployment_tools/model_optimizer/mo_tf.py --input_model ../models/facenet.pb --output_dir lrmodels/

## 使用openvino进行推理（VPU）
```
cd server
./server.sh
```
