# -*- coding: utf-8 -*-
# @Time    : 2023/1/12 下午5:50
# @Author  : liuliping
# @File    : models.py
# @description:

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from dvadmin.utils.models import CoreModel, table_prefix


class ProsafeAIProject(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    project_manager = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_project"
        verbose_name = "prosafeAI_project"


class ProsafeAIUsercase(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(
        "ProsafeAIProject", models.CASCADE, blank=True, null=True
    )
    model_tasktype = models.CharField(max_length=255, blank=True, null=True)
    model_framework = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    developer = models.CharField(max_length=255, blank=True, null=True)
    # task_type = models.CharField(max_length=255, blank=True, null=True)
    # model = models.ForeignKey("ProsafeAIRobustnessModelInfo", models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_usercase"
        verbose_name = "prosafeAI_usercase"


class ProsafeAITable(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    usercase = models.ForeignKey(
        "ProsafeAIUsercase", models.CASCADE, blank=True, null=True
    )
    table_description = models.CharField(max_length=255, blank=True, null=True)
    table_name_mysql = models.CharField(max_length=255, blank=True, null=True)
    # version = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey("ProsafeAITable", models.CASCADE, blank=True, null=True)
    table_type = models.CharField(max_length=255, blank=True, null=True)
    odd_version = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_table"
        verbose_name = "prosafeAI_table"


class ProsafeAIOdd(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey("ProsafeAIOdd", models.CASCADE, blank=True, null=True)
    odd_version = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_odd"
        verbose_name = "prosafeAI_odd"


class ProsafeAIField(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    table = models.ForeignKey("ProsafeAITable", models.CASCADE, blank=True, null=True)
    field_name = models.CharField(max_length=255, blank=True, null=True)
    field_type = models.CharField(max_length=255, blank=True, null=True)
    field_category = models.CharField(max_length=255, blank=True, null=True)
    field_data_securty_level = models.CharField(max_length=255, blank=True, null=True)
    txt_field_name = models.CharField(max_length=255, blank=True, null=True)
    odd = models.ForeignKey("ProsafeAIOdd", models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_field"
        verbose_name = "prosafeAI_field"


class ProsafeAIFieldValueInfo(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    table = models.ForeignKey("ProsafeAITable", models.CASCADE, blank=True, null=True)
    field = models.ForeignKey("ProsafeAIField", models.CASCADE, blank=True, null=True)
    field_name = models.CharField(max_length=255, blank=True, null=True)
    field_value = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_field_value_info"
        verbose_name = "prosafeAI_field_value_info"


class ProsafeAIVersion(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    table = models.ForeignKey("ProsafeAITable", models.CASCADE, blank=True, null=True)
    # row_id = models.IntegerField(default=1, blank=True, null=True)
    version = models.IntegerField(default=1, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    label_map = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "prosafeAI_version"
        verbose_name = "prosafeAI_version"


class ProsafeAIDataRequirements(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    usercase = models.ForeignKey(
        "ProsafeAIUsercase", models.CASCADE, blank=True, null=True
    )
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "prosafeAI_data_requirements"
        verbose_name = "prosafeAI_data_requirements"


class ProsafeAIDataSubRequirements(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    requirements = models.ForeignKey(
        "ProsafeAIDataRequirements", models.CASCADE, blank=True, null=True
    )
    rule_id = models.CharField(max_length=255, blank=True, null=True)
    rule_name = models.CharField(max_length=255, blank=True, null=True)
    classification = models.CharField(max_length=255, blank=True, null=True)
    verification_object = models.CharField(max_length=255, blank=True, null=True)
    verification_content = models.CharField(max_length=255, blank=True, null=True)
    computation_rule = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "prosafeAI_data_sub_requirements"
        verbose_name = "prosafeAI_data_sub_requirements"


class ProsafeAIDataVerificationTask(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    task_name = models.CharField(max_length=255, blank=True, null=True)
    table = models.ForeignKey("ProsafeAITable", models.CASCADE, blank=True, null=True)
    version = models.IntegerField(default=1, blank=True, null=True)
    requirements = models.ForeignKey(
        "ProsafeAIDataRequirements", models.CASCADE, blank=True, null=True
    )
    test_begin_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    test_end_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_data_verification_task"
        verbose_name = "prosafeAI_data_verification_task"


class ProsafeAIDataVerificationResult(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    task = models.ForeignKey(
        "ProsafeAIDataVerificationTask", models.CASCADE, blank=True, null=True
    )
    table = models.ForeignKey("ProsafeAITable", models.CASCADE, blank=True, null=True)
    version = models.IntegerField(default=1, blank=True, null=True)
    requirements = models.ForeignKey(
        "ProsafeAIDataRequirements", models.CASCADE, blank=True, null=True
    )
    sub_requirements = models.ForeignKey(
        "ProsafeAIDataSubRequirements", models.CASCADE, blank=True, null=True
    )
    test_result = models.CharField(max_length=255, blank=True, null=True)
    result_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_data_verification_result"
        verbose_name = "prosafeAI_data_verification_result"


class ProsafeAIModelVTask(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    usercase = models.ForeignKey(
        "ProsafeAIUsercase", models.CASCADE, blank=True, null=True
    )
    model_path = models.CharField(max_length=255, blank=True, null=True)
    data_path = models.CharField(max_length=255, blank=True, null=True)
    task_type = models.CharField(max_length=255, blank=True, null=True)
    init_hyperparameter = models.TextField(null=True, blank=True)
    machine_info = models.CharField(max_length=255, blank=True, null=True)
    table = models.ForeignKey("ProsafeAITable", models.CASCADE, blank=True, null=True)
    version = models.IntegerField(default=1, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    algorithm_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_modelV_task"
        verbose_name = "prosafeAI_modelV_task"


class ProsafeAIModelVTokenRecharge(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    task = models.ForeignKey(
        "ProsafeAIModelVTask", models.CASCADE, blank=True, null=True
    )
    recharge_quantity = models.IntegerField(default=1, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    total_quantity = models.IntegerField(default=1, blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_modelV_token_recharge"
        verbose_name = "prosafeAI_modelV_token_recharge"


class ProsafeAIModelVCheckReport(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    task = models.ForeignKey(
        "ProsafeAIModelVTask", models.CASCADE, blank=True, null=True
    )
    run = models.ForeignKey("ProsafeAIModelVRun", models.CASCADE, blank=True, null=True)
    report_path = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "prosafeAI_modelV_check_report"
        verbose_name = "prosafeAI_modelV_check_report"


class ProsafeAIModelVRun(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    task = models.ForeignKey(
        "ProsafeAIModelVTask", models.CASCADE, blank=True, null=True
    )
    task_type = models.CharField(max_length=255, blank=True, null=True)
    hyperparameter = models.TextField(null=True, blank=True)
    result_path = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    end_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    celery_result = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "prosafeAI_modelV_run"
        verbose_name = "prosafeAI_modelV_run"


class ProsafeAIModelVStep(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    task = models.ForeignKey(
        "ProsafeAIModelVTask", models.CASCADE, blank=True, null=True
    )
    run = models.ForeignKey("ProsafeAIModelVRun", models.CASCADE, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    iteration = models.IntegerField(default=1, blank=True, null=True)
    fail_test_num = models.IntegerField(default=1, blank=True, null=True)
    total_mutator = models.IntegerField(default=1, blank=True, null=True)
    ASR = models.FloatField(default=0, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "prosafeAI_modelV_step"
        verbose_name = "prosafeAI_modelV_step"


class ProsafeAIIModelVAttackMethod(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    method = models.CharField(max_length=255, blank=True, null=True)
    attack_type = models.CharField(max_length=255, blank=True, null=True)
    support_model = models.CharField(max_length=255, blank=True, null=True)
    parameter = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "prosafeAI_modelV_attack_method"
        verbose_name = "prosafeAI_modelV_attack_method"
