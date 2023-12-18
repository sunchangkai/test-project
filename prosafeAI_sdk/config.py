# -*- coding: utf-8 -*-
"""
@Time ： 10/4/2023 4:25 pm
@Auth ： Jingrui Han
@File ：config.py.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""

# BASEADDR = "http://123.249.71.254:8000"
BASEADDR = 'http://10.38.49.30:8000'

ADDRS = {
    "create_run": f"{BASEADDR}/api/prosafeai/modelV_sdk/create_run/",
    "check_metadata": f"{BASEADDR}/api/prosafeai/modelV_sdk/check_metadata/",
    "save_phased_results": f"{BASEADDR}/api/prosafeai/modelV_sdk/save_phased_results/",
    "save_results": f"{BASEADDR}/api/prosafeai/modelV_sdk/save_results/",
    "login": f"{BASEADDR}/apiLogin/",
    "system_file": f"{BASEADDR}/api/system/file/",
    "import_metadata": f"{BASEADDR}/api/prosafeai/data_management/import_data/",
    "create_data_verification": f"{BASEADDR}/api/prosafeai/data_verification/import_task/",
    "run_data_verification": f"{BASEADDR}/api/prosafeai/data_verification/run_verification/",
    "download_data_verification_report": f"{BASEADDR}/api/prosafeai/export_report/",
}
SUPPORTIMAGE_FORMAT = ["bmp", "jpg", "jpeg", "png", "tif", "tiff", "dng", "webp", "mpo"]
