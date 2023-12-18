export let crudOptions;
// eslint-disable-next-line prefer-const
crudOptions = vm => {
  return {
    searchOptions: {
      // 查询配置参数,
      size: 'small',
      show: true, // 是否显示搜索工具条
      disabled: false, // 是否禁用搜索工具条
      searchAfterReset: true, // 点击重置后是否立即查询
      buttons: {
        search: {
          // 配置false，隐藏按钮
          thin: false, // 瘦模式，thin=true 且 text=null 可以设置方形按钮节省位置
          text: 'Search', // 按钮文字， null= 取消文字，↓↓↓↓也可以传入一个方法↓↓↓↓
          // text(scope){return 'xx'}
          type: 'warning', // 按钮类型
          icon: 'el-view', // 按钮图标，↓↓↓↓也可以传入一个方法↓↓↓↓
          // icon(scope){return 'xx'}
          size: 'small', // 按钮大小
          circle: false, // 圆形按钮 ，需要thin=true,且text=null
          show: false, // 是否显示按钮，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否显示↓↓↓↓↓↓↓↓
          // show(index,row){return row.status==='xxx'}
          disabled: false, // 是否禁用，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否禁用↓↓↓↓
          // disabled(index,row){return row.status==='xxx'}
          order: 1, // 排序号，数字小，排前面
        },
        reset: {
          thin: false, // 瘦模式，thin=true 且 text=null 可以设置方形按钮节省位置
          text: 'Reset', // 按钮文字， null= 取消文字，↓↓↓↓也可以传入一个方法↓↓↓↓
          type: 'success', // 按钮类型
          // text(scope){return 'xx'}
          icon: 'el-view', // 按钮图标，↓↓↓↓也可以传入一个方法↓↓↓↓
          // icon(scope){return 'xx'}
          size: 'small', // 按钮大小
          circle: false, // 圆形按钮 ，需要thin=true,且text=null
          show: false, // 是否显示按钮，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否显示↓↓↓↓↓↓↓↓
          // show(index,row){return row.status==='xxx'}
          disabled: false, // 是否禁用，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否禁用↓↓↓↓
          // disabled(index,row){return row.status==='xxx'}
          order: 2, // 排序号，数字小，排前面
        }, // 同上
      },
    },
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: 'vxe-table',
      size: 'medium',
      rowKey: false,
      height: '100%',
      rowId: 'id',
      stripe: true,
      emptyText: 'No data',
      highlightCurrentRow: true,
      rowStyle({ row, rowIndex }) {
        const stylejson = {};
        stylejson.height = 50 + 'px';
        return stylejson;
      },
    },

    rowHandle: false, // 隐藏操作列
    viewOptions: {
      componentType: 'form',
    },
    formOptions: {
      defaultSpan: 24,
      width: '30%',
    },
    pagination: {
      pageSizes: [10, 20, 50, 100],
      pageSize: 10,
      textAlign: 'center',
    },
    columns: [
      {
        title: 'Object_ID',
        key: 'object_id',
        width: 150,
        form: {
          disabled: true,
        },
      },

      {
        title: 'Object_Type',
        key: 'object_class',
        width: 150,
        form: {
          disabled: true,
        },
      },

      {
        title: 'Object_Tag',
        key: 'object_tag',
        minWidth: 250,
        rowSlot: true,
        form: {
          disabled: true,
        },
      },
    ],
  };
};
