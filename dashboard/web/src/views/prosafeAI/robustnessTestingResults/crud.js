export const crudOptions = vm => {
  const runId = vm.$route.query.runId;
  return {
    pageOptions: {
      compact: false,
    },
    options: {
      height: '100%',
    },
    rowHandle: false,
    searchOptions: {
      form: {
        run_id: runId,
      },
      debounce: false,
    },
    columns: [
      vm.$route.query.modelType !== 'black box' && {
        title: 'Attack Sample',
        key: 'saved_path',
        rowSlot: true,
      },
      {
        title: 'Seed',
        key: 'init_path',
        rowSlot: true,
      },
      {
        title: 'Method',
        key: 'mutated_method',
        type: 'select',
        search: {
          disabled: false,
          key: 'method',
          component: {
            props: {
              options: vm.runAttackMethodList,
            },
          },
        },
        dict: {
          value: 'name',
          label: 'name',
        },
      },
      vm.$route.query.algType !== 'object_detection' && {
        title: 'True Label',
        key: 'label',
        type: 'select',
        search: {
          disabled: false,
          component: {
            props: {
              options: vm.runLabelList,
            },
          },
        },
        dict: {
          value: 'idx',
          label: 'category',
        },
      },
      vm.$route.query.algType !== 'object_detection' && {
        title: 'Pre Label',
        key: 'pred_label',
        type: 'select',
        search: {
          disabled: false,
          component: {
            props: {
              options: vm.runLabelList,
            },
          },
        },
        dict: {
          value: 'idx',
          label: 'category',
        },
      },
      vm.$route.query.algType === 'object_detection' && {
        title: 'Attack Status',
        key: 'attack_status',
        type: 'select',
        search: {
          disabled: false,
          key: 'attack_status',
          component: {
            props: {
              options: [
                { label: 'success', value: 'success' },
                { label: 'fail', value: 'fail' },
              ],
            },
          },
        },
      },
      {
        title: 'L0',
        key: 'l0',
      },
      {
        title: 'L1',
        key: 'l1',
      },
      {
        title: 'L2',
        key: 'l2',
      },
      {
        title: 'Linf',
        key: 'linf',
      },
      {
        title: 'SSIM',
        key: 'ssim',
      },
    ].filter(Boolean),
  };
};
