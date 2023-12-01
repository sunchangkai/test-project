import { mapState } from 'vuex';
import menuMixin from '../mixin/menu';
import { createMenu } from '../libs/util.menu';
import BScroll from 'better-scroll';

export default {
  name: 'd2-layout-header-aside-menu-side',
  mixins: [menuMixin],
  render(h) {
    console.log('menu path:', this.$route.fullPath);
    let highLightMenuPath = '';
    if (
      this.$route.fullPath.indexOf('/api/prosafeai/prosafeai_metadatainfo') >= 0 ||
      this.$route.fullPath.indexOf('/api/prosafeai/object_tag_details') >= 0
    ) {
      highLightMenuPath = '/api/prosafeai/table_details';
    } else if (this.$route.fullPath.indexOf('/api/prosafeai/prosafeai_datadisplaychart') >= 0) {
      highLightMenuPath = '/api/prosafeai/prosafeai_datadisplay';
    } else if (
      this.$route.fullPath.indexOf('/api/prosafeai/modelV_crud/modelV_run_list/') >= 0 ||
      this.$route.fullPath.indexOf('/modeltesting/bm/taskchart') >= 0
    ) {
      highLightMenuPath = '/api/prosafeai/modelV_crud/modelV_task_list';
    } else {
      highLightMenuPath = this.$route.fullPath;
    }
    return (
      <div class="d2-layout-header-aside-menu-side">
        <el-menu
          collapse={this.asideCollapse}
          collapseTransition={this.asideTransition}
          uniqueOpened={true}
          defaultActive={highLightMenuPath}
          ref="menu"
          onSelect={this.handleMenuSelect}
        >
          {this.aside.map(menu => createMenu.call(this, h, menu))}
        </el-menu>
        {this.aside.length === 0 && !this.asideCollapse ? (
          <div class="d2-layout-header-aside-menu-empty" flex="dir:top main:center cross:center">
            <d2-icon name="inbox"></d2-icon>
            <span>no sidebar menu</span>
          </div>
        ) : null}
      </div>
    );
  },
  data() {
    return {
      asideHeight: 300,
      BS: null,
    };
  },
  computed: {
    ...mapState('d2admin/menu', ['aside', 'asideCollapse', 'asideTransition']),
  },
  watch: {
    // 折叠和展开菜单的时候销毁 better scroll
    asideCollapse(val) {
      this.scrollDestroy();
      setTimeout(() => {
        this.scrollInit();
      }, 500);
    },
  },
  mounted() {
    this.scrollInit();
  },
  beforeDestroy() {
    this.scrollDestroy();
  },
  methods: {
    scrollInit() {
      this.BS = new BScroll(this.$el, {
        mouseWheel: true,
        click: true,
        // 如果你愿意可以打开显示滚动条
        // scrollbar: {
        //   fade: true,
        //   interactive: false
        // }
      });
    },
    scrollDestroy() {
      // https://github.com/d2-projects/d2-admin/issues/75
      try {
        this.BS.destroy();
      } catch (e) {
        delete this.BS;
        this.BS = null;
      }
    },
  },
};
