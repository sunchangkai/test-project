# ProsafeAI API List PI23.1

开发环境后端地址：http://10.38.49.30:8000/

用户名：superadmin 密码：admin123456 (拥有所有权限)

用户名：admin 密码：admin123456 (管理员权限)

用户名：liping 密码：admin123456 (普通用户)

## 1. data_management

数据管理模块，主要实现数据预览，数据导入功能


### a. 获取table_list

#### URL

| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/prosafeai_tables/ | GET  |


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
| page    | int | 页码   |
| limit   | int | 每页数据条数   |
| total   | int | 数据条数 |
| data    |dict  |返回的实际数据(用户无可用usercase返回空list) 注：其中task_type表示metadata的任务类型，0：classification，1：object detection|



示例：

请求
```shell
http://10.38.49.30:8000/api/prosafeai/prosafeai_tables
```

响应
```shell
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 100,
        "total": 2,
        "data": [
            {
                "id": 1,
                "table_description": "TSR meta data ",
                "table_name_mysql": "prosafeAI_metadata_1",
                "odd_version": "v10.0",
                "usercase_id": 1,
                "table_type": "metadata",
                "parent_id": null,
                "project_name": "TSR",
                "usercase_name": "TSR_Classifier",
                "latest_version": 3,
                "fields": [
                    "image_name",
                    "image_format",
                    "augmentation",
                    "dataset",
                    "dataset_type",
                    "class",
                    "Fog_intensity",
                    "Snowfall_intensity",
                    "Illuminance",
                    "Rain_quantity"
                ],
                "object_num": 0,
                "task_type": 0
            },
            {
                "id": 2,
                "table_description": "TSR",
                "table_name_mysql": "prosafeAI_metadata_2",
                "odd_version": "v1.0",
                "usercase_id": 1,
                "table_type": "metadata",
                "parent_id": null,
                "project_name": "TSR",
                "usercase_name": "TSR_Classifier",
                "latest_version": 1,
                "fields": [],
                "object_num": 0,
                "task_type": 0
            }
        ]
    },
    "msg": "success"
}
```


注：当前用户是superadmin，返回所有tables; 当前用户有可用usercase，则返回可用tables; 当前用户无可用usercase，则返回空list.

### b. 获取table_details

#### URL

