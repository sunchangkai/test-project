<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <!--    <template slot="header">-->

    <!--    </template>-->
    <d2-crud-x
      ref="d2Crud"
      :loading="loading"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @viewDetails="details"
      crud.options.tableType="vxe-table"
    >
      <div slot="header">
        <!--        <p class="dialog_grey_line"></p>-->
        <div style="margin-bottom: 10px;margin-top: 10px;display: flex;align-items: center">
          <el-page-header @back="handleCloseCurrent" content=""></el-page-header>
          Current Version:&nbsp;&nbsp;{{ currentVersion }}&nbsp;&nbsp;&nbsp;&nbsp;
          <el-button size="small" type="warning" @click="viewPrevious">
            <i /> View Other Version
          </el-button>
          <el-button size="small" type="success" @click="importNewData">
            <i />Import New Data
          </el-button>
          <!--        <el-button type="primary" size="small" round icon="el-icon-arrow-left" @click="handleCloseCurrent">Back-->
          <!--        </el-button>-->
        </div>

        <p class="dialog_grey_line"></p>
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
          @reset="resetSearch"
          @click="fuzzySearch"
        >
          <template slot="slotExampleSearchSlot">
            <el-select v-model="selectValue" placeholder="Please select">
              <el-option
                v-for="item in columnKeyOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
            <span>&nbsp;&nbsp;for&nbsp;&nbsp;</span>
            <el-input
              ref="slotExample"
              v-model="inputValue"
              placeholder="input the value you want to search"
              style="width:250px"
            ></el-input>

            &nbsp;&nbsp;
            <el-button size="small" type="warning" @click="accurateSearch">
              Accurate Search
            </el-button>
          </template>
          <crud-toolbar
            :compact.sync="crud.pageOptions.compact"
            :columns="crud.columns"
            @refresh="doRefresh()"
            @columns-filter-changed="handleColumnsFilterChanged"
          />
        </crud-search>
      </div>
    </d2-crud-x>

    <el-dialog
      title="View Other Version"
      v-if="versionDialogVisible"
      :visible.sync="versionDialogVisible"
      @close="versionDialogClose"
    >
      <div class="dialog-body-style">
        <el-table
          max-height="250"
          :data="versionList"
          border
          highlight-current-row
          @current-change="handleCurrentChange"
          style="width: 100%;border: 1px solid #ddd;"
        >
          <el-table-column property="create_time" label="Import Data" width="210">
          </el-table-column>
          <el-table-column property="version" label="Version" width="120"> </el-table-column>
          <el-table-column property="description" label="Version Comments"> </el-table-column>
        </el-table>
      </div>

      <p class="dialog_grey_line"></p>

      <div slot="footer" class="dialog-footer">
        <el-button @click="commitVersion" type="success" :disabled="discommit">Commit</el-button>
      </div>
    </el-dialog>
    <el-dialog title="Import New Data" :visible.sync="importDialogVisible" width="40%">
      <div style="padding:10px 30px 10px 30px;">
        <el-upload
          class="upload-demo"
          :action="uploadUrl"
          :on-success="handleUploadSuccess"
          :on-remove="handleRemoveFile"
          :before-remove="beforeRemove"
          :limit="1"
          :file-list="fileList"
          :disabled="listenDisable"
        >
          <label class="xrequired">Import json file : </label>
          <el-button size="small" type="primary" :disabled="listenDisable">Browse</el-button>
        </el-upload>

        <el-checkbox style="margin-top: 10px;" v-model="previewCheck" @change="previewTemplate"
          >I have previewed and downloaded the template
        </el-checkbox>
        <div style="margin-bottom: 10px;">
          <el-link type="primary" @click="onExport">Preview and download Json template </el-link>
        </div>

        <div style="margin-bottom: 10px;display: flex; align-items: center;">
          <el-tooltip placement="top">
            <div slot="content">Example:<br />0 car<br />1 bus<br />...</div>
            <label class="xrequired">Import labels : </label>
          </el-tooltip>
          <input
            style="display: none;"
            type="file"
            @change="handleUploadLabel"
            ref="labelsInput"
            accept=".txt"
          />
          <div>
            <el-button
              style="margin-left: 8px;"
              size="small"
              type="primary"
              @click="handleClickUpload"
              >upload</el-button
            >
          </div>
          <span style="padding-left: 10px;">{{ labelFile.name }}</span>
        </div>

        <label class="xrequired">Version comments : </label>
        <el-input
          type="textarea"
          :rows="3"
          placeholder="please input the comments"
          v-model="verisonComments"
          :style="{ marginTop: 10 + 'px' }"
        >
        </el-input>
      </div>
      <p class="dialog_grey_line"></p>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addVersion" type="success">Commit</el-button>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import { d2CrudPlus } from 'd2-crud-plus';
