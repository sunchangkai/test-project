# ProsafeAI API List PI23.2

开发环境后端地址：http://10.38.49.30:8000/

用户名：superadmin 密码：admin123456 (拥有所有权限)

用户名：admin 密码：admin123456 (管理员权限)

用户名：liping 密码：admin123456 (普通用户)

需要先登录用户，获取session,cookie等header

```shell
curl --location '10.38.49.30:8000/apiLogin/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "superadmin",
    "password": "admin123456"
}'
```
然后才可以正常访问相关接口。

## 1. modelV_sdk

与sdk交互的模块，主要实现数据传输，权限验证

### a. create_run
#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_sdk/create_run/ | POST  |


#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| token | String | 是  | 无    | 随机token   |
| task_type  | String | 是  | 无      | task类型: 0: robustness;1: basic_metrics    |
| hyperparameter  | String | 是  | 无      | 超参数 |
| signature  | String | 否  | 无      | 签名     |

#### 响应结果
* 返回HTTP状态：2000表示成功，400表示失败
* 返回msg为创建成功/失败信息
* 结果描述：data中包含响应的数据,即run_id

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_sdk/create_run/' \
--header 'X-CSRFToken: pmkquVmhO29RsDfw7AKssVg2cr7v5LsMAMlYOdji7C54oovjnPn2edSTG4FFAuSn' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=pmkquVmhO29RsDfw7AKssVg2cr7v5LsMAMlYOdji7C54oovjnPn2edSTG4FFAuSn; sessionid=91oq47rx61n5kz88geekbf7tlwlbhsar' \
--data '{
    "token": "af7ea4c0-d773-11ed-83f7-0242ac110002",
    "task_type": "0",
    "hyperparameter": "test_6"
}'
```

响应
```json
{
    "code": 2000,
    "data": {
        "run_id": 8
    },
    "msg": "success"
}
```

### b. check_metadata
#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_sdk/check_metadata/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| token | String | 是  | 无    | 随机token   |
| run_id | int | 是  | 无    | run_id   |
|file |file文件|是 | 无 |需要上传的文件 |
| signature  | String | 否  | 无      | 签名 |

#### 响应结果
* 返回HTTP状态：2000表示成功，400表示失败
* 返回msg为检查成功/失败信息

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_sdk/check_metadata/' \
--header 'X-CSRFToken: pmkquVmhO29RsDfw7AKssVg2cr7v5LsMAMlYOdji7C54oovjnPn2edSTG4FFAuSn' \
--header 'Cookie: csrftoken=pmkquVmhO29RsDfw7AKssVg2cr7v5LsMAMlYOdji7C54oovjnPn2edSTG4FFAuSn; sessionid=91oq47rx61n5kz88geekbf7tlwlbhsar' \
--form 'token="af7ea4c0-d773-11ed-83f7-0242ac110002"' \
--form 'file=@"/metadata_1_version_1.txt"' \
--form 'run_id="5"'
```

响应
```shell
# pass
{
    "code": 2000,
    "data": null
    "msg": "success"
}
# failed
{
    "code": 400,
    "data": null
    "msg": "failed"
}
```

### c. save_phased_results

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_sdk/save_phased_results/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| token | String | 是  | 无    | 随机token   |
| run_id | String | 是  | 无    | run_id   |
|results |dict|是 | 无 |阶段性结果 |
|status |String|是 | 无 |状态 0:running，1:done |
| signature  | String | 否  | 无      | 签名 |

#### 响应结果
* 返回HTTP状态：2000表示成功，400表示失败
* 返回msg为保存成功/失败信息

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_sdk/save_phased_results/' \
--header 'X-CSRFToken: pmkquVmhO29RsDfw7AKssVg2cr7v5LsMAMlYOdji7C54oovjnPn2edSTG4FFAuSn' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=pmkquVmhO29RsDfw7AKssVg2cr7v5LsMAMlYOdji7C54oovjnPn2edSTG4FFAuSn; sessionid=91oq47rx61n5kz88geekbf7tlwlbhsar' \
--data '{
    "token": "af7ea4c0-d773-11ed-83f7-0242ac110002",
    "run_id": 7,
    "results": {"criteria": "test", "iteration": "20", "fail_test_num": "10", "total_mutator": "30", "ASR": "0.9"},
    "status": "0"
}'
```

响应：
```json
{
    "code": 2000,
    "data": null,
    "msg": "success"
}
```

### d. save_results
#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_sdk/save_results/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| token | String | 是  | 无    | 随机token   |
| run_id | String | 是  | 无    | run_id   |
|file |File/Zip|是 | 无 |最终结果 |
| signature  | String | 否  | 无      | 签名 |

#### 响应结果
* 返回HTTP状态：2000表示成功，400表示失败
* 返回msg为保存成功/失败信息

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_sdk/save_results/' \
--header 'X-CSRFToken: cchEIwx6aL5BjUD1IaRB9gBQsqGJPmuI1t02TJJdSf1USWtx9iiB2ZciL6BlM9Fb' \
--header 'Cookie: csrftoken=cchEIwx6aL5BjUD1IaRB9gBQsqGJPmuI1t02TJJdSf1USWtx9iiB2ZciL6BlM9Fb; sessionid=h9io9393yz8t3o0d7g5jxq5yjavy7rbl' \
--form 'token="af7ea4c0-d773-11ed-83f7-0242ac110002"' \
--form 'file=@"/metadata_1_version_1.txt"' \
--form 'run_id="2"'
```

响应：
```json
{
    "code": 2000,
    "data": null,
    "msg": "success"
}
```

### e. get_ground_truth
### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_sdk/get_ground_truth/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| token | String | 是  | 无    | 随机token   |
| img_list | List | 是  | 无    | 需要获取标注数据的image列表   |

