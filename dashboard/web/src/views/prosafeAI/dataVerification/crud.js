// import { request } from '@/api/service'
export const crudOptions = vm => {
  return {
    pageOptions: {
      compact: true,
    },
    loadingOptions: {
      // 设置加载文字，进度条形状，背景色
      text: '加载中...',
      background: '#585858',
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true,
      height: '100%',
      rowId: 'id',
      algin: 'center',
      highlightCurrentRow: true,
      rowStyle({ row, rowIndex }) {
        const styleJson = {
          height: '50px',
        };
        return styleJson;
      },
    },
    rowHandle: {
      columnHeader: 'Operation',
      align: 'center',
      width: 240,
      view: { show: false },
      edit: { show: false },
      remove: { show: false },
      custom: [
        {
          text(scope) {
            return scope.row.status === 'DONE' ? 'ReTest' : 'Test';
          },
          type: 'primary',
          size: 'small',
          emit: 'runTask',
          show: true,
          order: 1,
        },
        {
          text: 'View Sub-task',
          type: 'warning', // 按钮类型
          // icon: 'el-view',
          size: 'small',
          emit: 'viewSubTask',
          disabled: false,
          show: true,
        },
      ],
      fixed: 'right',
    },
    viewOptions: {
      componentType: 'form',
    },
    formOptions: {
      defaultSpan: 24,
      width: '30%',
    },
    columns: [
      {
        title: 'Task ID',
        key: 'id',
        width: 100,
        align: 'center',
        form: {
          disabled: true,
        },
      },
      {
        title: 'Task Name',
        key: 'task_name',
        width: 250,
        align: 'center',
        type: 'input',
        form: {
          disabled: true,
        },
      },
      {
        title: 'Json File',
        key: 'requirements',
        width: 250,
        align: 'center',
        form: {
          disabled: true,
        },
      },
      {
        title: 'Table Name',
        key: 'table_description',
        show: false,
        width: 250,
        align: 'center',
        // type: 'select',
        form: {
          disabled: false,
        },
      },
      {
        title: 'Table Version',
        key: 'version',
        width: 250,
        align: 'center',
        form: {
          disabled: false,
        },
      },
      {
        title: 'Test_begin_time',
        key: 'test_begin_time',
        width: 250,
        align: 'center',
        form: {
          disabled: true,
        },
      },
      {
        title: 'Test_end_time',
        key: 'test_end_time',
        width: 250,
        align: 'center',
        form: {
          disabled: true,
        },
      },
      {
        title: 'Status',
        key: 'status',
        width: 100,
        form: {
          disabled: true,
        },
        align: 'center',
      },
    ],
  };
};
