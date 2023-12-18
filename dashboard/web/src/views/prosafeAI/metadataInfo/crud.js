export const crudOptions = vm => {
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: 'vxe-table',
      rowKey: false,
      height: '100%',
      rowId: 'id',
      stripe: true,
      emptyText: 'No data',
      fit: true,
      highlightCurrentRow: true,
      rowStyle({ row, rowIndex }) {
        const stylejson = {};
        stylejson.height = 50 + 'px';
        return stylejson;
      },
    },
    // 判断object number 是否大于0，来显示操作列
    rowHandle:
      vm.$store.state.objectnumber <= 0
        ? false
        : {
            columnHeader: 'Operation',
            align: 'center',
            width: 160,
            view: { show: false },
            edit: { show: false },
            remove: { show: false },
            custom: [
              {
                text: 'Object Table',
                type: 'warning',
                size: 'small',
                emit: 'viewDetails',
                show(index, row) {
                  return true;
                },
                disabled(index, row) {
                  if (row.object_num === 0) {
                    return true;
                  } else {
                    return false;
                  }
                },
                order: 1,
              },
            ],
            fixed: 'right',
          },
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
          text: 'Fuzzy Search', // 按钮文字， null= 取消文字，↓↓↓↓也可以传入一个方法↓↓↓↓
          // text(scope){return 'xx'}
          type: 'warning', // 按钮类型
          icon: 'el-view', // 按钮图标，↓↓↓↓也可以传入一个方法↓↓↓↓
          // icon(scope){return 'xx'}
          size: 'small', // 按钮大小
          circle: false, // 圆形按钮 ，需要thin=true,且text=null
          show: true, // 是否显示按钮，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否显示↓↓↓↓↓↓↓↓
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
          show: true, // 是否显示按钮，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否显示↓↓↓↓↓↓↓↓
          // show(index,row){return row.status==='xxx'}
          disabled: false, // 是否禁用，↓↓↓↓也可以传入一个方法根据数据决定该按钮是否禁用↓↓↓↓
          // disabled(index,row){return row.status==='xxx'}
          order: 2, // 排序号，数字小，排前面
        }, // 同上
      },
    },
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
        title: 'Search by',
        key: 'slotExample',
        // type: 'slot-all', // slot-all等效
        search: {
          disabled: false,
          slot: true,
        },
        rowSlot: true,
        show: false,
      },
    ],
  };
};
