<template xmlns:el-dialloog="http://www.w3.org/1999/html">
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @runTask="runTask"
      @viewSubTask="viewSubTask"
      crud.options.tableType="vxe-table"
    >
      <div slot="header">
        <!--        <crud-search-->
        <!--          ref="search"-->
        <!--          :options="crud.searchOptions"-->
        <!--          @submit="handleSearch">-->
        <div style="margin: 20px;"></div>
        <el-button-group>
          <el-button type="success" size="medium" @click="createTask">
            <i class="el-icon-plus" /> New Task
          </el-button>
        </el-button-group>
        <crud-toolbar
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
        <div style="margin: 20px;"></div>
      </div>
    </d2-crud-x>
    <el-dialog v-bind:title="tipTitle" :visible.sync="dialogVisible" width="30%" center>
      <span>{{ tipString }}</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">OK</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="Create New Task"
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
      width="40%"
    >
      <div style="margin: 20px;"></div>
      <el-form
        :model="createTaskForm"
        ref="createTaskForm"
        :rules="createTaskRules"
        label-width="180px"
        label-position="left"
      >
        <el-form-item label="Task Name" prop="task_name" required>
          <el-input
            v-model="createTaskForm.task_name"
            placeholder="Please input a task name"
          ></el-input>
        </el-form-item>
        <el-form-item label="Choose a table" prop="table" required>
          <el-select
            v-model="createTaskForm.table"
            placeholder="Please choose a table"
            clearable
            ref="tableinfo"
            style="width: 100%"
            @change="getVersion"
          >
            <el-option
              v-for="item in TableInfo"
              :key="item.id"
              :label="item.table_description"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="Choose a table version"
          prop="table_version"
          required
          v-if="createTaskForm.table"
        >
          <el-select
            v-model="createTaskForm.table_version"
            placeholder="Please choose a table version"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="item in TableVersion"
              :key="item.version"
              :label="item.version + ' (' + item.description + ')'"
              :value="item.version"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Choose a requirement" prop="requirement" required v-if="taskNum > 0">
          <el-select
            v-model="createTaskForm.requirement"
            placeholder="Please choose a historic requirement"
            clearable
            ref="requirementinfo"
            value-key="id"
            style="width: 100%"
            @change="subRequirementDetail"
          >
            <el-option
              v-for="item in RequirementInfo"
              :key="item.id"
              :label="item.name"
              :value="item"
            >
            </el-option>
            <el-option label="Other" value="-1"></el-option>
          </el-select>
        </el-form-item>
        <!--        <el-card class="box-card" v-if="SubRequirement.length>0 && !importflag">-->
        <el-card class="d2-card" v-if="SubRequirement.length > 0 && !importflag">
          <div slot="header" class="clearfix">
            <span>Sub Requirement: </span>
            <el-button
              style="float: right; padding: 3px 0"
              type="text"
              @click="viewSubRequirement = true"
              >view more</el-button
            >
          </div>
          <div>Create Time: {{ current_requirement.create_time }}</div>
          <div v-for="item in SubRequirement.slice(0, 3)" :key="item.id" class="text item">
            name: {{ item.rule_name }}; classification: {{ item.classification }}
          </div>
        </el-card>
        <el-form-item label="Import a JSON file " prop="requirement" required v-if="importflag">
          <el-upload
            ref="upload"
            :limit="1"
            :headers="upload.headers"
            :action="upload.url"
            :disabled="upload.isUploading"
            :on-progress="handleFileUploadProgress"
            :on-success="handleFileSuccess"
          >
            <el-button size="small" type="primary" :disabled="listenDisable">
              <i />Browse
            </el-button>
          </el-upload>
        </el-form-item>
        <div style="margin: 20px;"></div>
        <el-checkbox
          :style="{ marginTop: 10 + 'px' }"
          v-model="checked"
          @change="previewTemplate"
          v-if="importflag"
        >
          I have previewed and downloaded the template
        </el-checkbox>
        <div>
          <el-link
            :style="{ marginTop: 20 + 'px' }"
            type="primary"
            @click="exportTemplate"
            v-if="importflag"
            >Preview and download Json template
          </el-link>
        </div>
      </el-form>
      <el-dialog
        title="View Sub Requirement"
        :visible.sync="viewSubRequirement"
        :close-on-click-modal="false"
        width="60%"
        append-to-body
      >
        <el-descriptions style="margin-bottom: 20px;" :column="2" border>
          <el-descriptions-item label="Requirement Name">{{
            current_requirement.name
          }}</el-descriptions-item>
          <el-descriptions-item label="Create Time">{{
            current_requirement.create_time
          }}</el-descriptions-item>
        </el-descriptions>
        <el-table max-height="300" :data="SubRequirement" highlight-current-row style="width: 100%">
          <el-table-column property="rule_name" label="Rule name" width="120"> </el-table-column>
          <el-table-column property="classification" label="Classification" width="120">
          </el-table-column>
          <el-table-column property="verification_object" label="Verification object" width="120">
          </el-table-column>
          <el-table-column property="verification_content" label="Verification content" width="120">
          </el-table-column>
          <el-table-column property="computation_rule" label="Computation rule" width="160">
          </el-table-column>
        </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button @click="viewSubRequirement = false" type="success">OK</el-button>
        </div>
      </el-dialog>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelCreateTask" type="warning">Cancel</el-button>
        <el-button @click="commitCreateTask" type="success">Commit</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title="View Sub Task"
      :visible.sync="viewSubTaskVisible"
      :close-on-click-modal="false"
      width="70%"
    >
      <el-descriptions style="margin-bottom: 20px;" :column="2" border>
        <el-descriptions-item label="Table">{{
          current_task.table_description
        }}</el-descriptions-item>
        <el-descriptions-item label="Table Version">{{
          current_task.version
        }}</el-descriptions-item>
        <el-descriptions-item label="Requirement Name">{{
          current_task.requirements
        }}</el-descriptions-item>
        <el-descriptions-item label="Test Time">{{
          current_task.test_begin_time
        }}</el-descriptions-item>
      </el-descriptions>
      <el-table max-height="300" :data="SubTask" highlight-current-row style="width: 100%">
        <el-table-column property="rule_name" label="Rule name" width="120"> </el-table-column>
        <el-table-column property="classification" label="Classification" width="120">
        </el-table-column>
        <el-table-column property="verification_object" label="Verification object" width="120">
        </el-table-column>
        <el-table-column property="verification_content" label="Verification content" width="120">
        </el-table-column>
        <el-table-column property="computation_rule" label="Computation rule" width="160">
        </el-table-column>
        <el-table-column property="test_result" label="Test result" width="120"> </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="downLoadReport" type="success">Generate report and download</el-button>
        <el-button @click="viewSubTaskVisible = false" type="success">No, thanks</el-button>
      </div>
    </el-dialog>
    <div v-if="progressVisible" class="bacc">
      <el-progress
        :text-inside="true"
        :stroke-width="15"
        :percentage="percentage"
        :color="colors"
      ></el-progress>
      <div class="wrapper">
        <div class="circle"></div>
        <div class="circle"></div>
        <div class="circle"></div>
        <div class="shadow"></div>
        <div class="shadow"></div>
        <div class="shadow"></div>
      </div>
    </div>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';
