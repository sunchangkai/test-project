<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      add-title="New Task"
      @goHistoryList="goHistoryList"
      @showCode="showCode"
      @detailDialog="detailDialog"
      crud.options.tableType="vxe-table"
      @cell-data-change="handleCellDataChange"
    >
      <div slot="header">
        <div style="margin: 20px;"></div>
        <el-button type="success" size="medium" @click="createTask">
          <i class="el-icon-plus" /> New Task
        </el-button>
        <crud-toolbar
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
        <div style="margin: 20px;"></div>
      </div>
    </d2-crud-x>

    <el-dialog title="Task Detail" :visible.sync="dialogVisible" width="40%">
      <div>
        <p class="dialog_grey_line"></p>

        <div style="margin: 20px;">
          <div class="dialog-left-title">
            <p class="ptitle">Model Path:</p>
            <p class="pcontent">{{ modelPath }}</p>
          </div>
          <div class="dialog-left-title">
            <p class="ptitle">Data Path:</p>
            <p class="pcontent">{{ dataPath }}</p>
          </div>
          <div class="dialog-left-title">
            <p class="ptitle">Machine Info:</p>
            <p class="pcontent">{{ machineInfo }}</p>
          </div>
          <div class="dialog-left-title">
            <p class="ptitle">Task Description:</p>
            <p class="pcontent">{{ taskDesc }}</p>
          </div>
          <div class="dialog-left-title">
            <p class="ptitle">Create time:</p>
            <p class="pcontent">{{ createTime }}</p>
          </div>
        </div>
        <p class="dialog_grey_line"></p>
      </div>
      <div slot="footer">
        <el-button type="success" @click="dialogVisible = false" size="small">OK</el-button>
      </div>
    </el-dialog>

    <el-dialog title="Sample code" :visible.sync="scDialogVisible" width="60%">
      <div>
        <p class="dialog_grey_line"></p>
        <div style="padding: 20px">
          <div class="dialog-left-title">
            <i class="el-icon-info" style="margin-right: 2px"></i>
            <div class="ptitle">Token:</div>
            <div class="pcontent">{{ tokenStr }}</div>
          </div>

          <div class="dialog-left-title">
            <p class="ptitle">Remaining times:</p>
            <p class="pcontent">{{ remainingTimes }}</p>
          </div>

          <div>
            <p class="ptitle">User Guide:</p>
          </div>
          <p style="margin: 5px 0 10px 0;font-size:16px;">
            Step1: Install the SDK to your IDE by "pip install xxxx.whl"
          </p>
          <div class="step2-container">
            <div class="step2">
              <pre class="text">{{ codeSingleLine }}</pre>
              <el-button class="copy-btn" type="primary" @click="copyCode" size="small"
                >Copy</el-button
              >
            </div>
          </div>

          <p style="font-size: 12px;color: #999;margin-top: 5px;">
            Note: Please copy the sample code to your IDE and run the task
          </p>
        </div>
      </div>
    </el-dialog>
    <el-dialog title="Warning" :visible.sync="notVerifyDialogVisible" width="30%">
      <p class="dialog_grey_line"></p>
      <div class="dialog-body-style">
        <p class="ptitle">This table has not been verificated,</p>
        <p class="ptitle">please go data verification first,</p>
        <p class="ptitle">thanks</p>
      </div>
      <p class="dialog_grey_line"></p>
      <div slot="footer">
        <el-button type="warning" @click="notVerifyDialogVisible = false" style="width: 70px"
          >OK</el-button
        >
      </div>
    </el-dialog>

    <el-dialog title="New Task" :visible.sync="createDVisible" width="40%">
      <p class="dialog_grey_line"></p>
      <div style="padding: 20px;">
        <el-form
          :model="createForm"
          :rules="rules"
          ref="createFormRef"
          label-width="150px"
          label-position="left"
          :disabled="formDisabled"
        >
          <!--   你可能好奇为啥又套了一层，因为如果用户选择的表为other，会禁用下面所有的下拉框和输入框。实现这个功能需要单独给这个下拉框套一个form      -->
          <el-form
            :model="createFormSub"
            :rules="rulesSub"
            ref="createFormSubRef"
            label-width="150px"
            label-position="left"
          >
            <el-form-item label="Table Name:" prop="tableNameValue">
              <el-select
                class="select-filter"
                v-model="createFormSub.tableNameValue"
                size="medium"
                placeholder="please select table name"
                @change="handleTableChange"
              >
                <el-option
                  v-for="item in tableArr"
                  :key="item.label"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-form>

          <el-form-item label="Table Version:" prop="tableVersionValue">
            <el-select
              class="select-filter"
              v-model="createForm.tableVersionValue"
              size="medium"
              placeholder="please select table version"
            >
              <el-option
                v-for="item in versionArr"
                :key="item.version"
                :label="item.version + ' (' + item.description + ')'"
                :value="item.version"
              ></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="Alg Type:" prop="algTypeValue">
            <el-select
              class="select-filter"
              v-model="createForm.algTypeValue"
              size="medium"
              placeholder="please select algorithm type"
              clearable
            >
              <el-option
                v-for="item in algArr"
                :key="item.label"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>

          <el-form-item
            v-if="createForm.algTypeValue === '1'"
            label="Bounding box type:"
            prop="init_hyperparameter.bbox_type"
          >
            <el-select
              class="select-filter"
              v-model="createForm.init_hyperparameter.bbox_type"
              placeholder="please select bounding box type"
            >
              <el-option
                v-for="item in bboxType"
                :key="item.label"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>

          <el-form-item
            v-if="createForm.algTypeValue === '1'"
            label="Is the output scaled:"
            prop="init_hyperparameter.scale"
          >
            <el-select v-model="createForm.init_hyperparameter.scale">
              <el-option
                v-for="item in scaleType"
                :key="item.label"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="Model Path:" prop="addModelPath">
            <el-input
              style="width: 350px"
              v-model="createForm.addModelPath"
              placeholder="please enter an absolute path"
            ></el-input>
          </el-form-item>

          <el-form-item label="Data Path:" prop="addDataPath">
            <el-input
              style="width: 350px"
              v-model="createForm.addDataPath"
              placeholder="please enter an absolute path"
            ></el-input>
          </el-form-item>

          <el-form-item label="Machine Info:" prop="addMachineInfo">
            <el-input style="width: 350px" v-model="createForm.addMachineInfo"></el-input>
          </el-form-item>

          <el-form-item label="Task Description:" prop="addTaskDesc">
            <el-input
              type="textarea"
              style="width: 350px"
              v-model="createForm.addTaskDesc"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>

      <p class="dialog_grey_line"></p>

      <div slot="footer">
        <el-button
          type="success"
          @click="submitForm('createFormRef', 'createFormSubRef')"
          style="width: 100px"
          >Create</el-button
        >
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';