#### 响应结果
* 返回HTTP状态：2000表示成功，400表示失败
* 输出参数：包含在响应的Body中，JSON格式字符串

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_sdk/get_ground_truth/' \
--header 'X-CSRFToken: jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H; sessionid=wcu4i3mh13oht3nhm4gkil48qoi8fvi1' \
--data '{
    "token": "bbdd4bf7380ed50bb909af554a1a1c97",
    "img_list": ["001_Female_20_Afternoon_Anger_ir_00054.png", "001_Female_20_Afternoon_Fear_ir_00023.png"]
}'
```

响应：

```json
{
    "code": 2000,
    "data": {
        "001_Female_20_Afternoon_Anger_ir_00054.png": [
            {
                "bbox": [
                    433.6870085964,
                    171.5398192259,
                    495.5488704582,
                    263.4317111178
                ],
                "class": "0",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    412.4017233111,
                    152.9932726794,
                    461.6990206084,
                    206.614894301
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    504.0773989868,
                    400.9332126193,
                    537.4440990201,
                    440.9732526594
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    204.1154370248,
                    163.9222016083,
                    249.0884099978,
                    199.3816610678
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    222.277599187,
                    314.4086880948,
                    262.9262478356,
                    391.3816610678
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    309.6289505383,
                    209.7600394462,
                    361.5208424302,
                    262.5167962029
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    331.2432432432,
                    395.2432432432,
                    382.2702702703,
                    456.6486486486
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    443.6756756757,
                    306.1621621622,
                    494.7027027027,
                    355.4594594595
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    57.0810810811,
                    87.3513513514,
                    121.9459459459,
                    152.2162162162
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    345.0810810811,
                    38.0540540541,
                    409.0810810811,
                    90.8108108108
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    534.4864864865,
                    25.0810810811,
                    598.4864864865,
                    80.4324324324
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            }
        ],
        "001_Female_20_Afternoon_Fear_ir_00023.png": [
            {
                "bbox": [
                    427.9884761305,
                    174.7407561883,
                    488.6491367911,
                    264.8308462784
                ],
                "class": "0",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    414.3581791668,
                    168.9629784105,
                    455.2323867077,
                    219.0130284606
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    509.7188731942,
                    402.8802289944,
                    552.0972515726,
                    453.9072560215
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    196.6377921131,
                    173.6910398052,
                    241.6107650861,
                    212.6099587242
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    226.9080623834,
                    318.9883371025,
                    286.583738059,
                    374.3396884539
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    315.1242785996,
                    230.7721208863,
                    373.9350894104,
                    272.2856343998
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    401.2972972973,
                    326.0540540541,
                    438.4864864865,
                    378.8108108108
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    536.2162162162,
                    318.2702702703,
                    583.7837837838,
                    362.3783783784
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    82.1621621622,
                    76.1081081081,
                    162.5945945946,
                    141.8378378378
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            },
            {
                "bbox": [
                    371.027027027,
                    54.4864864865,
                    436.7567567568,
                    113.2972972973
                ],
                "class": "1",
                "bbox_type": "XYWH",
                "scale": 0
            }
        ]
    },
    "msg": "success"
}
```


## 2. modelV_crud
与frontend交互的模块，主要实现数据的增加，查询，计算指标

### a. modelV_task_list
此用户名下的task。按create_time倒序

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/modelV_task_list?task_type={task_type} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| task_type  | String | 是 | 无 | task类型: 0: robustness;1: basic_metrics |
| limit | String | 否  | 100    | 一页数据条数   |
| page  | String | 否  | 1      | 页码     |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| page    | int | 页码   |
| limit   | int | 每页数据条数   |
| total   | int | 数据条数 |
| data    |list  |返回的实际数据 |

注：用户无可用usercase返回空list，其中status: 0: 运行次数为0, 1:运行次数不为0

示例：

请求
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/modelV_task_list?task_type=1' \
--header 'Cookie: csrftoken=epFRaSADBsERVQejK3PPrdO75fGpYQmn36WwA45E91ZeMpF9TCVjcLGB7RFUT4HN; sessionid=45fqqvzlpj3w4hu2gq4zkxr3kjp89px9'
```

响应：
```json
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 100,
        "total": 1,
        "data": [
            {
                "id": 1,
                "model_path": null,
                "data_path": null,
                "algorithm_type": "classification",
                "machine_info": null,
                "token": "af7ea4c0-d773-11ed-83f7-0242ac110002",
                "description": null,
                "table_name_mysql": "prosafeAI_metadata_1",
                "version": 1,
                "init_hyperparameter": null,
                "status": "1",
                "create_time": "04/10/2023 15:58:47",
                "usercase_name": "TSR_Classifier",
                "project_name": "TSR"
            }
        ]
    },
    "msg": "success"
}
```