// import { mapState } from 'vuex'
import util from '@/libs/util';
// import { request, downloadJsonFile } from '@/api/service'

export default {
  name: 'ProsafeAIDataVerification',
  mixins: [d2CrudPlus.crud],
  inject: ['refreshView'],
  data() {
    return {
      dialogVisible: false,
      dialogFormVisible: false,
      tipTitle: 'Tip',
      tipString: 'Please create a task first',
      taskNum: 0,
      viewSubTaskVisible: false,
      importflag: false,
      TableInfo: [],
      TableVersion: [],
      TaskInfo: [],
      RequirementInfo: [],
      SubRequirement: [],
      default_requirement: { id: -1 },
      SubTask: [],
      current_task: '',
      current_requirement: '',
      checked: false,
      viewSubRequirement: false,
      progressVisible: false,
      percentage: 0,
      createTaskForm: {
        task_name: '',
        table: '',
        table_version: '',
        requirement: null,
        json_url: '',
      },
      createTaskRules: {
        task_name: [{ required: true, message: 'required' }],
        table: [{ required: true, message: 'required' }],
        table_version: [{ required: true, message: 'required' }],
        requirement: [{ required: true, message: 'required' }],
      },
      upload: {
        // 是否禁用上传
        isUploading: false,
        // 设置上传的请求头部
        headers: { Authorization: 'JWT ' + util.cookies.get('token') },
        // 上传的地址
        url: util.baseURL() + 'api/system/file/',
      },
    };
  },
  methods: {
    getCrudOptions() {
      return crudOptions(this);
    },
    pageRequest(query) {
      const _this = this;
      const res = api.GetList(query);
      res.then(
        function(ret) {
          const data = ret.data.data;
          _this.dialogVisible = data.length === 0;
          _this.importflag = data.length === 0;
          _this.TaskInfo = [];
          _this.RequirementInfo = [];
          data.forEach(function(item) {
            _this.TaskInfo.push(item);
            _this.taskNum = _this.TaskInfo.length;
          });
        },
        function(ret) {},
      );
      return res;
    },
    getVersion() {
      const that = this;
      const query = {};
      that.TableVersion = [];
      query.table_id = that.createTaskForm.table;
      return api.GetVersion(query).then(ret => {
        if (that.TableVersion.length <= 0) {
          for (const item of ret.data.data) {
            that.TableVersion.push(item);
          }
        }
      });
    },
    // 文件上传中处理
    handleFileUploadProgress(event, file, fileList) {
      this.upload.isUploading = true;
    },
    // 文件上传成功处理
    handleFileSuccess(response, file, fileList) {
      const that = this;
      that.upload.isUploading = false;
      that.createTaskForm.json_url = response.data.url;
    },
    exportTemplate() {
      // const that = this
      this.$confirm('Are you sure to export json template?', 'Warning', {
        confirmButtonText: 'confirm',
        cancelButtonText: 'cancel',
        type: 'warning',
      }).then(function() {
        return api.exportData();
      });
    },
    subRequirementDetail() {
      const that = this;
      that.current_requirement = that.createTaskForm.requirement;
      that.importflag = that.createTaskForm.requirement === '-1';
      that.SubRequirement = [];
      if (!that.importflag) {
        const query = {
          id: that.createTaskForm.requirement.id,
        };
        return api.GetSubRequirement(query).then(ret => {
          if (that.SubRequirement.length <= 0) {
            for (const item of ret.data.data) {
              that.SubRequirement.push(item);
            }
          }
        });
      } else {
      }
    },
    runTask({ row }) {
      const that = this;
      const obj = { task_id: row.id };
      that.openTimer();
      return api.RunTask(obj).then(ret => {
        if (ret.msg.includes('success')) {
          that.progressVisible = false;
          that.percentage = 0;
          that.$message.success('run task success!');
          that.refreshView();
        } else {
          that.$message.error('run task failed!');
        }
      });
    },
    openTimer() {
      this.progressVisible = true;
      // 进度慢
      const timer1 = setInterval(() => {
        this.percentage++;
        if (this.percentage > 90 && this.percentage <= 100) {
          if (timer1) {
            clearInterval(timer1);
          }
          // 进度快
          // const timer2 = setInterval(() => {
          //   this.percentage++
          //   if (this.percentage > 100) {
          //     clearInterval(timer2)
          //     // 加载完成,进度条消失
          //     this.progressVisible = false
          //     this.percentage = 0
          //   }
          // }, 40)
        }
      }, 50);
    },
    viewSubTask({ row }) {
      const that = this;
      that.viewSubTaskVisible = true;
      const query = {
        id: row.id,
      };
      that.current_task = row;
      return api.GetSubTask(query).then(ret => {
        if (that.SubTask.length <= 0) {
          for (const item of ret.data.data) {
            that.SubTask.push(item);
          }
        }
      });
    },
    addColumn(columnKey) {
      const crudOptions = this.getCrudOptions();
      console.log(crudOptions);
      this.addColumns.push({
        key: columnKey,
        title: columnKey,
        width: 150,
      });
      for (const item of this.addColumns) {
        crudOptions.columns.push(item);
      }
      this.reInitColumns(crudOptions);
    },
    // addRequest (row) {
    //   console.log('----addRow', row)
    //   return api.AddObj(row)
    // },
    // updateRequest (row) {
    //   console.log('----', row)
    //   return api.UpdateObj(row)
    // },
    // delRequest (row) {
    //   return api.DelObj(row.id)
    // },
    createTask() {
      const that = this;
      that.dialogFormVisible = true;
      const query = {};
      const tableinfo = api.GetTable(query);
      that.TableInfo = [];
      tableinfo.then(
        function(ret) {
          ret.data.data.forEach(function(item) {
            that.TableInfo.push(item);
          });
        },
        function(ret) {},
      );
      const requirementinfo = api.GetRequirement(query);
      that.RequirementInfo = [];
      requirementinfo.then(
        function(ret) {
          ret.data.data.forEach(function(item) {
            that.RequirementInfo.push(item);
          });
        },
        function(ret) {},
      );
    },
    cancelCreateTask() {
      const that = this;
      that.dialogFormVisible = false;
      that.importflag = false;
      that.createTaskForm = {
        task_name: '',
        table: '',
        table_version: '',
        requirement: null,
        json_url: '',
      };
      that.TableVersion = [];
      that.TableInfo = [];
      that.SubRequirement = [];
      that.RequirementInfo = [];
    },
    commitCreateTask() {
      const that = this;
      that.$refs.createTaskForm.validate(valid => {
        if (valid) {
          const obj = {
            table: that.createTaskForm.table,
            table_version: that.createTaskForm.table_version,
            task_name: that.createTaskForm.task_name,
            json_url: that.createTaskForm.json_url,
          };
          if (that.createTaskForm.requirement.id) {
            obj.requirement = that.createTaskForm.requirement.id;
          } else {
            obj.requirement = -1;
          }
          api.CommitCreateTask(obj).then(ret => {
            if (ret.msg.includes('success')) {
              that.dialogFormVisible = false;
              that.createTaskForm = {
                task_name: '',
                table: '',
                table_version: '',
                requirement: null,
                json_url: '',
              };
              that.TableVersion = [];
              that.TableInfo = [];
              that.SubRequirement = [];
              that.RequirementInfo = [];
              that.$message.success('create task success!');
              that.refreshView();
            } else {
              this.$message.error('No upload json file or requirement is emtpy!');
            }
          });
        } else {
          this.$message.error('The form verification failed. Please check!');
        }
      });
    },
    downLoadReport() {
      const query = {
        task_id: this.current_task.id,
      };
      this.$confirm('Are you sure to download report?', 'Warning', {
        confirmButtonText: 'confirm',
        cancelButtonText: 'cancel',
        type: 'warning',
      }).then(function() {
        return api.downloadReport(query);
      });
    },
  },
  computed: {
    // 一个计算属性的 getter
    // ...mapState(['tableid']),
    listenDisable() {
      return !this.checked;
    },
  },
};
</script>

