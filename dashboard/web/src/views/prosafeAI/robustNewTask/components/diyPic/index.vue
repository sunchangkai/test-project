<template>
  <div class="pic-container">
    <div class="header">
      <div class="title">{{ isOrigin ? 'Original sample' : 'Attacked sample' }}</div>
      <div v-if="!isOrigin" class="desc">
        {{ isMinimum ? 'Minimum parameter value' : 'Maximum parameter value' }}
      </div>
    </div>

    <div class="pic">
      <img :src="imgUrl" style="width: 100%;" />
    </div>
    <div class="select">
      <div v-if="isOrigin">
        <div>Default parameter scope</div>
        <div style="margin: 10px 0;text-align: center;">
          <div v-for="i in atk.parameters" :key="i.id">
            {{ i.name + ':(' + i.value + ')' }}
          </div>
        </div>
      </div>
      <div v-else>
        <div style="font-size: 12px;min-height: 50px;">
          <span>Current parameter</span>
          <span style="padding: 4px;" v-for="i in isMinimum ? minSelect : maxSelect" :key="i.id">
            {{ i.name + '=' + i.value }}
          </span>
        </div>
        <div v-if="!isEditMode">
          <div style="margin: 10px;text-align: center;">
            <el-button @click="isEditMode = true" type="primary">{{
              isMinimum ? 'Set minimum' : 'Set maximum'
            }}</el-button>
          </div>
        </div>
        <div v-else>
          <div class="sliders" v-for="i in isMinimum ? minSelect : maxSelect" :key="i.id">
            <span style="display: inline-block; width: 56px;">{{ i.name }}</span>
            <div style="flex: 1;position: relative;">
              <span style="position: absolute;left: 0;bottom: 26px;">{{
                getSliderMin(i.name)
              }}</span>
              <span style="position: absolute;right: 0;bottom: 26px;">{{
                getSliderMax(i.name)
              }}</span>
              <el-slider
                :value="i.value"
                :min="getSliderMin(i.name)"
                :max="getSliderMax(i.name)"
                :step="getStep(i)"
                @input="value => sliderChange(value, i.name)"
              ></el-slider>
            </div>
          </div>
          <div style="text-align: center;">
            <el-button @click="getPic" type="primary" size="small" style="margin: auto;"
              >Ok</el-button
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { GetPic } from '../../api';

export default {
  name: 'diy-pic',
  props: ['isOrigin', 'atk', 'isMinimum', 'minSelect', 'maxSelect'],
  data() {
    return {
      currParameters: [],
      isEditMode: false,
      imgUrl: '',
    };
  },
  mounted() {
    this.getPic();
  },
  methods: {
    getBase64URL(pic) {
      const blob = this.base64ImgToFile(pic);
      const blobUrl = window.URL.createObjectURL(blob);
      return blobUrl;
    },

    base64ImgToFile(dataurl, filename = 'file') {
      // 将base64格式分割：['data:image/png;base64','XXXX']
      const arr = dataurl.split(',');
      // .*？ 表示匹配任意字符到下一个符合条件的字符 刚好匹配到：
      // image/png
      const mime = arr[0].match(/:(.*?);/)[1]; // image/png
      // [image,png] 获取图片类型后缀
      const suffix = mime.split('/')[1]; // png
      const bstr = atob(arr[1]); // atob() 方法用于解码使用 base-64 编码的字符串
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], `${filename}.${suffix}`, {
        type: mime,
      });
    },

    getPic() {
      const params = {};
      let method = '';

      if (!this.isOrigin) {
        this.isEditMode = false;
        const source = this.isMinimum ? this.minSelect : this.maxSelect;
        source.forEach(i => (params[i.name] = i.value));
        method = this.atk.method;
      }
      GetPic({
        method,
        params,
      }).then(ret => {
        this.imgUrl = this.getBase64URL(ret.data.image);
      });
    },
    sliderChange(value, name) {
      const { isMinimum, minSelect, maxSelect } = this;
      const source = isMinimum ? minSelect : maxSelect;
      const data = source.map(i => {
        return i.name === name
          ? {
              ...i,
              value,
            }
          : { ...i };
      });
      this.$emit('change', data);
    },
    getStep(i) {
      return i.dtype === 'float' ? 0.01 : 1;
    },
    getSliderMin(name) {
      const { isMinimum, atk, minSelect } = this;
      const parameter = atk.parameters.find(i => i.name === name);
      const res = isMinimum ? parameter.min : minSelect.find(i => i.name === name).value;
      return res;
    },
    getSliderMax(name) {
      const { isMinimum, atk, maxSelect } = this;
      const parameter = atk.parameters.find(i => i.name === name);
      return isMinimum ? maxSelect.find(i => i.name === name).value : parameter.max;
    },
  },
};
</script>

<style lang="scss" scoped>
.pic-container {
  border: 1px solid #2f2f2f;
  border-radius: 6px;
  padding: 12px 16px;
  width: 265px;
  .header {
    height: 30px;
    .title {
      font-weight: 600;
    }
    .desc {
      color: #666;
      font-size: 12px;
    }
  }
  .pic {
    margin: 10px 0;
    min-height: 120px;
  }
  .select {
    .sliders {
      display: flex;
      align-items: center;
    }
  }
}
</style>