### b. generate_code
根据task_id，生成token和sample code，计算剩余token次数

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/generate_code?task_id={task_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| task_id | String |是  | 无    | task_id，即当前的task_id   |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明   |
| :---- | :----- | :------- |
| data    |dict  |返回的实际数据 |

示例：

请求:
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/generate_code?task_id=1' \
--header 'Cookie: csrftoken=toMEPta0EzgLBC1pxwnO3ZuxdkOyfAJE4MdNuA2g4p6LFi2Ga05HR7MQEmCd5JV8; sessionid=cpypnms0qgh2pthlb1ynvxk199xdrbol'
```
响应：

```json
{
    "code": 2000,
    "data": {
        "token": "af7ea4c0-d773-11ed-83f7-0242ac110002",
        "code": "bf = BasicMetrics(task_type=basic_metrics, alg_type=classification,\n                                           token=af7ea4c0-d773-11ed-83f7-0242ac110002,\n                                           data_path=None,\n                                           username=superadmin, password='your password')\n                         bf.run('your_prediction.txt')",
        "remaining_times": 9922,
        "hyperparameter": ""
    },
    "msg": "success"
}
```

### c. modelV_run_list
查看某task的历史测试结果(附带task信息)

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/modelV_run_list?task_id={task_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| task_id | String |是  | 无    | task_id，即当前表格的id   |
| limit | String | 否  | 100    | 一页数据条数   |
| page  | String | 否  | 1      | 页码     |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| page    | int | 页码   |
| limit   | int | 每页数据条数   |
| total   | int | 数据条数 |
| data    |list  |返回的实际数据 |

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/modelV_run_list?task_id=1&limit=10' \
--header 'Cookie: csrftoken=4wjDkyrMVLQBSIZXsoZdmGhaD9xnz26EwWbrINpMrXgJM0JtFQJiQZAp9qNL2iBa; sessionid=02kulnhdbrb6fl6gux04l3fx42bz0y9c'
```

响应：

```json
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 10,
        "total": 1,
        "data": [
            {
                "id": 1,
                "task_id": 1,
                "hyperparameter": "",
                "model_path": null,
                "data_path": null,
                "algorithm_type": "classification",
                "machine_info": null,
                "token": "af7ea4c0-d773-11ed-83f7-0242ac110002",
                "description": "basic_metric_t1_v1_classification",
                "table_id": 1,
                "version": 1,
                "start_time": "04/10/2023 08:38:57"
            }
        ]
    },
    "msg": "success"
}
```

### d. quick_modelV_run
用户最近三次的测试结果，按照可用的usercase筛选，start_time倒序。(附带task信息)

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/quick_modelV_run?task_type={task_type} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| task_type  | String | 是 | 无 | task类型: 0: robustness;1: basic_metrics |
| limit | String | 否  | 3    | 一页数据条数   |
| page  | String | 否  | 1      | 页码     |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| page    | int | 页码   |
| limit   | int | 每页数据条数   |
| total   | int | 数据条数 |
| data    |list  |返回的实际数据 |

示例：

请求：

```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/quick_modelV_run?task_type=1' \
--header 'Cookie: csrftoken=4wjDkyrMVLQBSIZXsoZdmGhaD9xnz26EwWbrINpMrXgJM0JtFQJiQZAp9qNL2iBa; sessionid=02kulnhdbrb6fl6gux04l3fx42bz0y9c'
```

响应：

```json
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 3,
        "total": 1,
        "data": [
            {
                "id": 1,
                "task_id": 1,
                "hyperparameter": "",
                "model_path": null,
                "data_path": null,
                "algorithm_type": "classification",
                "machine_info": null,
                "token": "af7ea4c0-d773-11ed-83f7-0242ac110002",
                "description": "basic_metric_t1_v1_classification",
                "table_id": 1,
                "version": 1,
                "start_time": "04/10/2023 08:38:57"
            }
        ]
    },
    "msg": "success"
}
```

### e. create_task
创建新task

#### URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/prosafeai/modelV_crud/create_task/ | POST  |

#### 请求参数

| 参数         | 类型   | 是否必须 | 默认值 | 说明  |
| :---------- | :----- | :----- | :---- |:----|
|table    | String | 是     | 无     | table_id |
|table_version| String | 是     | 无     | table version|
|task_type  | String | 是 | 无 | task类型: 0: robustness;1: basic_metrics |
|model_path  | String | 是     | 无     | 用户输入model绝对路径 |
|data_path    | String | 是     | 无     | 用户输入data绝对路径|
|init_hyperparameter|String|是   |无  |超参数    |
|algorithm_type  | String | 是     | 无 | 算法类型, 0:classification, 1: object detection|
|machine_info     | String | 是     | 无  | 用户输入machine信息|
|description    |String |是  |无  |用户输入task描述     |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回msg为创建成功/失败信息

示例：

请求：classification basic_metrics

```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/create_task/' \
--header 'X-CSRFToken: h6dh3vXfTjarfuvKpkdnMd651d8bBmJz0iyuV5pOu8mS6pdvOLBDu9vhlG8Omgho' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=h6dh3vXfTjarfuvKpkdnMd651d8bBmJz0iyuV5pOu8mS6pdvOLBDu9vhlG8Omgho; sessionid=suv87j9kpxcrve8ea82rtopyk4g8iyzu' \
--data '{
    "table": "1",
    "table_version": "1",
    "task_type": "1",
    "model_path": "/model",
    "data_path": "/data",
    "algorithm_type": "0",
    "machine_info": "HuaWei cloud",
    "description": "test_create_task"
}'
```

响应：
 ```json
{
    "code": 2000,
    "data": {
      "task_id": 14
    },
    "msg": "success"
}
```

请求： classification robustness
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/create_task/' \
--header 'X-CSRFToken: jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H; sessionid=wcu4i3mh13oht3nhm4gkil48qoi8fvi1' \
--data '{
    "table": "1",
    "table_version": "3",
    "task_type": "0",
    "model_path": "/model",
    "data_path": "/data",
    "algorithm_type": "0",
    "init_hyperparameter": {
  "task_type": "classification",
  "dataset_format": "classification",
  "model_framework": "keras",
  "domain": "computer version",
  "device": "cpu",
  "model_type": "white box",
  "mutation_guidance": "NC",
  "mutation_params": {
    "threshold": 0.75,
    "act_fn": [
      "ReLU"
    ]
  },
  "p_min": 0.7,
  "r": 20,
  "alpha": 0.8,
  "beta": 0.8,
  "k_time": 5,
  "try_num": 30,
  "max_iter": 500,
  "batch_size": 8,
  "pixel_level": [
    {
      "method": "mean_blur",
      "parameters": [
        {
          "name": "kernel_size",
          "value": "1,7",
          "dtype": "int"
        }
      ]
    }
  ],
  "semantic_level": [
    {
      "method": "affine",
      "parameters": [
        {
          "name": "pos_1_x",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_1_y",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_2_x",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_2_y",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_3_x",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_3_y",
          "value": "1,10",
          "dtype": "int"
        }
      ]
    }
  ]
},
    "machine_info": "HuaWei cloud",
    "description": "test_create_classification robustness"
}'
```

响应：
```json
{
    "code": 2000,
    "data": {
        "task_id": 74
    },
    "msg": "success"
}
```

请求： object_detection basic_metrics  bbox_type = {"0": "XYX2Y2", "1": "XYWH", "2": "YOLO"}
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/create_task/' \
--header 'X-CSRFToken: jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H; sessionid=wcu4i3mh13oht3nhm4gkil48qoi8fvi1' \
--data '{
    "table": "2",
    "table_version": "3",
    "task_type": "1",
    "model_path": "/model",
    "data_path": "/data",
    "algorithm_type": "1",
    "init_hyperparameter": {"bbox_type": "0", "scale": 0},
    "machine_info": "HuaWei cloud",
    "description": "test_create_object_detection_basic_metrics"
}'
```

响应：
```shell
{
    "code": 2000,
    "data": {
        "task_id": 75
    },
    "msg": "success"
}
```

请求：object_detection robustness  bbox_type = {"0": "XYX2Y2", "1": "XYWH", "2": "YOLO"}
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/create_task/' \
--header 'X-CSRFToken: jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H; sessionid=wcu4i3mh13oht3nhm4gkil48qoi8fvi1' \
--data '{
    "table": 2,
    "table_version": "3",
    "task_type": "0",
    "model_path": "/model",
    "data_path": "/data",
    "algorithm_type": "1",
    "init_hyperparameter": {
  "bbox_type": "0", 
  "scale": 0,
  "task_type": "detection",
  "model_framework": "torch",
  "domain": "computer version",
  "device": "cpu",
  "model_type": "black box",
  "bin_size": 10,
  "pixel_level": [
    {
      "method": "papper_noise",
      "parameters": [
        {
          "name": "ps",
          "value": "0.02,0.1",
          "dtype": "float"
        },
        {
          "name": "pp",
          "value": "0.02,0.1",
          "dtype": "float"
        }
      ]
    }
  ],
  "semantic_level": [
    {
      "method": "affine",
      "parameters": [
        {
          "name": "pos_1_x",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_1_y",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_2_x",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_2_y",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_3_x",
          "value": "1,10",
          "dtype": "int"
        },
        {
          "name": "pos_3_y",
          "value": "1,10",
          "dtype": "int"
        }
      ]
    }
  ],
  "corruption": [
     {
      "method": "add_fog",
      "parameters": [
        {
          "name": "brightness",
          "value": "0.3",
          "dtype": "float"
        },
        {
          "name": "potency",
          "value": "0.4",
          "dtype": "float"
        }
      ]
    } 
  ],
  "input_output_params": {
    "nms_include": 1,
    "letter_box_flag": 1,
    "input_size": {
      "width": 512,
      "height": 512
    },
    "normalize_dict": {
      "std": 1,
      "mean": 0,
      "necessary": 1
    },
    "groundtruth_annnotation_type": "xywh",
    "prediction_annnotation_type": "xywh"
  },
  "iou": 0.5
},
    "machine_info": "HuaWei cloud",
    "description": "test_create_object_detection_robustness"
}'
```


响应：
```shell
{
    "code": 2000,
    "data": {
        "task_id": 72
    },
    "msg": "success"
}
```
`
### f. table_list
table列表，详情看API_list_PI23.1.md中(1.a)接口说明

### g. table_version
version列表，详情看API_list_PI23.1.md中(1.c)接口说明

### h. download_report
下载报告
#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/download_report?run_id={run_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| run_id | String |是  | 无    | run_id，即当前表格的id   |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回pdf报告文件

### i. review_code
根据run_id，查看sample_code
#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/review_code?run_id={run_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| run_id | String |是  | 无    | run_id，即当前表格的id   |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明   |
| :---- | :----- | :------- |
| data    |dict  |返回的实际数据 |

示例：

请求：

```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/review_code?run_id=1' \
--header 'Cookie: csrftoken=h6dh3vXfTjarfuvKpkdnMd651d8bBmJz0iyuV5pOu8mS6pdvOLBDu9vhlG8Omgho; sessionid=suv87j9kpxcrve8ea82rtopyk4g8iyzu'
```

响应：

```json
{
    "code": 2000,
    "data": {
        "code": "bf = BasicMetrics(task_type=basic_metrics, alg_type=classification,\n          token=af7ea4c0-d773-11ed-83f7-0242ac110002,\n          data_path=None,\n          username=superadmin, password='your password')\nbf.run('your_prediction.txt')",
        "hyperparameter": ""
    },
    "msg": "success"
}
```

### j. field_list
odd列表，详情看API_list_PI23.1.md中(1.d)接口说明

[comment]: <> (### k. field_value)

[comment]: <> (某odd的value列表)

[comment]: <> (#### URL)

[comment]: <> (| 协议     | URL                              | 方法 |)

[comment]: <> (| :------- | :------------------------------  | :--- |)

[comment]: <> (| HTTP | api/modelV_crud/field_value?table_id={table_id}&field={field} | GET  |)

[comment]: <> (#### 请求参数)

[comment]: <> (| 参数   | 类型   | 是否必须 | 默认值   | 说明  |)

[comment]: <> (| :---- | :----- | :------- | :---- |:----|)

[comment]: <> (|run_id |String|是 | 无 |run_id |)

[comment]: <> (|field |String|是 | 无 |field的值 |)

[comment]: <> (| limit | String | 否  | 100    | 一页数据条数   |)

[comment]: <> (| page  | String | 否  | 1      | 页码     |)

[comment]: <> (#### 响应结果)

[comment]: <> (* 返回HTTP状态：2000表示成功)

[comment]: <> (* 输出参数：包含在响应的Body中，JSON格式字符串)

[comment]: <> (结果描述：data中包含响应的数据)

[comment]: <> (| 属性     | 类型    | 说明           |)

[comment]: <> (| :------ | :----- | :------------- |)

[comment]: <> (| page    | int | 页码   |)

[comment]: <> (| limit   | int | 每页数据条数   |)

[comment]: <> (| total   | int | 数据条数 |)

[comment]: <> (| data    |dict  |返回的实际数据 |)

### k. view_basic_metrics
查看basic_metrics结果，计算完整数据的各项指标(accuracy, precision, recall, f1score)

#### URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/prosafeai/modelV_crud/view_basic_metrics/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|run_id |String|是 | 无 |run_id， 即当前表格的id |
|iou |float|否 | 0.5 | object detection需要  |
|detail |List|是 | 无 |用户选择要计算的metrics,以及计算方法 |

具体指标可选的计算方法如下：

algorithm_type=classification

|计算指标   |可选计算方法 |默认方法|
|:----|:-----|:----|
|accuracy   |balance, total |balance   |
|precision  |macro, micro, weighted |weighted   |
|recall     |macro, micro, weighted |weighted   |
|f1score    |macro, micro, weighted |weighted   |

algorithm_type=object_detection

|计算指标   |可选计算方法 |默认方法|
|:----|:-----|:----|
|precision  |macro, micro, weighted |weighted   |
|recall     |macro, micro, weighted |weighted   |
|f1score    |macro, micro, weighted |weighted   |
|mAP    |无  |无  |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| data    |List  |返回的实际数据 |


示例：

algorithm_type=classification

请求：

```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_basic_metrics/' \
--header 'X-CSRFToken: MfEzIJRCz5NVqVwGbcrFK3MNbwqP3hPmaXHrDVBYwDFhHRqIKsgRb977IxXGAo7W' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=MfEzIJRCz5NVqVwGbcrFK3MNbwqP3hPmaXHrDVBYwDFhHRqIKsgRb977IxXGAo7W; sessionid=suv87j9kpxcrve8ea82rtopyk4g8iyzu' \
--data '{
    "run_id": 94,
    "detail": [
        {"metrics": "precision", "average": "macro"}, 
        {"metrics": "recall"},
        {"metrics": "accuracy", "average": "balance"}
  ]
}'
```
响应：

```json
{
    "code": 2000,
    "data": [
        {
            "metrics": "precision",
            "average": "macro",
            "value": 0.408
        },
        {
            "metrics": "recall",
            "average": "weighted",
            "value": 0.816
        },
        {
            "metrics": "accuracy",
            "average": "balance",
            "value": 0.5
        },
        {
            "metrics": "matrix",
            "detail": [
                [0, 0, 40],
                [0, 1, 0],
                [1, 0, 9],
                [1, 1, 0]
            ],
            "labels": [
                "class0",
                "class1"
            ]
        }
    ],
    "msg": "success"
}
```

algorithm_type=object_detection

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_basic_metrics/' \
--header 'X-CSRFToken: jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H; sessionid=wcu4i3mh13oht3nhm4gkil48qoi8fvi1' \
--data '{
    "run_id": 190,
    "detail": [
        {"metrics": "precision", "average": "macro"}, 
        {"metrics": "recall"},
        {"metrics": "f1score"},
        {"metrics": "mAP"}
  ],
  "iou": 0.75
}'
```

响应：
```json
{
    "code": 2000,
    "data": [
        {
            "metrics": "precision",
            "average": "macro",
            "value": 0.5
        },
        {
            "metrics": "recall",
            "average": "weighted",
            "value": 0.125
        },
        {
            "metrics": "f1score",
            "average": "weighted",
            "value": 0.135
        },
        {
            "metrics": "mAP",
            "value": 0.511
        }
    ],
    "msg": "success"
}
```

### l. view_slices_basic_metrics
查看slices_basic_metrics结果，计算数据切片的各项指标(accuracy, precision, recall, f1-score)

若单个odd维度进行切片，生成柱状图，选择多个指标，生成多个柱子；

两个odd维度，生成热力图，选择多个指标，生成多个热力图。

#### URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/prosafeai/modelV_crud/view_slices_basic_metrics/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|run_id |int|是 | 无 |run_id， 即当前表格的id |
|metrics |List|是 | 无 |用户选择要计算的metrics |
|iou |float|否 | 0.5 | object detection需要  |
|fields|List|是|无|用户选择odd的切片|
|field_type|String|是|object_detection为必须 |用户选择odd的类型 0：class, 1: odd|


```json
{
  "run_id": 1,
  "detail": [
        {"metrics": "precision", "average": "macro"}, 
        {"metrics": "recall"},
        {"metrics": "accuracy", "average": "balance"}
  ],
  "fields": ["fog intensity", "Snowfall"]
}
```

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| data    |dict  |返回的实际数据 |

如果只选择一个odd，则没有odd2

示例：

请求：

**algorithm_type=classification**

单odd
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_slices_basic_metrics/' \
--header 'X-CSRFToken: qdpqlAGbNnPExKonc4llyvesiMbqAHfGPg4amMeEoFT3z27FA7Oa3LX9bVv5eUEz' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=qdpqlAGbNnPExKonc4llyvesiMbqAHfGPg4amMeEoFT3z27FA7Oa3LX9bVv5eUEz; sessionid=9pg7o5x0vu5ryj28sdhilpze19arpplo' \
--data '{
    "run_id": 9,
    "detail": [
        {"metrics": "precision", "average": "macro"}, 
        {"metrics": "recall"},
        {"metrics": "accuracy", "average": "balance"}
  ],
    "fields": ["Snowfall_intensity"]
}'
```

响应：
```json
{
    "code": 2000,
    "data": [
        {
            "average": "macro",
            "metrics": "precision",
            "detail": [
                {
                    "odd1": "no snow",
                    "value": 0.568
                },
                {
                    "odd1": "light snow",
                    "value": 0.3
                }
            ],
            "values": [
                "no snow",
                "light snow"
            ]
        },
        {
            "average": "weighted",
            "metrics": "recall",
            "detail": [
                {
                    "odd1": "no snow",
                    "value": 0.767
                },
                {
                    "odd1": "light snow",
                    "value": 0.5
                }
            ],
            "values": [
                "no snow",
                "light snow"
            ]
        },
        {
            "average": "balance",
            "metrics": "accuracy",
            "detail": [
                {
                    "odd1": "no snow",
                    "value": 0.586
                },
                {
                    "odd1": "light snow",
                    "value": 0.375
                }
            ],
            "values": [
                "no snow",
                "light snow"
            ]
        },
        {
            "metrics": "matrix",
            "labels": [
                "class0",
                "class1"
            ],
            "detail": [
                {
                    "odd1": "no snow",
                    "detail": [
                        [0, 0, 31],
                        [0, 1, 6],
                        [1, 0, 4],
                        [1, 1, 2]
                    ]
                },
                {
                    "odd1": "light snow",
                    "detail": [
                        [0, 0, 3],
                        [0, 1, 1],
                        [1, 0, 2],
                        [1, 1, 0]
                    ]
                }
            ]
        }
    ],
    "msg": "success"
}
```

请求：双odd
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_slices_basic_metrics/' \
--header 'X-CSRFToken: qdpqlAGbNnPExKonc4llyvesiMbqAHfGPg4amMeEoFT3z27FA7Oa3LX9bVv5eUEz' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=qdpqlAGbNnPExKonc4llyvesiMbqAHfGPg4amMeEoFT3z27FA7Oa3LX9bVv5eUEz; sessionid=9pg7o5x0vu5ryj28sdhilpze19arpplo' \
--data '{
    "run_id": 9,
    "detail": [
        {"metrics": "precision", "average": "macro"}, 
        {"metrics": "recall"},
        {"metrics": "accuracy", "average": "balance"}
  ],
    "fields": ["Snowfall_intensity", "Illuminance"]
}'
```

响应：
```json
{
    "code": 2000,
    "data": [
        {
            "average": "macro",
            "metrics": "precision",
            "detail": [
                {
                    "odd1": "no snow",
                    "odd2": "cloudy",
                    "value": 0.523
                },
                {
                    "odd1": "no snow",
                    "odd2": "sunny",
                    "value": 0.5
                },
                {
                    "odd1": "no snow",
                    "odd2": "partly sunny",
                    "value": 1.0
                },
                {
                    "odd1": "light snow",
                    "odd2": "cloudy",
                    "value": 0.3
                },
                {
                    "odd1": "light snow",
                    "odd2": "sunny",
                    "value": 0
                },
                {
                    "odd1": "light snow",
                    "odd2": "partly sunny",
                    "value": 0
                }
            ],
            "values": {
                "Snowfall_intensity": [
                    "no snow",
                    "light snow"
                ],
                "Illuminance": [
                    "cloudy",
                    "sunny",
                    "partly sunny"
                ]
            }
        },
        {
            "average": "weighted",
            "metrics": "recall",
            "detail": [
                {
                    "odd1": "no snow",
                    "odd2": "cloudy",
                    "value": 0.742
                },
                {
                    "odd1": "no snow",
                    "odd2": "sunny",
                    "value": 0.667
                },
                {
                    "odd1": "no snow",
                    "odd2": "partly sunny",
                    "value": 1.0
                },
                {
                    "odd1": "light snow",
                    "odd2": "cloudy",
                    "value": 0.5
                },
                {
                    "odd1": "light snow",
                    "odd2": "sunny",
                    "value": 0
                },
                {
                    "odd1": "light snow",
                    "odd2": "partly sunny",
                    "value": 0
                }
            ],
            "values": {
                "Snowfall_intensity": [
                    "no snow",
                    "light snow"
                ],
                "Illuminance": [
                    "cloudy",
                    "sunny",
                    "partly sunny"
                ]
            }
        },
        {
            "average": "balance",
            "metrics": "accuracy",
            "detail": [
                {
                    "odd1": "no snow",
                    "odd2": "cloudy",
                    "value": 0.523
                },
                {
                    "odd1": "no snow",
                    "odd2": "sunny",
                    "value": 0.667
                },
                {
                    "odd1": "no snow",
                    "odd2": "partly sunny",
                    "value": 1.0
                },
                {
                    "odd1": "light snow",
                    "odd2": "cloudy",
                    "value": 0.375
                },
                {
                    "odd1": "light snow",
                    "odd2": "sunny",
                    "value": 0
                },
                {
                    "odd1": "light snow",
                    "odd2": "partly sunny",
                    "value": 0
                }
            ],
            "values": {
                "Snowfall_intensity": [
                    "no snow",
                    "light snow"
                ],
                "Illuminance": [
                    "cloudy",
                    "sunny",
                    "partly sunny"
                ]
            }
        },
        {
            "metrics": "matrix",
            "labels": [
                "class0",
                "class1"
            ],
            "detail": [
                {
                    "odd1": "no snow",
                    "odd2": "cloudy",
                    "detail": [
                        [0, 0, 22],
                        [0, 1, 4],
                        [1, 0, 4],
                        [1, 1, 1]
                    ]
                },
                {
                    "odd1": "no snow",
                    "odd2": "sunny",
                    "detail": [
                        [0, 0, 4],
                        [0, 1, 2],
                        [1, 0, 0],
                        [1, 1, 0]
                    ]
                },
                {
                    "odd1": "no snow",
                    "odd2": "partly sunny",
                    "detail": [
                        [0, 0, 5],
                        [0, 1, 0],
                        [1, 0, 0],
                        [1, 1, 1]
                    ]
                },
                {
                    "odd1": "light snow",
                    "odd2": "cloudy",
                    "detail": [
                        [0, 0, 3],
                        [0, 1, 1],
                        [1, 0, 2],
                        [1, 1, 0]
                    ]
                },
                {
                    "odd1": "light snow",
                    "odd2": "sunny",
                    "detail": [
                        []
                    ]
                },
                {
                    "odd1": "light snow",
                    "odd2": "partly sunny",
                    "detail": [
                        []
                    ]
                }
            ]
        }
    ],
    "msg": "success"
}

```

**algorithm_type=object_detection**

请求：odd切片
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_slices_basic_metrics/' \
--header 'X-CSRFToken: jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H; sessionid=wcu4i3mh13oht3nhm4gkil48qoi8fvi1' \
--data '{
    "run_id": 190,
    "detail": [
        {"metrics": "precision", "average": "macro"}, 
        {"metrics": "recall"},
        {"metrics": "mAP"}
  ],
    "fields": ["weather"],
    "field_type": "1"
}'
```

响应：
```json
{
    "code": 2000,
    "data": [
        {
            "average": "macro",
            "metrics": "precision",
            "detail": [
                {
                    "odd1": "cloudy",
                    "value": 0.0
                },
                {
                    "odd1": "sunny",
                    "value": 0.0
                }
            ],
            "values": [
                "cloudy",
                "sunny"
            ]
        },
        {
            "average": "weighted",
            "metrics": "recall",
            "detail": [
                {
                    "odd1": "cloudy",
                    "value": 0.0
                },
                {
                    "odd1": "sunny",
                    "value": 0.0
                }
            ],
            "values": [
                "cloudy",
                "sunny"
            ]
        },
        {
            "average": "",
            "metrics": "mAP",
            "detail": [
                {
                    "odd1": "cloudy",
                    "value": 0.0
                },
                {
                    "odd1": "sunny",
                    "value": 0.0
                }
            ],
            "values": [
                "cloudy",
                "sunny"
            ]
        }
    ],
    "msg": "success"
}
```

请求：class切片

```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_slices_basic_metrics/' \
--header 'X-CSRFToken: jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=jNp16XOLn5nfEAcpr83Hqa2fj0EYleTzz4v4f6lSc12ymMYvLn2sutFe78MGqS2H; sessionid=wcu4i3mh13oht3nhm4gkil48qoi8fvi1' \
--data '{
    "run_id": 190,
    "detail": [
        {"metrics": "precision", "average": "macro"}, 
        {"metrics": "recall"},
        {"metrics": "AP"}  # 注意是AP
  ],
    "fields": ["0"],  # label的idx
    "field_type": "0"
}'
```

响应：
```json
{
    "code": 2000,
    "data": [
        {
            "metrics": "precision",
            "average": "macro",
            "value": 0.75
        },
        {
            "metrics": "recall",
            "average": "weighted",
            "value": 1.0
        },
        {
            "metrics": "AP",
            "average": "",
            "value": 1.0
        },
        {
            "metrics": "PR-curve",
            "detail": {
                "x": [
                    0.0,
                    0.1,
                    0.2,
                    0.3,
                    0.4,
                    0.5,
                    0.6,
                    0.7,
                    0.8,
                    0.9,
                    1.0
                ],
                "y": [
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0
                ]
            }
        }
    ],
    "msg": "success"
}
```

### m. attack_method_info

获取攻击方法详情
#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/attack_method_info?model_type={model_type}&attack_type={attack_type} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| model_type | String |是  | 0    |测试的类型， 0：white, 1: black |
| attack_type | String |是  | 无    |攻击方法类型，0: pixel, 1: semantic, 2: corruption  |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明   |
| :---- | :----- | :------- |
| data    |List  |返回的实际数据 |

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/attack_method_info?model_type=0&attack_type=0' \
--header 'Cookie: csrftoken=cLQHpump7aa7LXafiCVbRBoO1Sjsx44lz23IYBPUngtheVuxmKAPxNYgkLxmcunR; sessionid=4hmubhl9jd7i4w84sh8wyrwq1bdnfxr8'
```

响应：
```json
{
    "code": 2000,
    "data": [
        {
            "method": "brightness",
            "parameter": [
                {
                    "name": "beta",
                    "value": "1,30",
                    "min": 1,
                    "max": 30,
                    "dtype": "int"
                }
            ],
            "description": null
        },
        {
            "method": "contrast",
            "parameter": [
                {
                    "name": "alpha",
                    "value": "0,2",
                    "min": 0,
                    "max": 2,
                    "dtype": "float"
                },
                {
                    "name": "beta",
                    "value": "0,5",
                    "min": 0,
                    "max": 5,
                    "dtype": "float"
                }
            ],
            "description": null
        },
        {
            "method": "papper_noise",
            "parameter": [
                {
                    "name": "ps",
                    "value": "0.02,0.1",
                    "min": 0.02,
                    "max": 0.1,
                    "dtype": "float"
                },
                {
                    "name": "pp",
                    "value": "0.02,0.1",
                    "min": 0.02,
                    "max": 0.1,
                    "dtype": "float"
                }
            ],
            "description": null
        },
        {
            "method": "uniform_noise",
            "parameter": [
                {
                    "name": "mean",
                    "value": "10,50",
                    "min": 10,
                    "max": 50,
                    "dtype": "int"
                },
                {
                    "name": "sigma",
                    "value": "50,150",
                    "min": 50,
                    "max": 150,
                    "dtype": "int"
                }
            ],
            "description": null
        },
        {
            "method": "exponent_noise",
            "parameter": [
                {
                    "name": "a",
                    "value": "5,20",
                    "min": 5,
                    "max": 20,
                    "dtype": "int"
                }
            ],
            "description": null
        },
        {
            "method": "mean_blur",
            "parameter": [
                {
                    "name": "kernel_size",
                    "value": "1,7",
                    "min": 1,
                    "max": 7,
                    "dtype": "int"
                }
            ],
            "description": null
        },
        {
            "method": "gaussian_blur",
            "parameter": [
                {
                    "name": "kernel_size",
                    "value": "1,7",
                    "min": 1,
                    "max": 7,
                    "dtype": "int"
                }
            ],
            "description": null
        },
        {
            "method": "poisson_noise",
            "parameter": [],
            "description": null
        },
        {
            "method": "gaussian_noise",
            "parameter": [
                {
                    "name": "mean",
                    "value": "0,1",
                    "min": 0,
                    "max": 1,
                    "dtype": "float"
                },
                {
                    "name": "sigma",
                    "value": "0,1",
                    "min": 0,
                    "max": 1,
                    "dtype": "float"
                },
                {
                    "name": "ratio",
                    "value": "0,1",
                    "min": 0,
                    "max": 1,
                    "dtype": "float"
                }
            ],
            "description": null
        },
        {
            "method": "FGSM",
            "parameter": [
                {
                    "name": "eps",
                    "value": "0,1",
                    "min": 0,
                    "max": 1,
                    "dtype": "float"
                }
            ],
            "description": null
        },
        {
            "method": "IFGSM",
            "parameter": [
                {
                    "name": "eps",
                    "value": "0,1",
                    "min": 0,
                    "max": 1,
                    "dtype": "float"
                },
                {
                    "name": "iteration_num",
                    "value": "3",
                    "min": 0,
                    "max": "inf",
                    "dtype": "float"
                }
            ],
            "description": null
        }
    ],
    "msg": "success"
}
```

### n. download_hyperparameter

下载超参数的yaml文件
#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/download_hyperparameter?task_id={task_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| task_id | String |是  | 无    | task_id，即当前的task_id   |

结果描述：data中包含响应的数据
* 返回yaml文件

示例：


### o. view_robustness_metrics

查看robustness结果，计算完整数据的各项指标(ASR, distance)

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/view_robustness_metrics/ | POST  |


#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|run_id |String|是 | 无 |run_id， 即当前表格的id |
|detail |List|是 | 无 |用户选择要计算的方面|

```json
{
  "run_id": 3,
  "detail": [
    {
      "aspect": "0", // category
      "choose": ["1", "2"]  // get_run_labels获取的idx
    },
    {
      "aspect": "1", // method
      "choose": ["m1", "m2"]  // get_run_attack_methods获取的method
    },
    {
      "aspect": "2", // distance
      "choose": "l0" // "l0", "l1", "l2", "linf", "ssim"
    }
  ]
}
```

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| data    |List  |返回的实际数据 |

示例：
1. 只选择category/method
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_robustness_metrics/' \
--header 'X-CSRFToken: cLQHpump7aa7LXafiCVbRBoO1Sjsx44lz23IYBPUngtheVuxmKAPxNYgkLxmcunR' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=cLQHpump7aa7LXafiCVbRBoO1Sjsx44lz23IYBPUngtheVuxmKAPxNYgkLxmcunR; sessionid=4hmubhl9jd7i4w84sh8wyrwq1bdnfxr8' \
--data '{
  "run_id": 3,
  "detail": [
    {
      "aspect": "1",
    }
  ]
}'
```
响应：

```json
{
    "code": 2000,
    "data": [
        {
            "slice": "exponent_noise",
            "detail": {
                "attack_samples": 12,
                "attack_success": 9,
                "ASR": 0.75
            }
        },
        {
            "slice": "gaussian_blur",
            "detail": {
                "attack_samples": 14,
                "attack_success": 8,
                "ASR": 0.571
            }
        },
        {
            "slice": "gaussian_noise",
            "detail": {
                "attack_samples": 7,
                "attack_success": 4,
                "ASR": 0.571
            }
        },
        {
            "slice": "vertical_flip",
            "detail": {
                "attack_samples": 9,
                "attack_success": 5,
                "ASR": 0.556
            }
        },
        {
            "slice": "perspective",
            "detail": {
                "attack_samples": 21,
                "attack_success": 11,
                "ASR": 0.524
            }
        },
        {
            "slice": "other",
            "detail": {
                "attack_samples": 137,
                "attack_success": 58
            }
        }
    ],
    "msg": "success"
}
```

2. 选择category + method
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_robustness_metrics/' \
--header 'X-CSRFToken: OnBQ9jcH10c2R17X3H8AZwYgrWSUDdOBgz1sCmZAMJHfzMezCb1pWTmOYIDcWdnc' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=OnBQ9jcH10c2R17X3H8AZwYgrWSUDdOBgz1sCmZAMJHfzMezCb1pWTmOYIDcWdnc; sessionid=r5bqr77vn3ypebboxuzce0rfqe1c4cf6' \
--data '{
  "run_id": 3,
  "detail": [
    {
      "aspect": "1",
      "choose": ["perspective", "rotate_center"]
    },
    {
      "aspect": "0", 
      "choose": ["0", "1"]
    }
  ]
}
```

响应：
```json

{
    "code": 2000,
    "data": [
        {
            "slice": "0*perspective",
            "detail": {
                "attack_success": 0,
                "attack_failed": 10
            }
        },
        {
            "slice": "1*perspective",
            "detail": {
                "attack_success": 11,
                "attack_failed": 0
            }
        },
        {
            "slice": "0*rotate_center",
            "detail": {
                "attack_success": 0,
                "attack_failed": 15
            }
        },
        {
            "slice": "1*rotate_center",
            "detail": {
                "attack_success": 16,
                "attack_failed": 0
            }
        }
    ],
    "msg": "success"
}
```

3. 选择category + distance / method + distance

```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_robustness_metrics/' \
--header 'X-CSRFToken: OnBQ9jcH10c2R17X3H8AZwYgrWSUDdOBgz1sCmZAMJHfzMezCb1pWTmOYIDcWdnc' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=OnBQ9jcH10c2R17X3H8AZwYgrWSUDdOBgz1sCmZAMJHfzMezCb1pWTmOYIDcWdnc; sessionid=r5bqr77vn3ypebboxuzce0rfqe1c4cf6' \
--data '{
  "run_id": 3,
  "detail": [
    {
      "aspect": "1",
      "choose": ["perspective", "rotate_center"]
    },
    {
      "aspect": "2", 
      "choose": "l0"
    }
  ]
}
```
响应：

```json
{
    "code": 2000,
    "data": {
        "x": [
            345.6,
            1036.8,
            1728.0,
            2419.2,
            3110.4,
            3801.6,
            4492.8,
            5184.0,
            5875.2,
            6566.4
        ],
        "detail": [
            {
                "slice": "perspective",
                "detail": [
                    0.524,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            },
            {
                "slice": "rotate_center",
                "detail": [
                    0.516,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            }
        ]
    },
    "msg": "success"
}
```

### p. get_run_labels

获取label列表

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/get_run_labels?run_id={run_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| run_id  | String | 是 | 无 | run_id，即当前表格的id |


#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| data    |List  |返回的实际数据 |

示例：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/get_run_labels?run_id=1' \
--header 'Cookie: csrftoken=cLQHpump7aa7LXafiCVbRBoO1Sjsx44lz23IYBPUngtheVuxmKAPxNYgkLxmcunR; sessionid=4hmubhl9jd7i4w84sh8wyrwq1bdnfxr8'
```

响应：
```json
{
    "code": 2000,
    "data": [
        {
            "idx": "0",
            "category": "class0"
        },
        {
            "idx": "1",
            "category": "class1"
        }
    ],
    "msg": "success"
}
```


### q. get_run_attack_methods

获取attack_method列表

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/get_run_attack_methods?run_id={run_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| run_id  | String | 是 | 无 | run_id，即当前表格的id |


#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| data    |List  |返回的实际数据 |

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/get_run_attack_methods?run_id=3' \
--header 'Cookie: csrftoken=OnBQ9jcH10c2R17X3H8AZwYgrWSUDdOBgz1sCmZAMJHfzMezCb1pWTmOYIDcWdnc; sessionid=r5bqr77vn3ypebboxuzce0rfqe1c4cf6'
```
响应：
```json
{
  "code": 2000,
  "data": [
    {
      "name": "perspective",
      "disable": 1  //不可用
    },
    {
      "name": "rotate_center",
      "disable": 0  //可用
    },
    {
        "name": "affine",
        "disable": 0
    },
    {
        "name": "IFGSM",
        "disable": 0
    }
  ],
  "msg": "success"
}
```

### r. view_attack_sample_info

查看攻击样本详情

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/view_attack_sample_info?run_id={run_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|run_id | String |是  | 无    | run_id，即当前表格的id   |
|method|String |否 | 无| 筛选攻击方法 |
|label|String | 否 |无 |筛选label |
|pred_label|String | 否 |无 |筛选预测label |
|attack_status  |String | 否 |无 |筛选attack_status {"success", "fail"}|
|limit | String | 否  | 100    | 一页数据条数   |
|page  | String | 否  | 1      | 页码     |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| page    | int | 页码   |
| limit   | int | 每页数据条数   |
| total   | int | 数据条数 |
| data    |list  |返回的实际数据 |

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/view_attack_sample_info?run_id=1&limit=3' \
--header 'Cookie: csrftoken=OnBQ9jcH10c2R17X3H8AZwYgrWSUDdOBgz1sCmZAMJHfzMezCb1pWTmOYIDcWdnc; sessionid=r5bqr77vn3ypebboxuzce0rfqe1c4cf6'
```

响应：

```json
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 3,
        "total": 200,
        "data": [
            {
                "ref_path": "/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/data/fewer/1/img_test_1453.png",
                "init_path": "/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/data/fewer/1/img_test_1453.png",
                "state": "0",
                "label": "1",
                "mutated_method": "mean_blur",
                "from_seed_path": "/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/data/fewer/1/img_test_1453.png",
                "l0": "205",
                "l1": "946264",
                "l2": "760.8206096051815",
                "linf": "255",
                "ssim": "0.5949153287120084",
                "pred_label": "0"
            },
            {
                "ref_path": "./hhh/saved/ref-1-1683181820.588256.png",
                "init_path": "/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/data/fewer/1/img_test_1453.png",
                "state": "1",
                "label": "1",
                "mutated_method": "perspective",
                "from_seed_path": "/Users/jingruihan/Desktop/prosafeai-prosafeai-main/prosafeai-prosafeai-main/data/fewer/1/img_test_1453.png",
                "l0": "120",
                "l1": "753850",
                "l2": "791.4758366494835",
                "linf": "255",
                "ssim": "0.24413644320427644",
                "pred_label": "0"
            }
        ]
    },
    "msg": "success"
}
```

### s. download_attack_sample

下载文件
#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/download_attack_sample?run_id={run_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| run_id | String |是  | 无    | run_id，即当前表格的id   |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回文件

### t. mutation_image

获取变异样本

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/mutation_image/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| method | String |否  | 无    | method为变异方法，默认无，返回原始图片   |
| params | Dict |否  | 无    | method的超参数   |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回base64的图片

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/mutation_image/' \
--header 'X-CSRFToken: 4UsxU2ExG1srxLaU6pQiytWpp9k6FbsPRJ1QZEiEBsCXXW4g5ugKHWduRVqrQYYv' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=4UsxU2ExG1srxLaU6pQiytWpp9k6FbsPRJ1QZEiEBsCXXW4g5ugKHWduRVqrQYYv; sessionid=pkqnya1dj6q4wgakmy9nxn75y4zoji7t' \
--data '{
    "method": "affine",
    "params": {
        "pos_1_x": 25,
        "pos_1_y": 5,
        "pos_2_x": 18,
        "pos_2_y": 13,
        "pos_3_x": 18,
        "pos_3_y": 15
    }
}'
```
响应：
```json
{
    "code": 2000,
    "data": {
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAArQAAAQACAIAAACf113UAAAgAElEQVR4AcTB68+l53mf5/O87rV7Z4ZDUSJFSoxJl1IVyLZqJIWdIEHS9luLBIbdpilaoGhRoH9y4X5ogG4Sw5I3IYezW+967uvXZ615KQ75Dt0lUGGPw//0v/7v/uav//r2dHr06NHbbz8eY3Nalu1uv90eZvd2ux1jdPd+v9/tdj/4wQ/++T/7Jx9++OEyc3PzYLfbffrppw8Ou8c3N/3i5XJ73OGYDVqns6PJz6cwi+KIQPHhM2z/Pp8RByxoSEZenWrfde1TXnwsxLhpApJZX8xTdfM04/fvoYotPzXJZFt2ldcM57KURRFoKzeZ6HcZBCMcZDiIWqrA2Pjwc9zOfjGxBCeZ4bY5xzIcauaQilFxcXUsrdbtd1HUIIQmit3Ww2nPNHjx4BAPq+X61WCKHtdj8eT7ebvVJKCME5L4oCIUQpvbu7S5LkfwJSgxFrAtbPswAAAABJRU5ErkJggg=="
    },
    "msg": "success"
} 
```

### o. hyperparamter_template_list
获取hyperparamter_template列表

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/hyperparamter_template_list/ | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| limit | String | 否  | 100    | 一页数据条数   |
| page  | String | 否  | 1      | 页码     |


#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| data    |List  |返回的实际数据 |

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/hyperparamter_template_list' \
--header 'Cookie: csrftoken=4UsxU2ExG1srxLaU6pQiytWpp9k6FbsPRJ1QZEiEBsCXXW4g5ugKHWduRVqrQYYv; sessionid=pkqnya1dj6q4wgakmy9nxn75y4zoji7t'
```
响应：
```json
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 100,
        "total": 1,
        "data": [
            {
                "id": 1,
                "name": "test_llp",
                "content": "{'task_type': 'classification', 'dataset_format': 'classification', 'model_framework': 'keras', 'domain': 'computer version', 'device': 'cpu', 'model_type': 'white box', 'mutation_guidance': 'NC', 'mutation_params': {'threshold': 0.75, 'act_fn': ['ReLU', 'Tanh', 'Sigmoid'], 'model_name': 'test2'}, 'p_min': 0.7, 'r': 20, 'alpha': 0.8, 'beta': 0.8, 'k_time': 5, 'try_num': 30, 'max_iter': 500, 'batch_size': 8, 'pixel_level': [{'method': 'gaussian_blur', 'parameters': [{'name': 'kernel_size', 'value': '1,7', 'dtype': 'int'}]}], 'semantic_level': [{'method': 'perspective', 'parameters': [{'name': 'pos_1_x', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_1_y', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_2_x', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_2_y', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_3_x', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_3_y', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_4_x', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_4_y', 'value': '1,10', 'dtype': 'int'}]}]}",
                "description": "test_llp",
                "create_time": "2023-07-13T17:59:55",
                "user_id": 1
            }
        ]
    },
    "msg": "success"
}
```

### p. save_hyperparamter_template

保存hyperparamter_template

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/save_hyperparamter_template/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|init_hyperparameter    |String |是  |无  |用户设置的超参数|
|template_name  |String   |是    |无  |模板名字|  
|template_description   |String    |是   |无  |模板描述|


#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| data    |List  |返回的实际数据 |

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/save_hyperparamter_template/' \
--header 'X-CSRFToken: 4UsxU2ExG1srxLaU6pQiytWpp9k6FbsPRJ1QZEiEBsCXXW4g5ugKHWduRVqrQYYv' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=4UsxU2ExG1srxLaU6pQiytWpp9k6FbsPRJ1QZEiEBsCXXW4g5ugKHWduRVqrQYYv; sessionid=pkqnya1dj6q4wgakmy9nxn75y4zoji7t' \
--data '{
    "init_hyperparameter": "{'task_type': 'classification', 'dataset_format': 'classification', 'model_framework': 'keras', 'domain': 'computer version', 'device': 'cpu', 'model_type': 'white box', 'mutation_guidance': 'NC', 'mutation_params': {'threshold': 0.75, 'act_fn': ['ReLU', 'Tanh', 'Sigmoid'], 'model_name': 'test2'}, 'p_min': 0.7, 'r': 20, 'alpha': 0.8, 'beta': 0.8, 'k_time': 5, 'try_num': 30, 'max_iter': 500, 'batch_size': 8, 'pixel_level': [{'method': 'gaussian_blur', 'parameters': [{'name': 'kernel_size', 'value': '1,7', 'dtype': 'int'}]}], 'semantic_level': [{'method': 'perspective', 'parameters': [{'name': 'pos_1_x', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_1_y', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_2_x', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_2_y', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_3_x', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_3_y', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_4_x', 'value': '1,10', 'dtype': 'int'}, {'name': 'pos_4_y', 'value': '1,10', 'dtype': 'int'}]}]}",,
    "template_name": "test_llp",
    "template_description": "test_llp"
}'
```

响应：
```json
{
    "code": 2000,
    "data": {
        "id": 5
    },
    "msg": "success"
}
```

### q. delete_hyperparamter_template

删除hyperparamter_template

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/modelV_crud/delete_hyperparamter_template/ | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| id | String | 否  | 无    | template id   |


#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：
返回删除状态： success/failed

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/modelV_crud/delete_hyperparamter_template?id=2' \
--header 'Cookie: csrftoken=4UsxU2ExG1srxLaU6pQiytWpp9k6FbsPRJ1QZEiEBsCXXW4g5ugKHWduRVqrQYYv; sessionid=pkqnya1dj6q4wgakmy9nxn75y4zoji7t'
```

响应：
```json
{
    "code": 2000,
    "data": null,
    "msg": "success"
}
```