| 协议     | URL                              | 方法 |
| :------- | :------------------------------  | :--- |
| HTTP | api/prosafeai/table_details?table_id={table_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|table_id |String|是 | 无 |table_id |
|version  |String|否 |latest_version| data version|
|search_param|String |否 | 无| 查询参数 |
|search_content|String | 否 |无 |查询文本 |
|search_type|String |否  | 0| 查询类型：0：精准匹配 1：模糊匹配|
| limit | String | 否  | 100    | 一页数据条数  |
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
| data    |dict  |返回的实际数据 |

示例:
```shell
http://10.38.49.30:8000/api/prosafeai/table_details?table_id=3&limit=3&search_param=car_model&search_content=ID4&search_type=1
```
响应
```shell
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 3,
        "total": 2,
        "data": [
            {
                "id": 1,
                "image_name": "image1.png",
                "description": "MIK emotion dataset",
                "version": "1",
                "camera_type": "0",
                "image_path": "xxx",
                "image_size": "{\"width\":222,\"height\":999}",
                "car_model": "ID4",
                "image_type": "IR",
                "timestamp": "YYYYMMDDHHMMSS",
                "weather": "sunny",
                "location": "outdoor",
                "so_driver": "0",
                "so_co_driver": "-1",
                "so_second_row_left": "-1",
                "so_second_row_center": "-1",
                "so_second_row_rigiht": "-1",
                "labels": "{face，}",
                "data_version": 1,
                "object_num": 3
            },
            {
                "id": 2,
                "image_name": "image2.png",
                "description": "MIK emotion dataset",
                "version": "1",
                "camera_type": "0",
                "image_path": "xxx",
                "image_size": "{\"width\":222,\"height\":999}",
                "car_model": "ID4",
                "image_type": "IR",
                "timestamp": "YYYYMMDDHHMMSS",
                "weather": "sunny",
                "location": "outdoor",
                "so_driver": "0",
                "so_co_driver": "-1",
                "so_second_row_left": "-1",
                "so_second_row_center": "-1",
                "so_second_row_rigiht": "-1",
                "labels": "{face，}",
                "data_version": 1,
                "object_num": 0
            }
        ]
    },
    "msg": "success"
}
```


### c. 获取version_info

#### URL

| 协议     | URL                              | 方法 |
| :------- | :------------------------------  | :--- |
| HTTP | api/prosafeai/version_info?table_id={table_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|table_id |String|是 | 无 |table_id |
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
| data    |dict  |返回的实际数据 |

示例:

请求
```shell
http://10.38.49.30:8000/api/prosafeai/version_info?table_id=1&limit=10
```
响应
```shell
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 10,
        "total": 3,
        "data": [
            {
                "version": 1,
                "description": "init_version",
                "create_time": "2023-02-15T14:35:43"
            },
            {
                "version": 2,
                "description": "new_version",
                "create_time": "2023-02-15T14:35:52"
            },
            {
                "version": 3,
                "description": "test",
                "create_time": "2023-02-15T16:24:45"
            }
        ]
    },
    "msg": "success"
}
```

### d. 获取table_field_info
#### URL

| 协议     | URL                              | 方法 |
| :------- | :------------------------------  | :--- |
| HTTP | api/prosafeai/table_field_info?table_id={table_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|table_id |String|是 | 无 |table_id |
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
| data    |dict  |返回的实际数据 |

示例：

请求
```shell
http://10.38.49.30:8000/api/prosafeai/table_field_info?table_id=1&limit=30
```
响应
```shell
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 30,
        "total": 10,
        "data": [
            {
                "field_name": "image_name"
            },
            {
                "field_name": "image_format"
            },
            {
                "field_name": "augmentation"
            },
            {
                "field_name": "dataset"
            },
            {
                "field_name": "dataset_type"
            },
            {
                "field_name": "class"
            },
            {
                "field_name": "Fog_intensity"
            },
            {
                "field_name": "Snowfall_intensity"
            },
            {
                "field_name": "Illuminance"
            },
            {
                "field_name": "Rain_quantity"
            }
        ]
    },
    "msg": "success"
}
```

### e. 获取object_tag_details
#### URL

| 协议     | URL                              | 方法 |
| :------- | :------------------------------  | :--- |
| HTTP | api/prosafeai/object_tag_details?table_id={table_id}&version={version}&sample_id={sample_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|table_id |String|是 | 无 |table_id |
|version  |String|是 |无 | data version|
|sample_id|String|是 |无 | sample id|
| limit | String | 否  | 100 | 一页数据条数  |
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
| data    |dict  |返回的实际数据 |

示例:

请求
```shell
http://10.38.49.30:8000/api/prosafeai/object_tag_details?table_id=3&version=3&sample_id=15
```

响应
```shell
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 100,
        "total": 11,
        "data": [
            {
                "object_id": 138,
                "object_class": "face",
                "object_code": "000001",
                "object_tag": [
                    {
                        "feature": "person_id",
                        "content": "000001"
                    },
                    {
                        "feature": "bbox",
                        "content": "[434.3094445751, 172.2897858103, 495.203672136, 265.2994621533]"
                    },
                    {
                        "feature": "type",
                        "content": "0"
                    },
                    {
                        "feature": "face_direction",
                        "content": "1"
                    },
                    {
                        "feature": "arousal_level",
                        "content": "1"
                    },
                    {
                        "feature": "face_covered",
                        "content": "0"
                    },
                    {
                        "feature": "use_emotion",
                        "content": "0"
                    }
                ]
            },
            {
                "object_id": 139,
                "object_class": "no face",
                "object_code": "000001",
                "object_tag": [
                    {
                        "feature": "person_id",
                        "content": "000001"
                    },
                    {
                        "feature": "bbox",
                        "content": "[44.1081081081, 115.8918918919, 75.2432432432, 152.2162162162]"
                    },
                    {
                        "feature": "type",
                        "content": ""
                    },
                    {
                        "feature": "face_direction",
                        "content": "0"
                    },
                    {
                        "feature": "arousal_level",
                        "content": "0"
                    },
                    {
                        "feature": "face_covered",
                        "content": "0"
                    },
                    {
                        "feature": "use_emotion",
                        "content": "0"
                    }
                ]
            }
        ]
    },
    "msg": "success"
}
```
### f. 导出json模板
#### URL

| 协议     | URL                              | 方法 |
| :------- | :------------------------------  | :--- |
| HTTP | api/prosafeai/data_management/import_data?table_id={table_id} | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|table_id |String|是 | 无 |table_id |

#### 响应结果
* 返回HTTP状态：200表示成功
* 返回json模板文件

结果描述：

返回json模板文件

示例:
```shell
http://10.38.49.30:8000/api/prosafeai/data_management/import_data?table_id=3
```

响应：response.body为json文件，其内容为：
```shell
[
    {
        "image_name": "string",
        "description": "string",
        "version": "string",
        "camera_type": "string",
        "image_path": "string",
        "image_size": "string",
        "car_model": "string",
        "image_type": "string",
        "timestamp": "datetime",
        "weather": "string",
        "location": "string",
        "so_driver": "string",
        "so_co_driver": "string",
        "so_second_row_left": "string",
        "so_second_row_center": "string",
        "so_second_row_rigiht": "string",
        "labels": "string",
        "objects": [
            {
                "object_class": "string",
                "tag": {}
            }
        ]
    }
]
```

### g. 导入数据

在执行导入数据时，需要进行两个接口的调用。

- 1. 调用http://10.38.49.30:8000/api/system/file/
- 2. 调用http://10.38.49.30:8000/api/prosafeai/data_management/import_data/

    
URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/system/file/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|file |file文件|是 | 无 |需要上传的文件 |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回file的详情

结果描述：data中包含返回的数据体

**特别需要关注的是data中的url,是调用第二个接口的请求参数**

示例：

请求
```shell
curl --location --request POST 'http://10.38.49.30:8000/api/system/file/' \
--header 'X-CSRFToken: 4tkYM5yfsBf6j7DAOVWBaiGm5WeT93uSwEeMwwAME9p19ByiIorE6j4AkvulFzLv' \
--header 'Cookie: csrftoken=4tkYM5yfsBf6j7DAOVWBaiGm5WeT93uSwEeMwwAME9p19ByiIorE6j4AkvulFzLv; sessionid=dtc3hnirbnv450degdzrq1sjac3doy2l' \
--form 'file=@"/home/format_data.json"'
```

响应：
```shell
{
    "code": 2000,
    "data": {
        "id": 20,
        "modifier_name": "超级管理员",
        "creator_name": "超级管理员",
        "create_datetime": "2023-02-23 19:07:19",
        "update_datetime": "2023-02-23 19:07:19",
        "url": "media/files/9/5/9576d196589ab998c037f9eb30f422f5.json",
        "description": null,
        "modifier": "1",
        "dept_belong_id": "1",
        "name": "format_data.json",
        "md5sum": "9576d196589ab998c037f9eb30f422f5",
        "creator": 1
    },
    "msg": "新增成功"
}
```

然后调用第二个接口

#### URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/prosafeai/data_management/import_data/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|table_id |String|是 | 无 |需要导入的table_id |
|version_comments|String|是|无|用户输入的版本说明|
|url    |String|是|无|调用上一个接口返回的url|
|label_file  | File | 是 |  |标签映射关系文件 |

label_file sample:
0 car
1 bus
2 person
3 bike
4 truck
5 motor
6 train
7 rider


#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回msg为导入成功/失败信息

示例：

请求：
```shell
curl --location 'http://10.38.49.30:8000/api/prosafeai/data_management/import_data/' \
--header 'X-CSRFToken: VtZKRlaRMO2rG1jsTRut5oCPy9NRNbALXBj4sJBDJF9be7Ziyp7fvQRA5yFujrsX' \
--header 'Cookie: csrftoken=VtZKRlaRMO2rG1jsTRut5oCPy9NRNbALXBj4sJBDJF9be7Ziyp7fvQRA5yFujrsX; sessionid=f2lg13ffaieusjl1th4uqo194mke1c8t' \
--form 'table_id="13"' \
--form 'version_comments="bdd100k_data_liulp_2023-11-29"' \
--form 'url="media/files/9/2/9245896d55d11dbdeb1f1087fd17e731_ctVC1nD.json"' \
--form 'label_file=@"/home/liu/PycharmProjects/VW/prosafeai-prosafeai-main/research/bdd100k/class.txt"'
```

响应
```shell
{
    "code": 2000,
    "data": null,
    "msg": "import success"
}

```

## 2. data_display

数据展示模块，主要实现数据统计，用于前端可视化

### a. 获取统计详情

#### URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/prosafeai/data_display/data_statistics/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|table_id |String|是 | 无 |需要统计的table_id |
|table_name |String|是 | 无 |需要统计的table_name |
|count_type |String|是  |0 | 统计目标，0:sample_num,1:object_num|
|fields|List    |是  |无  |至少有一个odd的列表    |
|versions |List |否  |latest_version |data_version的列表|


#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

示例：

请求
```shell
curl --location --request POST 'http://10.38.49.30:8000/api/prosafeai/data_display/data_statistics/' \
--header 'X-CSRFToken: 4tkYM5yfsBf6j7DAOVWBaiGm5WeT93uSwEeMwwAME9p19ByiIorE6j4AkvulFzLv' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=4tkYM5yfsBf6j7DAOVWBaiGm5WeT93uSwEeMwwAME9p19ByiIorE6j4AkvulFzLv; sessionid=dtc3hnirbnv450degdzrq1sjac3doy2l' \
--data-raw '{
    "table_id": 3,
    "table_name": "prosafeAI_metadata_3",
    "count_type": 1,
    "fields": ["weather", "location"],
    "versions": [4,5,6]
}'
```

响应
```shell
{
    "code": 2000,
    "data": [
        {
            "odd_name": "weather",
            "detail": [
                {
                    "data_version": 4,
                    "odd_value": "cloudy",
                    "count": 10
                },
                {
                    "data_version": 5,
                    "odd_value": "cloudy",
                    "count": 10
                },
                {
                    "data_version": 6,
                    "odd_value": "cloudy",
                    "count": 8
                },
                {
                    "data_version": 6,
                    "odd_value": "windy",
                    "count": 36
                }
            ]
        },
        {
            "odd_name": "location",
            "detail": [
                {
                    "data_version": 4,
                    "odd_value": "Car-park",
                    "count": 10
                },
                {
                    "data_version": 5,
                    "odd_value": "Car-park",
                    "count": 10
                },
                {
                    "data_version": 6,
                    "odd_value": "Car-park",
                    "count": 44
                }
            ]
        }
    ],
    "msg": "success"
}
```


## 3. data_verification

数据展示模块，主要实现数据统计，用于前端可视化

### a. 获取task 表格

#### URL
| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/task_list/ | GET  |


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
| page    | int | 页码   |
| limit   | int | 每页数据条数   |
| total   | int | 数据条数 |
| data    |dict  |返回的实际数据(用户无可用usercase返回空list) |

示例：

请求
```shell
http://10.38.49.30:8000/api/prosafeai/task_list
```

响应
```shell
{
    "code": 2000,
    "data": 
    {
        "page": 1,
        "limit": 100,
        "total": 1,
        "data": [
            {
                "id": 1,
                "task_name": "Data-TSRClassifier",
                "table_description": "TSR meta data ",
                "version": 1,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 1,
                "create_time": "03-01-2023 17:40:17"
            }
        ]
    },
    "msg": "success"
}
```

### b. 获取sub_task 表格

#### URL
| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/result_list/ | GET  |

id

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
| id    | String | 是  | 无     |需要导入的task_id |
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
| data    | dict|返回的实际数据(用户无可用usercase返回空list) |

示例：
请求
```shell
http://10.38.49.30:8000/api/prosafeai/result_list
```
响应
```shell
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 100,
        "total": 18,
        "data": [
            {
                "id": 1,
                "task_name": "Data-TSRClassifier",
                "table_description": "TSR meta data ",
                "version": 1,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 1,
                "create_time": "03/01/2023 17:40:17"
            },
            {
                "id": 28,
                "task_name": "`111",
                "table_description": "TSR meta data ",
                "version": 5,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 1,
                "create_time": "03/01/2023 17:40:17"
            },
            {
                "id": 29,
                "task_name": "`111",
                "table_description": "TSR meta data ",
                "version": 5,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 1,
                "create_time": "03/01/2023 17:40:17"
            },
            {
                "id": 36,
                "task_name": "11",
                "table_description": "TSR meta data ",
                "version": 3,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 15,
                "create_time": "03/09/2023 16:38:44"
            },
            {
                "id": 37,
                "task_name": "123456",
                "table_description": "TSR meta data ",
                "version": 3,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 1,
                "create_time": "03/01/2023 17:40:17"
            },
            {
                "id": 38,
                "task_name": "12345",
                "table_description": "TSR meta data ",
                "version": 7,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 16,
                "create_time": "03/09/2023 16:53:29"
            },
            {
                "id": 39,
                "task_name": "111",
                "table_description": "TSR meta data ",
                "version": 3,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 17,
                "create_time": "03/09/2023 16:55:42"
            },
            {
                "id": 41,
                "task_name": "11",
                "table_description": "TSR meta data ",
                "version": 1,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 19,
                "create_time": "03/09/2023 17:15:20"
            },
            {
                "id": 42,
                "task_name": "6666",
                "table_description": "TSR meta data ",
                "version": 1,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 16,
                "create_time": "03/09/2023 16:53:29"
            },
            {
                "id": 43,
                "task_name": "Data-TSRClassifier_update",
                "table_description": "TSR meta data ",
                "version": 1,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": "DONE",
                "requirements_id": 20,
                "create_time": "03/10/2023 06:56:36"
            },
            {
                "id": 40,
                "task_name": "123456",
                "table_description": "TSR",
                "version": 1,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 18,
                "create_time": "03/09/2023 16:59:25"
            },
            {
                "id": 27,
                "task_name": "Data-TSRClassifier-I",
                "table_description": "MIK",
                "version": 2,
                "requirements": "Data-TSRClassifier-1",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 12,
                "create_time": "03/08/2023 08:03:31"
            },
            {
                "id": 30,
                "task_name": "Data-TSRClassifier-I",
                "table_description": "MIK",
                "version": 2,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 13,
                "create_time": "03/09/2023 08:22:48"
            },
            {
                "id": 31,
                "task_name": "Data-TSRClassifier-I",
                "table_description": "MIK",
                "version": 2,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 1,
                "create_time": "03/01/2023 17:40:17"
            },
            {
                "id": 32,
                "task_name": "Data-TSRClassifier-I",
                "table_description": "MIK",
                "version": 2,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 1,
                "create_time": "03/01/2023 17:40:17"
            },
            {
                "id": 33,
                "task_name": "Data-TSRClassifier-I",
                "table_description": "MIK",
                "version": 2,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 14,
                "create_time": "03/09/2023 16:24:32"
            },
            {
                "id": 34,
                "task_name": "111",
                "table_description": "MIK",
                "version": 5,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 1,
                "create_time": "03/01/2023 17:40:17"
            },
            {
                "id": 35,
                "task_name": "111",
                "table_description": "MIK",
                "version": 5,
                "requirements": "Data-TSRClassifier",
                "test_begin_time": null,
                "test_end_time": null,
                "status": null,
                "requirements_id": 1,
                "create_time": "03/01/2023 17:40:17"
            }
        ]
    },
    "msg": "success"
}
```

### c. 获取requirements list
#### URL
| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/requirements_list/ | GET  |


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
| page    | int | 页码   |
| limit   | int | 每页数据条数   |
| total   | int | 数据条数 |
| data    |dict  |返回的实际数据(用户无可用usercase返回空list) |

示例：
请求
```shell
http://10.38.49.30:8000/api/prosafeai/requirements_list
```
响应
```shell
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 100,
        "total": 10,
        "data": [
            {
                "id": 20,
                "name": "Data-TSRClassifier",
                "create_time": "03/10/2023 06:56:36"
            },
            {
                "id": 19,
                "name": "Data-TSRClassifier",
                "create_time": "03/09/2023 17:15:20"
            },
            {
                "id": 18,
                "name": "Data-TSRClassifier",
                "create_time": "03/09/2023 16:59:25"
            },
            {
                "id": 17,
                "name": "Data-TSRClassifier",
                "create_time": "03/09/2023 16:55:42"
            },
            {
                "id": 16,
                "name": "Data-TSRClassifier",
                "create_time": "03/09/2023 16:53:29"
            },
            {
                "id": 15,
                "name": "Data-TSRClassifier",
                "create_time": "03/09/2023 16:38:44"
            },
            {
                "id": 14,
                "name": "Data-TSRClassifier",
                "create_time": "03/09/2023 16:24:32"
            },
            {
                "id": 13,
                "name": "Data-TSRClassifier",
                "create_time": "03/09/2023 08:22:48"
            },
            {
                "id": 12,
                "name": "Data-TSRClassifier-1",
                "create_time": "03/08/2023 08:03:31"
            },
            {
                "id": 1,
                "name": "Data-TSRClassifier",
                "create_time": "03/01/2023 17:40:17"
            }
        ]
    },
    "msg": "success"
}
```

### d. 获取sub_requirements details
#### URL
| 协议     | URL                             | 方法 |
| :------- | :------------------------------ | :--- |
| HTTP | api/prosafeai/sub_requirements/ | GET  |


#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :----- | :---- |:----|
| id    | String | 是     | 无     |需要导入的requirements_id |
| limit | String | 否     | 100    | 一页数据条数   |
| page  | String | 否     | 1      | 页码     |


#### 响应结果
* 返回HTTP状态：2000表示成功
* 输出参数：包含在响应的Body中，JSON格式字符串

结果描述：data中包含响应的数据

| 属性     | 类型    | 说明           |
| :------ | :----- | :------------- |
| page    | int | 页码   |
| limit   | int | 每页数据条数   |
| total   | int | 数据条数 |
| data    | dict |返回的实际数据(用户无可用usercase返回空list) |

示例：
请求
```shell
http://10.38.49.30:8000/api/prosafeai/sub_requirements
```
响应
```shell
{
    "code": 2000,
    "data": 
    {
        "page": 1,
        "limit": 100,
        "total": 29,
        "data": [
            {
                "rule_id": "552060081315418547",
                "rule_name": "data-tsr-1",
                "classification": "consistency",
                "verification_object": "class label",
                "verification_content": "taxonomy",
                "computation_rule": "{\"property\": \"distinguishable by visual characteristics\"}"
            },
            {
                "rule_id": "552060081315418638",
                "rule_name": "data-tsr-3",
                "classification": "consistency",
                "verification_object": "bounding box",
                "verification_content": "object count",
                "computation_rule": "{\"operator\": \"=\", \"threshold\": 1, \"detection_object\": \"traffic sign\"}"
            },
            {
                "rule_id": "552060081315418725",
                "rule_name": "data-tsr-4",
                "classification": "consistency",
                "verification_object": "bounding box",
                "verification_content": "visibility",
                "computation_rule": "{\"metric\": \"total visibility\", \"operator\": \">=\", \"threshold\": 50, \"detection_object\": \"construction area sign\"}"
            },
            {
                "rule_id": "552060081315418826",
                "rule_name": "data-tsr-5",
                "classification": "consistency",
                "verification_object": "bounding box",
                "verification_content": "visibility",
                "computation_rule": "{\"metric\": \"total visibility\", \"operator\": \">=\", \"threshold\": 70, \"detection_object\": \"speed limit sign\"}"
            },
            {
                "rule_id": "552060081315418970",
                "rule_name": "data-tsr-6",
                "classification": "consistency",
                "verification_object": "image",
                "verification_content": "perspective",
                "computation_rule": "{\"position\": \"front camera\"}"
            },
            {
                "rule_id": "552060081315419054",
                "rule_name": "data-tsr-7",
                "classification": "consistency",
                "verification_object": "image",
                "verification_content": "quality",
                "computation_rule": "{\"metric\": \"distortion\", \"operator\": \">\", \"threshold\": 10, \"action\": \"visual inspection\"}"
            },
            {
                "rule_id": "552060081315419192",
                "rule_name": "data-tsr-8",
                "classification": "consistency",
                "verification_object": "image",
                "verification_content": "quality",
                "computation_rule": "{\"metric\": \"brightness\", \"operator\": \">\", \"threshold\": 10, \"action\": \"visual inspection\"}"
            },
            {
                "rule_id": "552060081315419361",
                "rule_name": "data-tsr-9",
                "classification": "consistency",
                "verification_object": "image",
                "verification_content": "quality",
                "computation_rule": "{\"metric\": \"blurriness\", \"operator\": \">\", \"threshold\": 10, \"action\": \"visual inspection\"}"
            },
            {
                "rule_id": "552060081315419527",
                "rule_name": "data-tsr-10",
                "classification": "consistency",
                "verification_object": "image",
                "verification_content": "quality",
                "computation_rule": "{\"metric\": \"contrast\", \"operator\": \">\", \"threshold\": 10, \"action\": \"visual inspection\"}"
            },
            {
                "rule_id": "552060081315419708",
                "rule_name": "data-tsr-11",
                "classification": "consistency",
                "verification_object": "image",
                "verification_content": "quality",
                "computation_rule": "{\"metric\": \"saturation\", \"operator\": \"<\", \"threshold\": 10, \"action\": \"visual inspection\"}"
            },
            {
                "rule_id": "552060081315419904",
                "rule_name": "data-tsr-12a",
                "classification": "accuracy",
                "verification_object": "image",
                "verification_content": "annotation",
                "computation_rule": "{\"information\": \"class label\"}"
            },
            {
                "rule_id": "552060081315420098",
                "rule_name": "data-tsr-12b",
                "classification": "accuracy",
                "verification_object": "image",
                "verification_content": "annotation",
                "computation_rule": "{\"information\": \"bounding box\"}"
            },
            {
                "rule_id": "552060081315420275",
                "rule_name": "data-tsr-13",
                "classification": "accuracy",
                "verification_object": "meta data",
                "verification_content": "schema",
                "computation_rule": "{\"information\": \"general description\"}"
            },
            {
                "rule_id": "552060081315420482",
                "rule_name": "data-tsr-14",
                "classification": "accuracy",
                "verification_object": "meta data",
                "verification_content": "schema",
                "computation_rule": "{\"information\": \"detection method\"}"
            },
            {
                "rule_id": "552060081315420696",
                "rule_name": "data-tsr-15",
                "classification": "accuracy",
                "verification_object": "image",
                "verification_content": "annotation",
                "computation_rule": "{\"information\": \"meta data\"}"
            },
            {
                "rule_id": "552060081315420941",
                "rule_name": "data-tsr-16",
                "classification": "accuracy",
                "verification_object": "meta data",
                "verification_content": "odd information",
                "computation_rule": "{\"odd_parameter\": \"Rain quantity\", \"info_type\": \"categorical\", \"metric\": \"set cardinality\", \"operator\": \">=\", \"threshold\": 2}"
            },
            {
                "rule_id": "552060081315439123",
                "rule_name": "data-tsr-17a",
                "classification": "accuracy",
                "verification_object": "meta data",
                "verification_content": "odd information",
                "computation_rule": "{\"odd_parameter\": \"Road type\"}"
            },
            {
                "rule_id": "552060081316200891",
                "rule_name": "data-tsr-17b",
                "classification": "accuracy",
                "verification_object": "meta data",
                "verification_content": "odd information",
                "computation_rule": "{\"odd_parameter\": \"Regions or states\"}"
            },
            {
                "rule_id": "552060081315433929",
                "rule_name": "data-tsr-19",
                "classification": "accuracy",
                "verification_object": "meta data",
                "verification_content": "mapping",
                "computation_rule": "{\"from\": \"odd\", \"to\": \"meta_data\", \"odd_parameter\": \"Rain quantity\", \"mapping_property\": \"surjective\"}"
            },
            {
                "rule_id": "552060081315434195",
                "rule_name": "data-tsr-20",
                "classification": "accuracy",
                "verification_object": "bounding box",
                "verification_content": "deviation",
                "computation_rule": "{\"metric\": \"maximal deviation\", \"operator\": \"<\", \"threshold\": 5, \"detection_object\": \"traffic sign\"}"
            },
            {
                "rule_id": "552060081315434768",
                "rule_name": "data-tsr-21",
                "classification": "representativeness",
                "verification_object": "dataset",
                "verification_content": "distribution",
                "computation_rule": "{\"odd_parameter\": \"Rain quantity\", \"statistical_distribution\": [{\"odd_class\": \"no rain\", \"probability\": 0.64}, {\"odd_class\": \"light rain\", \"probability\": 0.22}, {\"odd_class\": \"moderate rain\", \"probability\": 0.08}, {\"odd_class\": \"heavy rain\", \"probability\": 0.04}, {\"odd_class\": \"violent rain\", \"probability\": 0.019}, {\"odd_class\": \"cloud burst\", \"probability\": 0.001}], \"statistical_test\": \"Chi Square Test\", \"significance\": 0.05}"
            },
            {
                "rule_id": "552060081315435432",
                "rule_name": "data-tsr-23",
                "classification": "representativeness",
                "verification_object": "dataset",
                "verification_content": "parameter coverage",
                "computation_rule": "{\"odd_parameter\": \"Rain quantity\"}"
            },
            {
                "rule_id": "552060081315435821",
                "rule_name": "data-tsr-24",
                "classification": "representativeness",
                "verification_object": "dataset",
                "verification_content": "parameter coverage",
                "computation_rule": "{\"odd_parameter\": \"Regions or states\"}"
            },
            {
                "rule_id": "552060081315436150",
                "rule_name": "data-tsr-25",
                "classification": "representativeness",
                "verification_object": "dataset",
                "verification_content": "parameter coverage",
                "computation_rule": "{\"odd_parameter\": \"Road type\"}"
            },
            {
                "rule_id": "7528772871778298172",
                "rule_name": "data-tsr-26a",
                "classification": "accuracy",
                "verification_object": "class label",
                "verification_content": "specification",
                "computation_rule": "{\"detection_object\": \"traffic sign\", \"odd_parameters\": [{\"name\": \"Construction area signs\"}, {\"name\": \"Speed limit signs\"}]}"
            },
            {
                "rule_id": "552060081315436513",
                "rule_name": "data-tsr-26b",
                "classification": "representativeness",
                "verification_object": "dataset",
                "verification_content": "label balance",
                "computation_rule": "{\"property\": \"balanced data\"}"
            },
            {
                "rule_id": "552060081315437264",
                "rule_name": "data-tsr-28",
                "classification": "representativeness",
                "verification_object": "dataset",
                "verification_content": "scenario coverage",
                "computation_rule": "{\"metric\": \"count\", \"operator\": \">=\", \"threshold\": 100, \"scenario\": [{\"odd_parameter\": \"Rain quantity\", \"odd_class\": \"light rain\"}, {\"odd_parameter\": \"Illuminance\", \"odd_class\": \"overcast night\"}]}"
            },
            {
                "rule_id": "552060081315438086",
                "rule_name": "data-tsr-30",
                "classification": "representativeness",
                "verification_object": "dataset",
                "verification_content": "scenario coverage",
                "computation_rule": "{\"metric\": \"count\", \"operator\": \">=\", \"threshold\": 10, \"scenario\": [{\"odd_parameter\": \"Rain quantity\", \"odd_class\": \"cloud burst\"}, {\"odd_parameter\": \"Illuminance\", \"odd_class\": \"overcast night\"}]}"
            },
            {
                "rule_id": "552060081315438672",
                "rule_name": "data-tsr-31",
                "classification": "representativeness",
                "verification_object": "dataset",
                "verification_content": "amount",
                "computation_rule": "{\"metric\": \"total amount\", \"operator\": \">=\", \"threshold\": 5000}"
            }
        ]
    },
    "msg": "success"
}
```

### e. 导出requirements 模版
#### URL

| 协议     | URL                              | 方法 |
| :------- | :------------------------------  | :--- |
| HTTP | api/prosafeai/data_verification/import_task | GET  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|


#### 响应结果
* 返回HTTP状态：200表示成功
* 返回json模板文件

结果描述：

返回json模板文件

示例:
```shell
http://10.38.49.30:8000/api/prosafeai/data_verification/import_task
```

响应：response.body为json文件，其内容为：
```shell
[
    {
        "requirements_catalog": {
            "name": "string",
            "id": "string",
            "requirements": [
                {
                    "name": "string",
                    "id": "string",
                    "type": "string",
                    "classification": "string",
                    "export": "string",
                    "description": {
                        "verification_object": "string",
                        "verification_content": "string",
                        "computation_rule": {}
                    }
                }
            ]
        }
    }
]
```

### f. 导入 data_requirements.json 并创建task

在执行导入数据时，需要进行两个接口的调用。

- 1. 调用http://10.38.49.30:8000/api/system/file/
- 2. 调用http://10.38.49.30:8000/api/prosafeai/data_verification/import_task/

    
URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/system/file/ | POST  |

#### 请求参数

| 参数   | 类型   | 是否必须 | 默认值   | 说明  |
| :---- | :----- | :------- | :---- |:----|
|file |file文件|是 | 无 |需要上传的文件 |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回file的详情

结果描述：data中包含返回的数据体

**特别需要关注的是data中的url,是调用第二个接口的请求参数**

示例：

请求
```shell
curl --location --request POST 'http://10.38.49.30:8000/api/system/file/' \
--header 'X-CSRFToken: ouJjEnBgNBTOhJiqTgD0ulcQVu9IgrPxW2d7uxMLwer2t9C952kvp4DZ8bRznrFr' \
--header 'Cookie: csrftoken=ouJjEnBgNBTOhJiqTgD0ulcQVu9IgrPxW2d7uxMLwer2t9C952kvp4DZ8bRznrFr; sessionid=pizki94vnqoh98zm6cbx7hyr9as5flsq' \
--form 'file=@"/home/Data-TSRClassifier.json"'
```

响应：
```shell
{
    "code": 2000,
    "data": 
    {
        "id": 65,
        "modifier_name": "超级管理员",
        "creator_name": "超级管理员",
        "create_datetime": "2023-03-08 01:58:35",
        "update_datetime": "2023-03-08 01:58:35",
        "url": "media/files/f/3/f36bb48c49fd2da56a3d92e8fdfdef18_V1B8H88.json",
        "description": null,
        "modifier": "1",
        "dept_belong_id": "1",
        "name": "Data-TSRClassifier.json",
        "md5sum": "f36bb48c49fd2da56a3d92e8fdfdef18",
        "creator": 1,
    },
    "msg": "新增成功"
}
```

然后调用第二个接口

#### URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/prosafeai/data_management/import_task/ | POST  |

#### 请求参数

| 参数         | 类型   | 是否必须 | 默认值 | 说明  |
| :---------- | :----- | :----- | :---- |:----|
|table        | String | 是     | 无     | 需要导入的table_id |
|table_version| String | 是     | 无     | 用户输入的table version|
|requirement  | String | 是     | 无     | 用户输入的requirement id|
|task_name    | String | 是     | 无     | 用户输入的task名称或描述|
|json_url     | String | 是     | 无     | 调用上一个接口返回的url|


#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回msg为导入成功/失败信息

示例：

请求：
```shell
curl --location --request POST 'http://10.38.49.30:8000/api/prosafeai/data_verification/import_task/' \
--header 'X-CSRFToken: ouJjEnBgNBTOhJiqTgD0ulcQVu9IgrPxW2d7uxMLwer2t9C952kvp4DZ8bRznrFr' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ouJjEnBgNBTOhJiqTgD0ulcQVu9IgrPxW2d7uxMLwer2t9C952kvp4DZ8bRznrFr; sessionid=pizki94vnqoh98zm6cbx7hyr9as5flsq' \
--data-raw '{
    "table": 3,
    "table_version": 2,
    "requirement": -1,
    "task_name": "Data-TSRClassifier-I",
    "json_url": "media/files/f/3/f36bb48c49fd2da56a3d92e8fdfdef18_V1B8H88.json"
}'
```

响应
```shell
{
    "code": 2000,
    "data": null,
    "msg": "import task success"
}