<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
  .basic {
    width: 400px;
    height: 100px;
  }
}
.bacc {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
  background: rgba(0, 0, 0, 0.6);
}
.bacc .el-progress {
  position: absolute;
  width: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;
}
// 以下是蹦跶的三个小球的样式
.wrapper {
  position: absolute;
  width: 200px;
  height: 60px;
  top: 55%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.circle {
  width: 20px;
  height: 20px;
  position: absolute;
  border-radius: 50%;
  background-color: #e6ebf5;
  left: 15%;
  transform-origin: 50%;
  animation: circle7124 0.5s alternate infinite ease;
}

@keyframes circle7124 {
  0% {
    top: 60px;
    height: 5px;
    border-radius: 50px 50px 25px 25px;
    transform: scaleX(1.7);
  }

  40% {
    height: 20px;
    border-radius: 50%;
    transform: scaleX(1);
  }

  100% {
    top: 0%;
  }
}

.circle:nth-child(2) {
  left: 45%;
  animation-delay: 0.2s;
}

.circle:nth-child(3) {
  left: auto;
  right: 15%;
  animation-delay: 0.3s;
}

.shadow {
  width: 20px;
  height: 4px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.9);
  position: absolute;
  top: 62px;
  transform-origin: 50%;
  z-index: -1;
  left: 15%;
  filter: blur(1px);
  animation: shadow046 0.5s alternate infinite ease;
}

@keyframes shadow046 {
  0% {
    transform: scaleX(1.5);
  }

  40% {
    transform: scaleX(1);
    opacity: 0.7;
  }

  100% {
    transform: scaleX(0.2);
    opacity: 0.4;
  }
}
.shadow:nth-child(4) {
  left: 45%;
  animation-delay: 0.2s;
}
.shadow:nth-child(5) {
  left: auto;
  right: 15%;
  animation-delay: 0.3s;
}
</style>