import util from '@/libs/util';
// import { mapState, mapMutations } from 'vuex'
import { mapMutations, mapActions } from 'vuex';

export default {
  name: 'metadataInfo',
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      loading: false,
      uploadUrl: util.baseURL() + 'api/system/file/',
      previewCheck: false,
      tableId: '',
      verisonComments: '',
      fileList: [],
      uploadSuccessUrl: '',
      versionDialogVisible: false,
      importDialogVisible: false,
      accurateQuery: true,
      columnKeyOptions: [],
      selectValue: '',
      inputValue: '',
      hasInitColumn: false,
      addColumns: [],
      versionList: [],
      queryObject: {},
      currentVersion: '',
      chooseVersionTemp: '',
      version: '1.0.0',
      taskType: 0,
      discommit: true,
      labelFile: {},
    };
  },
  mounted() {
    this.$store.commit('changeid', this.$route.query.table_id);
    this.$store.commit('saveObjectnumber', this.$route.query.object_number);
    this.tableId = this.$route.query.table_id;
    this.currentVersion = this.$route.query.latest_version;
    this.taskType = this.$route.query.task_type;
  },

  watch: {
    importDialogVisible: function(newV, oldV) {
      if (!newV) {
        this.uploadSuccessUrl = '';
        this.verisonComments = '';
        this.labelFile = {};
      }
    },
    chooseVersionTemp: function(newV, oldV) {
      if (newV === '') {
        this.discommit = true;
      } else {
        this.discommit = false;
      }
    },
  },

  methods: {
    ...mapMutations('d2admin/page', ['keepAliveRemove', 'keepAliveClean']),
    ...mapActions('d2admin/page', ['close', 'closeLeft', 'closeRight', 'closeOther', 'closeAll']),
    handleUploadLabel(e) {
      this.labelFile = e.target.files[0];
    },
    handleClickUpload() {
      this.$refs.labelsInput.click();
    },
    versionDialogClose() {
      this.chooseVersionTemp = '';
    },
    // 关闭当前
    handleCloseCurrent() {
      this.$router.back();
    },
    beforeRemove(file, fileList) {
      return this.$confirm('Are you sure to remove ' + file.name + '？');
    },
    handleRemoveFile(file, fileList) {
      this.uploadSuccessUrl = '';
    },
    onExport() {
      const that = this;
      this.$confirm('Are you sure to export json template?', 'Warning', {
        confirmButtonText: 'confirm',
        cancelButtonText: 'cancel',
        type: 'warning',
      }).then(function() {
        const query = {};
        query.table_id = that.tableId;
        return api.exportData(query);
      });
    },
    previewTemplate(val) {},
    addVersionSucc() {
      this.$message.success('add new version success!');
      this.importDialogVisible = false;
      this.uploadSuccessUrl = '';
      this.verisonComments = '';
      this.labelFile = {};
      this.previewCheck = false;
    },
    // 增加一个版本信息
    addVersion: function() {
      if (
        this.uploadSuccessUrl.length !== 0 &&
        this.verisonComments.length !== 0 &&
        this.labelFile.name
      ) {
        const formData = new FormData();
        formData.append('table_id', this.tableId);
        formData.append('version_comments', this.verisonComments);
        formData.append('url', this.uploadSuccessUrl);
        formData.append('label_file', this.labelFile);

        const that = this;
        api.AddVersion(formData).then(ret => {
          that.addVersionSucc();
        });
      } else {
        this.$message.error('No upload json file or labels file or comments is emtpy!');
      }
    },
    // 上传成功
    handleUploadSuccess(response, file, fileList) {
      this.uploadSuccessUrl = response.data.url;
    },

    handleCurrentChange(currentRow, oldRow) {
      this.chooseVersionTemp = currentRow.version;
    },
    getCrudOptions() {
      return crudOptions(this);
    },
    importNewData() {
      this.importDialogVisible = true;
    },
    resetSearch() {
      this.inputValue = '';
      this.selectValue = '';
    },
    accurateSearch() {
      this.accurateQuery = true;
      this.doSearch({});
    },
    fuzzySearch() {
      this.accurateQuery = false;
    },
    getVersion(query, manural) {
      const that = this;
      return api.GetVersion(query).then(ret => {
        if (manural) {
          that.versionDialogVisible = true;
        }
        that.versionList = [];
        for (const item of ret.data.data) {
          that.versionList.push(item);
        }
      });
    },
    pageRequest(query) {
      this.loading = true;
      query.table_id = this.$route.query.table_id;
      this.queryObject = query;
      this.getVersion(query, false);
      query.search_param = this.selectValue;
      query.search_content = this.inputValue;
      query.version = this.currentVersion;
      if (this.accurateQuery) {
        query.search_type = '0';
      } else {
        query.search_type = '1';
      }
      this.accurateQuery = false;
      const _this = this;
      return api
        .GetList(query)
        .then(ret => {
          this.loading = false;
          if (ret.data.data.length >= 0) {
            if (!_this.hasInitColumn) {
              Object.keys(ret.data.data[0]).forEach(function(key) {
                // 不显示下面三列
                if (key !== 'data_version' && key !== 'image_path' && key !== 'class') {
                  if (key === 'object_num') {
                    if (_this.taskType > 0) {
                      _this.addColumn(key);
                      _this.columnKeyOptions.push({
                        value: key,
                        label: key,
                      });
                    }
                  } else {
                    _this.addColumn(key);
                    _this.columnKeyOptions.push({
                      value: key,
                      label: key,
                    });
                  }
                }
                _this.hasInitColumn = true;
              });
            }
          }
          return ret;
        })
        .catch(() => {
          _this.loading = false;
        });
    },
    details(scope) {
      const that = this;
      this.$router.push({
        name: 'objectTable',
        path: '/api/prosafeai/object_tag_details/',
        query: {
          table_id: that.tableId,
          version: that.currentVersion,
          sample_id: scope.row.id,
        },
        params: {
          image_name: scope.row.image_name,
          image_format: scope.row.image_format,
          dataset: scope.row.dataset,
        },
      });
    },
    commitVersion() {
      if (this.chooseVersionTemp === '') {
        this.$message({
          message: 'You have not choose version yet!',
          type: 'warning',
        });
      } else {
        this.discommit = true;
        this.currentVersion = this.chooseVersionTemp;
        this.versionDialogVisible = false;
        this.doSearch({});
      }
    },
    viewPrevious() {
      this.getVersion(this.queryObject, true);
    },
    addColumn(columnKey) {
      const crudOptions = this.getCrudOptions();
      this.addColumns.push({
        key: columnKey,
        title: columnKey,
        minWidth: 200,
      });
      for (const item of this.addColumns) {
        crudOptions.columns.push(item);
      }
      this.reInitColumns(crudOptions);
    },
  },
  computed: {
    // 一个计算属性的 getter
    listenDisable() {
      return !this.previewCheck;
    },
  },
};
</script>

<style lang="scss" scoped>
//表头
thead th:not(.is-hidden):first-child {
  border-left: 1px solid #ebeef5;
}

//表单
.el-table__row {
  td:not(.is-hidden):first-child {
    border-left: 1px solid #e4e7ec;
  }
}

.dialog-body-inner {
  padding: 1px;
  border: 1px solid #a1a1a1;
  background: #dddddd;
  border-radius: 5px;
}

.dialog-body-style {
  padding: 10px 40px 10px 40px;
}

::v-deep .el-dialog__body {
  padding: 0;
}

::v-deep .el-dialog {
  border-radius: 8px;
}

::v-deep .el-dialog__title {
  line-height: 24px;
  font-size: 18px;
  color: #666;
}

::v-deep .el-dialog__wrapper {
  background-color: rgba(0, 0, 0, 0.2);
}

.dialog_grey_line {
  height: 10px;
  border-top: 1px solid #ddd;
  text-align: center;
  margin-top: 15px;
}

.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}

label.xrequired:before {
  content: '* ';
  color: red;
}

.el-pagination {
  text-align: center;
}
.grey_line {
  height: 1px;
  border-top: 1px solid #ddd;
  text-align: center;
  margin-bottom: 10px;
}
</style>