```

### g. run all test for a task
#### URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/prosafeai/data_verification/run_verification/ | POST  |

#### 请求参数

| 参数         | 类型   | 是否必须 | 默认值 | 说明  |
| :---------- | :----- | :----- | :---- |:----|
|task_id      | String | 是     | 无     | 需要导入的task_id |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回msg为导入成功/失败信息

请求：
```shell
curl --location --request POST 'http://10.38.49.30:8000/api/prosafeai/data_verification/run_verification/' \
--header 'X-CSRFToken: ouJjEnBgNBTOhJiqTgD0ulcQVu9IgrPxW2d7uxMLwer2t9C952kvp4DZ8bRznrFr' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ouJjEnBgNBTOhJiqTgD0ulcQVu9IgrPxW2d7uxMLwer2t9C952kvp4DZ8bRznrFr; sessionid=pizki94vnqoh98zm6cbx7hyr9as5flsq' \
--data-raw '{
    "task_id": "43"
}'
```


响应
```shell
{
    "code": 2000,
    "data": null,
    "msg": "data verification success"
}

```

### h. run subtask 
#### URL

| 协议     | URL         | 方法 |
| :------- | :--------  | :--- |
| HTTP | api/prosafeai/data_verification/run_for_subtask/ | POST  |

#### 请求参数

| 参数         | 类型   | 是否必须 | 默认值 | 说明  |
| :---------- | :----- | :----- | :---- |:----|
|subtask_id      | String | 是     | 无     | 需要导入的subtask_id |

#### 响应结果
* 返回HTTP状态：2000表示成功
* 返回msg为导入成功/失败信息

请求：
```shell
curl --location --request POST 'http://10.38.49.30:8000/api/prosafeai/data_verification/run_for_subtask/' \
--header 'X-CSRFToken: ouJjEnBgNBTOhJiqTgD0ulcQVu9IgrPxW2d7uxMLwer2t9C952kvp4DZ8bRznrFr' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ouJjEnBgNBTOhJiqTgD0ulcQVu9IgrPxW2d7uxMLwer2t9C952kvp4DZ8bRznrFr; sessionid=pizki94vnqoh98zm6cbx7hyr9as5flsq' \
--data-raw '{
    "subtask_id": "580"
}'
```

响应
```shell
{
    "code": 2000,
    "data": null,
    "msg": "subtask success"
}

```

### i. export results.pdf 

| 协议     | URL         | 方法 | 
| :------- | :--------  | :--- | 
| HTTP | api/prosafeai/export_report/?task_id={task_id} | GET |


#### 请求参数
| 参数         | 类型   | 是否必须 | 默认值 | 说明  |
| :---------- | :----- | :----- | :---- |:----|
|task_id      | String | 是     | 无     | 需要导入的task_id |

#### 响应结果
* 返回HTTP状态：200表示成功
* 返回pdf报告文件


结果描述：

返回pdf报告文件

示例:
```shell
http://10.38.49.30:8000/api/prosafeai/export_report/?task_id=43
```

响应：response.body为pdf文件，其内容为：
```shell

```