export default {
  name: 'bmTaskList',
  mixins: [d2CrudPlus.crud],

  data() {
    return {
      formDisabled: false,

      createFormSub: {
        tableNameValue: '',
      },
      rulesSub: {
        tableNameValue: [
          { required: true, message: 'please select table name', trigger: 'change' },
        ],
      },
      createForm: {
        tableVersionValue: '',
        algTypeValue: '',
        addModelPath: '',
        addDataPath: '',
        addMachineInfo: '',
        addTaskDesc: '',
        init_hyperparameter: {
          bbox_type: '0',
          scale: 1,
        },
      },
      rules: {
        tableVersionValue: [
          { required: true, message: 'please select table version', trigger: 'change' },
        ],
        algTypeValue: [
          { required: true, message: 'Please select algorithm type', trigger: 'change' },
        ],
        addModelPath: [
          { required: true, message: 'please enter an absolute path', trigger: 'blur' },
        ],
        addDataPath: [
          { required: true, message: 'please enter an absolute path', trigger: 'blur' },
        ],
        addMachineInfo: [{ required: true, message: 'please enter machine info', trigger: 'blur' }],
        addTaskDesc: [
          { required: true, message: 'please enter task description', trigger: 'blur' },
        ],
      },
      algArr: [
        { value: '0', label: 'Classfication' },
        { value: '1', label: 'Object Detection' },
      ],
      bboxType: [
        { value: '0', label: '(X1, Y1, X2, Y2)' },
        { value: '1', label: '(X1, Y1, W, H)' },
        { value: '2', label: '(Xcenter, Ycenter, W, H)' },
      ],
      scaleType: [
        { value: 0, label: 'No' },
        { value: 1, label: 'Yes' },
      ],
      tableArr: [],
      versionArr: [],
      hyperParas: [],
      createDVisible: false,
      notVerifyDialogVisible: false,
      scDialogVisible: false,
      dialogVisible: false,
      tokenStr: '',
      remainingTimes: 0,
      sampleCodeStr: [],
      hyperParas2: '',
      codeSingleLine: '',

      modelPath: '',
      dataPath: '',
      machineInfo: '',
      taskDesc: '',
      algType: '',
      createTime: '',
    };
  },
  mounted() {
    this.getTableNames();
  },

  watch: {},

  methods: {
    createTask() {
      this.createDVisible = true;
      this.getTableNames();
    },
    /**
     * 监听切换table
     */
    handleTableChange(val) {
      if (val === -1) {
        this.formDisabled = true;
        this.noTableTip();
      } else {
        this.formDisabled = false;
        this.getVersion(val);
      }
    },
    /**
     * form表单提交
     */
    submitForm(formName, formNameSub) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.addTask();
        } else {
          return false;
        }
      });

      this.$refs[formNameSub].validate(valid => {
        if (!valid) {
        }
      });
    },

    resetForm(formName, formNameSub) {
      this.$refs.createFormRef.resetFields();
      this.$refs.createFormSubRef.resetFields();
    },
    /**
     * 创建Task
     */
    addTask() {
      const that = this;
      const requestBody = {
        table: this.createFormSub.tableNameValue,
        table_version: this.createForm.tableVersionValue,
        task_type: '1',
        model_path: this.createForm.addModelPath,
        data_path: this.createForm.addDataPath,
        algorithm_type: this.createForm.algTypeValue,
        machine_info: this.createForm.addMachineInfo,
        description: this.createForm.addTaskDesc,
        init_hyperparameter: JSON.stringify(this.createForm.init_hyperparameter),
      };
      api.createTask(requestBody).then(ret => {
        this.$message({
          message: 'create successful!',
          type: 'success',
        });
        this.doRefresh();

        that.createDVisible = false;
        that.resetForm('createFormRef', 'createFormSubRef');
        that.createForm.addMachineInfo = '';
        that.createForm.addTaskDesc = '';
      });
    },

    /**
     * 获取版本列表
     */
    getSampleCode(scope) {
      const that = this;
      that.tokenStr = '';
      that.codeSingleLine = '';
      that.remainingTimes = 0;
      const query = {};
      query.task_id = scope.row.id;
      api.GetSampleCode(query).then(ret => {
        that.tokenStr = ret.data.token;
        that.codeSingleLine = ret.data.code;
        that.remainingTimes = ret.data.remaining_times;
      });
    },
    /**
     * 获取所有表格列表
     */
    getTableNames() {
      const that = this;
      this.tableArr = [];
      api.GetTableList().then(ret => {
        for (const item of ret.data.data) {
          that.tableArr.push({ value: item.id, label: item.table_name_mysql });
        }
        this.tableArr.push({ value: '-1', label: 'other' });
      });
    },
    /**
     * 获取版本列表
     */
    getVersion(tableId) {
      const that = this;
      const query = {};
      query.table_id = tableId;
      that.versionArr = [];
      return api.GetVersion(query).then(
        function(ret) {
          for (const item of ret.data.data) {
            that.versionArr.push(item);
          }
        },
        function(ret) {},
      );
    },
    /**
     * 没有表跳转到Data Manager page
     */
    noTableTip() {
      const that = this;
      this.$confirm('Please import your matedata in Data Management', 'Tip', {
        confirmButtonText: 'Skip to',
        cancelButtonText: 'Cancel',
        type: 'info',
        center: true,
      })
        .then(() => {
          that.goDataManagement();
        })
        .catch(() => {});
    },

    handleCellDataChange({ rowIndex, key, value, row }) {},
    /**
     * 复制文本到剪切板中
     */
    copyCode() {
      const textarea = document.createElement('textarea');
      textarea.readOnly = 'readonly';
      textarea.style.position = 'absolute';
      textarea.style.left = '-9999px';
      textarea.value = this.codeSingleLine;
      document.body.appendChild(textarea);
      textarea.select();
      textarea.setSelectionRange(0, textarea.value.length);
      document.execCommand('Copy');
      document.body.removeChild(textarea);
      this.$message({
        message: 'Copy successful',
        type: 'success',
      });
    },

    getCrudOptions() {
      return crudOptions(this);
    },

    pageRequest(query) {
      // task类型: 0: robustness;1: basic_metrics
      query.task_type = 1;
      return api.GetTaskList(query).then(ret => {
        if (ret.data.data.length <= 0) {
          this.$alert('You haven’t create any task', 'Tip', {
            confirmButtonText: 'Confirm',
            callback: action => {},
          });
        }
        return ret;
      });
    },

    goHistoryList(scope) {
      this.$router.push({
        name: 'bmTaskHistory',
        query: { task_id: scope.row.id },
      });
    },
    goDataManagement() {
      this.$router.push({
        path: '/api/prosafeai/data_management',
        query: {},
      });
    },
    showCode(scope) {
      this.scDialogVisible = true;
      this.getSampleCode(scope);
    },

    detailDialog(scope) {
      this.dialogVisible = true;
      this.modelPath = scope.row.model_path == null ? 'null' : scope.row.model_path;
      this.dataPath = scope.row.data_path == null ? 'null' : scope.row.data_path;
      this.machineInfo = scope.row.machine_info == null ? 'null' : scope.row.machine_info;
      this.taskDesc = scope.row.description == null ? 'null' : scope.row.description;
      this.hyperParas = scope.row.init_hyperparameter == null ? [] : scope.row.init_hyperparameter;
      this.algType = scope.row.algorithm_type == null ? 'null' : scope.row.algorithm_type;
      this.createTime = scope.row.create_time == null ? 'null' : scope.row.create_time;
    },
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
.select-filter {
  width: 350px;
}

label.xrequired:before {
  content: '* ';
  color: red;
}

// 这里重置dialog 的布局
::v-deep .el-dialog__body {
  padding: 0px;
}

::v-deep .el-dialog {
  border-radius: 8px;
}

::v-deep .el-dialog__title {
  /*display: none;*/
  line-height: 14px;
  font-size: 22px;
  color: #333;
}

::v-deep .el-dialog__wrapper {
  background-color: rgba(0, 0, 0, 0.2);
}

.confirmbtn-rb {
  position: absolute;
  right: 15px;
  bottom: 10px;
}

.el-dialog__header {
  height: 50px;
}
.step2-container {
  position: relative;

  .step2 {
    padding: 16px 10px 26px 10px;
    margin-top: 10px;
    background-color: #2d2d2d;
    overflow: auto;
    .text {
      color: #fff;
    }
    .copy-btn {
      position: absolute;
      right: 16px;
      bottom: 16px;
    }
  }
}

.dialog-left-title {
  display: flex;
  margin-bottom: 20px;
}

.div-hyperpara {
  margin-bottom: 20px;
}

.cdialog-title {
  font-weight: bold;
  line-height: 25px;
  font-size: 20px;
  color: #666;
}

.ptitle {
  font-weight: bold;
  line-height: 15px;
  font-size: 15px;
  color: #333;
}

.pcontent {
  margin-left: 5px;
  line-height: 15px;
  font-size: 15px;
  font-size: 15px;
  color: #999;
}

.dialog-body-style {
  margin: 20px 0 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dialog_grey_line {
  height: 1px;
  border-top: 1px solid #ddd;
  text-align: center;
}

.el-pagination {
  text-align: center;
}
</style>
