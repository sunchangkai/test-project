<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x ref="d2Crud" :data="data" :columns="crud.columns" :options="crud.options">
      <template slot="body">
        <div>
          <div class="step-layout">
            <el-steps
              :active="stepActive"
              finish-status="success"
              align-center
              class="el-step__main"
            >
              <el-step title="add model"></el-step>
              <el-step title="add dataset"></el-step>
              <el-step title="add config"></el-step>
            </el-steps>
          </div>

          <div class="content-layout">
            <div v-if="modelDivVisiable" class="content-div">
              <el-form
                :model="modelForm"
                :rules="modelRules"
                ref="modelFormRef"
                label-width="180px"
                label-position="left"
                style="height: 100%"
              >
                <el-form-item label="Model Path:" prop="modelPath">
                  <el-input
                    style="width: 550px"
                    v-model="modelForm.modelPath"
                    placeholder="please enter an absolute path, eg: /folder/file"
                  ></el-input>
                </el-form-item>

                <el-form-item label="Domain:" prop="modelDomain">
                  <el-select
                    class="select-filter"
                    v-model="modelForm.modelDomain"
                    size="medium"
                    placeholder="please select domain"
                  >
                    <el-option
                      v-for="item in modelDomains"
                      :key="item"
                      :label="item"
                      :value="item"
                    ></el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label="Task Type:" prop="modelAlgType">
                  <el-select
                    class="select-filter"
                    v-model="modelForm.modelAlgType"
                    size="medium"
                    placeholder="please select task type"
                    @change="taskTypeChange"
                    clearable
                  >
                    <el-option
                      v-for="item in modelTTypes"
                      :key="item"
                      :label="item"
                      :value="item"
                    ></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="Model Framework:" prop="modelFramework">
                  <el-select
                    class="select-filter"
                    v-model="modelForm.modelFramework"
                    size="medium"
                    placeholder="please select table name"
                    @change="handleDomainChange"
                  >
                    <el-option
                      v-for="item in modelFrameworks"
                      :key="item"
                      :label="item"
                      :value="item"
                    ></el-option>
                  </el-select>
                </el-form-item>
                <!--              -->
                <el-form-item label="Task Description:" prop="modelTaskDesc">
                  <el-input
                    type="textarea"
                    style="width: 350px"
                    v-model="modelForm.modelTaskDesc"
                  ></el-input>
                </el-form-item>

                <div style="display: flex;flex-direction: row-reverse">
                  <el-button type="success" @click="validModel('modelFormRef')" style="width: 100px"
                    >Next</el-button
                  >
                </div>
              </el-form>
            </div>

            <div v-if="datasetDivVisiable" class="content-div">
              <el-form
                :model="datasetForm"
                :rules="datasetRules"
                ref="datasetFormRef"
                label-width="180px"
                label-position="left"
                style="height: 100%"
              >
                <el-form-item label="Choose the table:" prop="datasetTable">
                  <el-select
                    class="select-filter"
                    v-model="datasetForm.datasetTable"
                    size="medium"
                    placeholder="please select table name"
                    @change="handleTableChange"
                  >
                    <el-option
                      v-for="item in tableArr"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    ></el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label="Choose the version:" prop="datasetTableVersion">
                  <el-select
                    class="select-filter"
                    v-model="datasetForm.datasetTableVersion"
                    size="medium"
                    placeholder="please select domain"
                  >
                    <!--                    <el-option v-for="item in versionArr" :key="item"-->
                    <!--                               :label="item"-->
                    <!--                               :value="item"></el-option>-->

                    <el-option
                      v-for="item in versionArr"
                      :key="item.version"
                      :label="item.version + ' (' + item.description + ')'"
                      :value="item.version"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label="Data Path:" prop="dataPath">
                  <el-input
                    style="width: 550px"
                    v-model="datasetForm.dataPath"
                    placeholder="please enter an absolute path, eg: /folder/file"
                  ></el-input>
                </el-form-item>

                <el-form-item v-if="isObjDet" label="Bounding box type:" prop="bboxType">
                  <el-select
                    class="select-filter"
                    v-model="datasetForm.bboxType"
                    placeholder="please select bounding box type"
                  >
                    <el-option
                      v-for="item in bboxTypeList"
                      :key="item.label"
                      :label="item.label"
                      :value="item.value"
                    ></el-option>
                  </el-select>
                </el-form-item>

                <el-form-item v-if="isObjDet" label="Is the output scaled:" prop="scale">
                  <el-select v-model="datasetForm.scale">
                    <el-option
                      v-for="item in scaleTypeList"
                      :key="item.label"
                      :label="item.label"
                      :value="item.value"
                    ></el-option>
                  </el-select>
                </el-form-item>

                <!-- <el-form-item label="Dataset format:" prop="datasetFormat">
                  <el-select
                    class="select-filter"
                    v-model="datasetForm.datasetFormat"
                    size="medium"
                    placeholder="please select domain"
                  >
                    <el-option
                      v-for="item in datasetFormatArr"
                      :key="item"
                      :label="item"
                      :value="item"
                    ></el-option>
                  </el-select>
                </el-form-item> -->

                <div style="display: flex;flex-direction: row-reverse">
                  <el-button
                    type="success"
                    @click="validDatasetForm('datasetFormRef')"
                    style="width: 100px"
                    >Next
                  </el-button>
                  <el-button @click="backToEdit(0)" style="width: 100px;margin-right: 10px"
                    >Prev
                  </el-button>
                </div>
              </el-form>
            </div>

            <div v-if="configDivVisiable" class="content-div">
              <template v-if="!!templates.length && !isShowCfg">
                <div>
                  <div class="templHeader">Configuration Template List</div>
                  <el-table :data="templates" border>
                    <el-table-column align="center" prop="modelAlgType" label="Task Type">
                      <template slot-scope="scope">
                        {{ JSON.parse(scope.row.content).modelForm?.modelAlgType }}
                      </template>
                    </el-table-column>
                    <el-table-column align="center" prop="modelType" label="Model Type">
                      <template slot-scope="scope">
                        {{ JSON.parse(scope.row.content).modelType }}
                      </template>
                    </el-table-column>
                    <el-table-column align="center" prop="name" label="Template Name">
                    </el-table-column>
                    <el-table-column align="center" prop="description" label="Template Description">
                    </el-table-column>
                    <el-table-column align="center" prop="create_time" label="Create Time">
                    </el-table-column>
                    <el-table-column align="center" prop="op" label="Operation">
                      <template slot-scope="scope">
                        <el-button @click="applyTemplate(scope.row)" type="text">Apply</el-button>
                        <el-popconfirm
                          title="Are you sure to delete it?"
                          @confirm="delTemplate(scope.row)"
                        >
                          <el-link type="danger" slot="reference" style="margin-left: 12px;"
                            >Delete</el-link
                          >
                        </el-popconfirm>
                      </template>
                    </el-table-column>
                  </el-table>
                  <div style="text-align: right;margin-top:16px">
                    <el-button type="primary" @click="isShowCfg = true"
                      >There's nothing I want, go configure it.</el-button
                    >
                  </div>
                </div>
              </template>
              <template v-else>
                <el-container style="height: 100%;">
                  <el-main style="height: 100%;padding: 1px">
                    <span>Devices:</span>
                    <el-input
                      style="width: 550px;"
                      v-model="configForm.deviceInfo"
                      ref="deviceRef"
                      @blur="valDevice"
                      placeholder="CPU/Index of GPU"
                    ></el-input>
                    <span style="color:#666;font-size: 12px;"
                      >(You can input CPU or 0,1,2,3...)</span
                    >

                    <div class="criteria-params">
                      <div class="model-params">
                        <span>Model Type:</span>
                        <el-select
                          class="select-filter"
                          v-model="modelType"
                          size="medium"
                          placeholder="please select table name"
                          @change="handleModelTypeChange"
                        >
                          <el-option
                            v-for="item in modelTypeArr"
                            :key="item"
                            :label="item"
                            :value="item"
                          ></el-option>
                        </el-select>
                        <template v-if="modelType == 'white box'">
                          <span style="margin-left: 15px">Mutation Guidance:</span>
                          <el-radio-group v-model="mutationValue" @input="mutationChange">
                            <el-radio :label="'NC'">NC</el-radio>
                            <el-radio :label="'KMNC'">KMNC</el-radio>
                            <el-radio :label="'Top-K'">Top-K</el-radio>
                            <el-radio :label="'NeuronSensitivity'">NeuronSensitivity</el-radio>
                          </el-radio-group>
                        </template>
                      </div>

                      <div v-if="modelType == 'white box'">
                        <span style="font-weight: bold">Params of {{ mutationValue }}</span>

                        <el-popover
                          placement="top"
                          title=""
                          width="200"
                          trigger="hover"
                          :content="restoreTip"
                          style="margin: 0;"
                        >
                          <i
                            slot="reference"
                            class="el-icon-refresh-right"
                            style="font-size: 20px; color: royalblue"
                            @click="resetMutationParas"
                          ></i>
                        </el-popover>

                        <div style="display: flex">
                          <div
                            style="display: flex;flex-direction: row;align-items: center;margin-top: 5px;"
                          >
                            <span>{{ mutationFirstParasLabel }}:</span>

                            <el-input
                              ref="mutationFirstParaRef"
                              class="fristpara-input"
                              v-model="firstParaValue"
                              placeholder="0.75"
                              @blur="valMutationFirstPara"
                              oninput="value=value.replace(/[^0-9.]/g,'')"
                            ></el-input>

                            <div
                              v-if="neuronParasVisiable"
                              style="display: flex;flex-direction: row;align-items: center;"
                            >
                              <span style="margin-left: 15px;">e:</span>

                              <el-input
                                ref="mutationSecondParaRef"
                                style="width: 100px;padding: 1px"
                                v-model="secondParaValue"
                                placeholder="0.75"
                                @blur="valMutationSecondPara"
                                oninput="value=value.replace(/[^0-9.]/g,'')"
                              ></el-input>
                            </div>
                          </div>

                          <div
                            style="display: flex;flex-direction: row;align-items: center;margin-top: 5px;margin-left: 10px;"
                          >
                            <span>Activate Function:</span>
                            <el-checkbox-group v-model="actFnChoosedValue">
                              <el-checkbox v-for="act in actFnValues" :label="act" :key="act">{{
                                act
                              }}</el-checkbox>
                            </el-checkbox-group>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!--              runing-params总的布局-->
                    <div class="runing-params">
                      <div style="width: 55%;padding-right: 80px;">
                        <div v-if="modelType == 'black box'" class="hyperpara-half">
                          <div class="hyperpara-label">
                            <el-popover
                              placement="top"
                              width="300"
                              trigger="hover"
                              content="The number of bins in each parameter range."
                              style="margin: 0;"
                            >
                              <i slot="reference" class="el-icon-info"></i>
                            </el-popover>
                            <p style="margin-left: 5px;">bin_size</p>
                          </div>
                          <el-input-number
                            style="width: 160px"
                            class="fristpara-input"
                            ref="binSizeRef"
                            v-model="binSize"
                            placeholder="3"
                            :min="0"
                          ></el-input-number>
                        </div>
                        <template v-if="modelType == 'white box'">
                          <div class="hyperpara-half">
                            <div class="hyperpara-label">
                              <el-popover
                                placement="top"
                                title=""
                                width="300"
                                trigger="hover"
                                :content="descPMin"
                                style="margin: 0;"
                              >
                                <i slot="reference" class="el-icon-info"></i>
                              </el-popover>
                              <p style="margin-left: 5px;">p_min (</p>
                              <p class="params-desc">a float number from 0 to 1</p>
                              <p style="margin-left: 2px">)</p>
                            </div>

                            <el-input
                              ref="pMinRef"
                              @blur="valPMin"
                              class="fristpara-input"
                              v-model="pMinPara"
                              placeholder="0.7"
                              oninput="value=value.replace(/[^0-9.]/g,'')"
                            ></el-input>
                          </div>
                          <div class="hyperpara-half">
                            <div class="hyperpara-label">
                              <el-popover
                                placement="top"
                                title=""
                                width="300"
                                trigger="hover"
                                :content="descR"
                                style="margin: 0px"
                              >
                                <i slot="reference" class="el-icon-info"></i>
                              </el-popover>
                              <p style="margin-left: 5px;margin-right: 0px">r (</p>
                              <p class="params-desc">an integer more than 1</p>
                              <p>)</p>
                            </div>

                            <el-input
                              ref="rRef"
                              @blur="valR"
                              class="fristpara-input"
                              v-model="rPara"
                              placeholder="20"
                              oninput="value=value.replace(/[^0-9]/g,'')"
                            ></el-input>
                          </div>
                          <div class="hyperpara-half">
                            <div class="hyperpara-label">
                              <el-popover
                                placement="top"
                                title=""
                                width="300"
                                trigger="hover"
                                :content="descAlpha"
                                style="margin: 0;"
                              >
                                <i slot="reference" class="el-icon-info"></i>
                              </el-popover>
                              <p style="margin-left: 5px;margin-right: 0px">alpha (</p>
                              <p class="params-desc">a float number from 0 to 1</p>
                              <p>)</p>
                            </div>

                            <el-input
                              ref="alphaRef"
                              @blur="valAlpha"
                              class="fristpara-input"
                              v-model="alphaPara"
                              placeholder="0.8"
                              oninput="value=value.replace(/[^0-9.]/g,'')"
                            ></el-input>
                          </div>
                          <div class="hyperpara-half">
                            <div class="hyperpara-label">
                              <el-popover
                                placement="top"
                                title=""
                                width="300"
                                trigger="hover"
                                :content="descBeta"
                                style="margin: 0;"
                              >
                                <i slot="reference" class="el-icon-info"></i>
                              </el-popover>
                              <p style="margin-left: 5px;margin-right: 0px">beta (</p>
                              <p class="params-desc">a float number from 0 to 1</p>
                              <p>)</p>
                            </div>

                            <el-input
                              ref="betaRef"
                              @blur="valBeta"
                              class="fristpara-input"
                              v-model="betaPara"
                              placeholder="0.8"
                              oninput="value=value.replace(/[^0-9.]/g,'')"
                            ></el-input>
                          </div>
                        </template>
                      </div>

                      <div style="width:45%;padding-left: 100px;padding-right: 120px;">
                        <template v-if="modelType == 'white box'">
                          <div class="hyperpara-half">
                            <div class="hyperpara-label">
                              <el-popover
                                placement="top"
                                title=""
                                width="300"
                                trigger="hover"
                                :content="descKtime"
                                style="margin: 0;"
                              >
                                <i slot="reference" class="el-icon-info"></i>
                              </el-popover>
                              <p style="margin-left: 5px;">k_time:</p>
                            </div>
                            <el-input
                              ref="ktimeRef"
                              @blur="valKtime"
                              style="width: 100px;padding: 1px"
                              v-model="kTimePara"
                              placeholder="5"
                              oninput="value=value.replace(/[^0-9]/g,'')"
                            ></el-input>
                          </div>

                          <div class="hyperpara-half">
                            <div class="hyperpara-label">
                              <el-popover
                                placement="top"
                                title=""
                                width="300"
                                trigger="hover"
                                :content="descTrynumber"
                                style="margin: 0;"
                              >
                                <i slot="reference" class="el-icon-info"></i>
                              </el-popover>

                              <p style="margin-left: 5px;">try_num:</p>
                              <p style="margin-left: 5px;">try_num:</p>
                            </div>
                            <el-input
                              ref="trynumRef"
                              @blur="valTrynum"
                              style="width: 100px;padding: 1px"
                              v-model="tryNumPara"
                              placeholder="30"
                              oninput="value=value.replace(/[^0-9]/g,'')"
                            ></el-input>
                          </div>
                          <div class="hyperpara-half">
                            <div class="hyperpara-label">
                              <el-popover
                                placement="top"
                                title=""
                                width="300"
                                trigger="hover"
                                :content="descMaxiter"
                                style="margin: 0;"
                              >
                                <i slot="reference" class="el-icon-info"></i>
                              </el-popover>
                              <p style="margin-left: 5px;">max_iter:</p>
                            </div>
                            <el-input
                              ref="maxIterRef"
                              @blur="valMaxiter"
                              style="width: 100px;padding: 1px"
                              v-model="maxIterPara"
                              placeholder="500"
                              oninput="value=value.replace(/[^0-9]/g,'')"
                            ></el-input>
                          </div>
                          <div class="hyperpara-half">
                            <div class="hyperpara-label">
                              <el-popover
                                placement="top"
                                title=""
                                width="300"
                                trigger="hover"
                                :content="descBatchsize"
                                style="margin: 0;"
                              >
                                <i slot="reference" class="el-icon-info"></i>
                              </el-popover>
                              <p style="margin-left: 5px;">batch_size:</p>
                            </div>
                            <el-input
                              ref="batchSizeRef"
                              @blur="valBatchsize"
                              style="width: 100px;padding: 1px"
                              v-model="batchSizePara"
                              placeholder="8"
                              oninput="value=value.replace(/[^0-9]/g,'')"
                            ></el-input>
                          </div>
                        </template>

                        <div class="dialog" v-if="modelType == 'white box'">
                          <el-popover
                            placement="top"
                            title=""
                            width="200"
                            trigger="hover"
                            :content="restoreTip"
                          >
                            <i
                              slot="reference"
                              class="el-icon-refresh-right"
                              style="font-size: 20px;color: royalblue;position: absolute
                        ;bottom: 0;right: 0;transform: translate(150%,0%)"
                              @click="resetRuningParas"
                            ></i>
                          </el-popover>
                        </div>
                      </div>
                    </div>

                    <div v-if="isObjDet" class="obj-det-ctn">
                      <div style="padding: 10px 0;">Params of Object Detection</div>
                      <el-form
                        ref="ioForm"
                        class="io-form"
                        :model="ioForm"
                        labelPosition="left"
                        label-width="210px"
                      >
                        <el-form-item label="NMS_included">
                          <el-select v-model="ioForm.nms_include">
                            <el-option label="True" :value="1"></el-option>
                            <el-option label="False" :value="0"></el-option>
                          </el-select>
                        </el-form-item>
                        <el-form-item label="Is_normalize_needed">
                          <el-select v-model="ioForm.is_normalize">
                            <el-option label="True" :value="1"></el-option>
                            <el-option label="False" :value="0"></el-option>
                          </el-select>
                        </el-form-item>
                        <el-form-item label="Letter_box_flag">
                          <el-select v-model="ioForm.letter_box_flag">
                            <el-option label="True" :value="1"></el-option>
                            <el-option label="False" :value="0"></el-option>
                          </el-select>
                        </el-form-item>
                        <el-form-item v-if="!!ioForm.is_normalize" label="Normalize_dict">
                          <el-select v-model="ioForm.mormalize_type" style="width:100px">
                            <el-option label="Std" value="std"></el-option>
                            <el-option label="Mean" value="mean"></el-option>
                          </el-select>
                          <el-input-number
                            v-if="ioForm.mormalize_type == 'std'"
                            style="width: 60px;margin-left: 10px"
                            :controls="false"
                            v-model="ioForm.normalize_dict.std"
                          ></el-input-number>
                          <el-input-number
                            v-if="ioForm.mormalize_type == 'mean'"
                            style="width: 60px;margin-left: 10px"
                            :controls="false"
                            v-model="ioForm.normalize_dict.mean"
                          ></el-input-number>
                        </el-form-item>
                        <el-form-item label="Input_size">
                          <el-input-number
                            style="width: 80px"
                            :controls="false"
                            v-model="ioForm.input_size.width"
                          ></el-input-number>
                          <span style="padding: 0 8px">*</span>
                          <el-input-number
                            style="width: 80px"
                            :controls="false"
                            v-model="ioForm.input_size.height"
                          ></el-input-number>
                        </el-form-item>
                        <el-form-item label="GroundTruth_annotation_type">
                          <el-select v-model="ioForm.groundtruth_annnotation_type">
                            <el-option
                              v-for="i in groundtruthAnnoType"
                              :key="i.value"
                              :label="i.label"
                              :value="i.value"
                            ></el-option>
                          </el-select>
                        </el-form-item>

                        <el-form-item label="IOU threshold">
                          <el-input-number
                            v-model="iou"
                            :precision="2"
                            :min="0.5"
                            :max="0.95"
                            :step="0.05"
                          ></el-input-number>
                        </el-form-item>

                        <el-form-item label="Prediction_annotation_type">
                          <el-select v-model="ioForm.prediction_annnotation_type">
                            <el-option
                              v-for="i in predictionAnnoType"
                              :key="i.value"
                              :label="i.label"
                              :value="i.value"
                            ></el-option>
                          </el-select>
                        </el-form-item>
                      </el-form>
                    </div>
                    <div v-if="modelType == 'black box'" style="padding: 16px 0;color: red;">
                      * Select at least one of the following
                      {{ isObjDet ? 'two' : 'three' }} categories methods
                    </div>
                    <p style="font-weight: bold;margin-top: 8px;margin-bottom: 8px">
                      Pixel Level Attacks
                      {{
                        modelType === 'white box'
                          ? '(Pixel level and corruption select one at least)'
                          : ''
                      }}
                    </p>
                    <div>
                      <div v-for="(pam, index) in pixAddedAttackCache" :key="pam.id">
                        <div style="display: flex;align-items: center">
                          <i
                            class="el-icon-remove-outline"
                            style="font-size: 20px;margin-right: 10px;color: red;"
                            @click="delPixelAttact(index)"
                          ></i>
                          <el-select
                            class="select-filter"
                            v-model="pam.method"
                            size="medium"
                            placeholder="please select attack method"
                            @change="val => handlePixelChange(val, index)"
                          >
                            <el-option
                              v-for="itemIner in pixLeveAttackArr"
                              :key="itemIner.method"
                              :label="itemIner.method"
                              :value="itemIner.method"
                            ></el-option>
                          </el-select>

                          <div style="display: flex;flex-flow:row wrap;">
                            <div
                              v-for="(paras, idx) in pam.parameters"
                              :key="paras.id"
                              style="margin-left: 10px;display: flex;flex-direction: row;align-items: center"
                            >
                              <span>{{ paras.name }}</span>
                              <el-input
                                :ref="'pixelInputRef' + index + idx"
                                class="short-input"
                                :value="paras.value"
                                @input="value => handleVersion(value, paras, idx)"
                                :placeholder="paras.min + ',' + paras.max"
                                @blur="blurPAMParams(index, idx)"
                              ></el-input>
                              <el-popover placement="top" trigger="hover" :content="restoreTip">
                                <i
                                  slot="reference"
                                  class="el-icon-refresh-right"
                                  style="font-size: 20px; color: royalblue;margin-left: 10px"
                                  @click="resetPixelParas(index, idx)"
                                ></i>
                              </el-popover>
                            </div>
                          </div>
                          <el-popover
                            v-if="
                              !!pam.parameters?.length &&
                                pam.method !== 'FGSM' &&
                                pam.method !== 'IFGSM'
                            "
                            placement="top"
                            trigger="hover"
                            content="View the visualization effect of this method"
                          >
                            <i
                              slot="reference"
                              class="el-icon-picture-outline"
                              style="font-size: 20px; color: royalblue;"
                              @click="getDiffPic(pam, 'pixel')"
                            ></i>
                          </el-popover>
                        </div>
                        <!--                      <p style="color: #49a1ff;font-size: 10px;">Comments:xxxxxxx</p>-->
                      </div>

                      <el-button
                        class="addattack"
                        type="primary"
                        icon="el-icon-plus"
                        @click="addPixelAttact"
                        >ADD
                      </el-button>
                    </div>
                    <template v-if="!(modelType === 'black box' && isObjDet)">
                      <p style="font-weight: bold;margin-top: 15px;margin-bottom: 10px;">
                        Semantic Level Attacks
                        {{ modelType === 'black box' ? '' : '(Select one at least)' }}
                      </p>
                      <div style="">
                        <div v-for="(pam, index) in semanticAddedAttackCache" :key="pam.id">
                          <div style="display: flex;align-items: center">
                            <i
                              class="el-icon-remove-outline"
                              style="font-size: 20px;margin-right: 10px;color: red;"
                              @click="delSemanticAttact(index)"
                            ></i>
                            <el-select
                              class="select-filter"
                              v-model="pam.method"
                              size="medium"
                              placeholder="please select attack method"
                              @change="val => handleSemanticChange(val, index)"
                            >
                              <el-option
                                v-for="itemIner in semanticLeveAttackArr"
                                :key="itemIner.method"
                                :label="itemIner.method"
                                :value="itemIner.method"
                              ></el-option>
                            </el-select>

                            <div style="display: flex;flex-flow:row wrap;align-items: center;">
                              <div
                                v-for="(paras, idx) in pam.parameters"
                                :key="paras.id"
                                style="margin-left: 10px;display: flex;flex-direction: row;align-items: center"
                              >
                                <span>{{ paras.name }}</span>
                                <el-input
                                  :ref="'semanticInputRef' + index + idx"
                                  class="short-input"
                                  :value="paras.value"
                                  @input="value => handleVersion(value, paras, idx)"
                                  :placeholder="paras.min + ',' + paras.max"
                                  @blur="blurSAMParams(index, idx)"
                                ></el-input>

                                <el-popover
                                  placement="top"
                                  title=""
                                  width="200"
                                  trigger="hover"
                                  :content="restoreTip"
                                >
                                  <i
                                    slot="reference"
                                    class="el-icon-refresh-right"
                                    style="font-size: 20px; color: royalblue;margin-left: 10px"
                                    @click="resetSemanticParas(index, idx)"
                                  ></i>
                                </el-popover>
                              </div>
                              <el-popover
                                v-if="!!pam.parameters?.length"
                                placement="top"
                                trigger="hover"
                                content="View the visualization effect of this method"
                              >
                                <i
                                  slot="reference"
                                  class="el-icon-picture-outline"
                                  style="font-size: 20px; color: royalblue;"
                                  @click="getDiffPic(pam, 'semantic')"
                                ></i>
                              </el-popover>
                            </div>
                          </div>
                        </div>

                        <el-button
                          class="addattack"
                          type="primary"
                          icon="el-icon-plus"
                          @click="addSemanticAttact()"
                          >ADD
                        </el-button>
                      </div>
                    </template>
                    <template>
                      <p style="font-weight: bold;margin-top: 15px;margin-bottom: 10px;">
                        Corruption Attacks
                      </p>
                      <div>
                        <div v-for="(pam, index) in selectedCorr" :key="pam.id">
                          <div style="display: flex;align-items: center">
                            <i
                              class="el-icon-remove-outline"
                              style="font-size: 20px;margin-right: 10px;color: red;"
                              @click="delCorr(index)"
                            ></i>
                            <el-select
                              class="select-filter"
                              v-model="pam.method"
                              size="medium"
                              placeholder="please select attack method"
                              @change="val => handleCorrChange(val, index)"
                            >
                              <el-option
                                v-for="itemIner in corrAttacks"
                                :key="itemIner.method"
                                :label="itemIner.method"
                                :value="itemIner.method"
                              ></el-option>
                            </el-select>

                            <div style="display: flex;flex-flow:row wrap;">
                              <div
                                v-for="(paras, idx) in pam.parameters"
                                :key="paras.id"
                                style="margin-left: 10px;display: flex;flex-direction: row;align-items: center"
                              >
                                <span>{{ paras.name }}</span>
                                <el-input
                                  :ref="'corrInputRef' + index + idx"
                                  class="short-input"
                                  :value="paras.value"
                                  @input="value => handleVersion(value, paras, idx)"
                                  :placeholder="paras.min + ',' + paras.max"
                                  @blur="blurCorrParams(index, idx)"
                                ></el-input>
                                <el-popover placement="top" trigger="hover" :content="restoreTip">
                                  <i
                                    slot="reference"
                                    class="el-icon-refresh-right"
                                    style="font-size: 20px; color: royalblue;margin-left: 10px"
                                    @click="resetCorrParas(index, idx)"
                                  ></i>
                                </el-popover>
                              </div>
                            </div>
                            <!-- <el-popover
                              v-if="
                                !!pam.parameters?.length &&
                                  pam.method !== 'FGSM' &&
                                  pam.method !== 'IFGSM'
                              "
                              placement="top"
                              trigger="hover"
                              content="View the visualization effect of this method"
                            >
                              <i
                                slot="reference"
                                class="el-icon-picture-outline"
                                style="font-size: 20px; color: royalblue;"
                                @click="getDiffPic(pam, 'pixel')"
                              ></i>
                            </el-popover> -->
                          </div>
                          <!--                      <p style="color: #49a1ff;font-size: 10px;">Comments:xxxxxxx</p>-->
                        </div>

                        <el-button
                          class="addattack"
                          type="primary"
                          icon="el-icon-plus"
                          @click="addCorrAttact"
                          >ADD
                        </el-button>
                      </div>
                    </template>
                    <div style="display: flex;flex-direction: row-reverse">
                      <el-button
                        type="success"
                        @click="toPreview()"
                        style="width: 100px;margin: 0 20px 0 0;"
                        >Next
                      </el-button>
                      <el-button @click="backToEdit(1)" style="width: 100px;margin-right: 10px"
                        >Prev
                      </el-button>
                    </div>
                  </el-main>
                </el-container>
              </template>
            </div>
            <div v-if="previewDivVisiable" class="content-div">
              <el-container style="height: 100%;">
                <el-main style="height: 100%;padding: 1px">
                  <div class="criteria-params">
                    <div>
                      <span style="font-weight: bold;font-size: 20px;">Model Information</span>

                      <div class="dialog">
                        <el-button
                          type="primary"
                          size="small"
                          class="edit-button"
                          @click="backToEdit(0)"
                          >Edit
                        </el-button>
                      </div>

                      <div style="display: flex;margin-top: 15px;">
                        <div style="width:50%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold;">Model Path:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              modelForm.modelPath
                            }}</span>
                          </li>
                        </div>
                        <div style="width:50%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold">Domain:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              modelForm.modelDomain
                            }}</span>
                          </li>
                        </div>
                      </div>
                      <div style="display: flex;margin-top: 15px;">
                        <div style="width:50%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold;">Model Framework:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              modelForm.modelFramework
                            }}</span>
                          </li>
                        </div>
                        <div style="width:50%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold">Task Type:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              modelForm.modelAlgType
                            }}</span>
                          </li>
                        </div>
                      </div>
                    </div>
                    <div></div>
                  </div>

                  <!--Data Information 布局-->
                  <div class="criteria-params">
                    <div>
                      <span style="font-weight: bold;font-size: 20px;">Data Information</span>
                      <div class="dialog">
                        <el-button
                          type="primary"
                          size="small"
                          class="edit-button"
                          @click="backToEdit(1)"
                          >Edit
                        </el-button>
                      </div>
                      <div style="display: flex;margin-top: 15px;">
                        <div style="width:50%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold;">Tabel:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              this.previewTabelName
                            }}</span>
                          </li>
                        </div>
                        <div style="width:50%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold">Data Path:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              datasetForm.dataPath
                            }}</span>
                          </li>
                        </div>
                      </div>
                      <div style="display: flex;margin-top: 15px;">
                        <div style="width:50%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold;">Table version:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              datasetForm.datasetTableVersion
                            }}</span>
                          </li>
                        </div>
                        <!-- <div style="width:50%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold">Dataset format:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              datasetForm.datasetFormat
                            }}</span>
                          </li>
                        </div> -->
                      </div>
                    </div>
                  </div>

                  <!--init hyper 布局-->
                  <div class="config-preview">
                    <div>
                      <span style="font-weight: bold;font-size: 20px;">Config Information</span>
                      <div class="dialog">
                        <el-button
                          type="primary"
                          size="small"
                          class="edit-button"
                          @click="backToEdit(2)"
                          >Edit
                        </el-button>
                      </div>
                      <div style="display: flex;margin-top: 15px;">
                        <div style="width:50%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold;">Device Info:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              configForm.deviceInfo
                            }}</span>
                          </li>
                        </div>
                      </div>
                      <div style="display: flex;margin-top: 15px;">
                        <div style="width:30%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold;">Model Type:</span
                            ><span style="color: #666;font-size: 14px;">{{ modelType }}</span>
                          </li>
                        </div>
                        <div v-if="modelType == 'white box'" style="width:70%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold">Mutation Guidance:</span
                            ><span style="color: #666;font-size: 14px;">{{
                              previewMutationValue
                            }}</span>
                          </li>
                        </div>
                      </div>
                      <div style="display: flex;margin-top: 15px;margin-bottom: 10px">
                        <div style="width:100%;padding-left: 20px">
                          <li>
                            <span style="font-weight: bold;">Related Parameters:</span>
                            <span
                              v-if="modelType == 'white box'"
                              style="color: #666;font-size: 14px;"
                            >
                              p_min={{ pMinPara }};k_time={{ kTimePara }};r={{
                                rPara
                              }};try_number={{ tryNumPara }};alpha={{ alphaPara }};max_iter={{
                                maxIterPara
                              }};beta={{ betaPara }};batch_size={{ batchSizePara }}
                            </span>
                            <span v-else style="color: #666;font-size: 14px;">
                              bin_size={{ binSize }};
                            </span>
                          </li>
                        </div>
                      </div>
                    </div>

                    <template v-if="!!pixelPreviewList.length">
                      <span style="font-weight: bold;font-size: 20px;">Pixel Level Attacks:</span>
                      <div style="padding-left: 20px" v-for="item in pixelPreviewList" :key="item">
                        <li>
                          <span style="font-weight: bold;">{{ item }}</span>
                        </li>
                      </div>
                    </template>

                    <template v-if="!!semanticPreviewList.length">
                      <span style="font-weight: bold;font-size: 20px;margin-top: 10px;"
                        >Semantic Level Attacks:</span
                      >
                      <div
                        style="padding-left: 20px"
                        v-for="item in semanticPreviewList"
                        :key="item"
                      >
                        <li>
                          <span style="font-weight: bold;">{{ item }}</span>
                        </li>
                      </div>
                    </template>

                    <template v-if="!!corrPreviewList.length">
                      <span style="font-weight: bold;font-size: 20px;margin-top: 10px;"
                        >Corruption Level Attacks:</span
                      >
                      <div style="padding-left: 20px" v-for="item in corrPreviewList" :key="item">
                        <li>
                          <span style="font-weight: bold;">{{ item }}</span>
                        </li>
                      </div>
                    </template>
                  </div>

                  <!-- 用 text-align:right 或者flex的方式都会使按钮的disabled属性失效 很奇怪的bug 应该是element-ui的问题 暂时使用定位实现右侧对齐 -->
                  <div style="position: relative;height: 60px;">
                    <div style="position: absolute; top: 16px; right: 0px;">
                      <el-button
                        type="success"
                        @click="createTemplVsb = true"
                        :disabled="hasAddtempl"
                      >
                        {{ hasAddtempl ? 'Saved' : 'Save as Template' }}
                      </el-button>
                      <el-button type="success" @click="createRobustTask">
                        Confirm
                      </el-button>
                    </div>
                  </div>
                </el-main>
              </el-container>
            </div>
          </div>

          <div></div>
        </div>
      </template>
    </d2-crud-x>
    <el-dialog title="" :visible.sync="downYamlVisible" width="40%">
      <div class="dialog-body-style">
        <span style="text-align: center"
          >Do you want to download the yaml file that contains all the hyperparameter you just
          set,which will be used in the test later</span
        >
      </div>

      <p class="dialog_grey_line"></p>

      <span slot="footer" class="dialog-footer">
        <el-button @click="downloadYaml" type="success" style="width: 150px">Download</el-button>
        <el-button type="primary" @click="downloadLater">Download Later</el-button>
      </span>
    </el-dialog>
    <diff-pic-modal
      v-if="diffPicVisible"
      :visible="diffPicVisible"
      @cancel="diffPicVisible = false"
      @ok="saveParams"
      :atk="currAtk"
    >
    </diff-pic-modal>
    <el-dialog title="Add to Template Library" :visible.sync="createTemplVsb">
      <el-form :model="templateForm" label-width="180px" ref="templateFormRef">
        <el-form-item label="Template Name" prop="template_name" required>
          <el-input v-model="templateForm.template_name"></el-input>
        </el-form-item>

        <el-form-item label="Template Description" prop="template_description" required>
          <el-input type="textarea" v-model="templateForm.template_description"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer">
        <el-button @click="createTemplVsb = false">Cancel</el-button>
        <el-button type="primary" @click="createTempl('templateFormRef')">Confirm</el-button>
      </span>
    </el-dialog>
  </d2-container>
</template>

<script>
import * as api from './api';
import { crudOptions } from './crud';
import diffPicModal from './components/diffPicModal';
import { d2CrudPlus } from 'd2-crud-plus';
import { mapMutations, mapActions } from 'vuex';
import { bboxTypeList, scaleTypeList, groundtruthAnnoType, predictionAnnoType } from './constants';

export default {
  name: 'robustNewTask',
  mixins: [d2CrudPlus.crud],
  components: { diffPicModal },

  data: function() {
    return {
      data: [],
      bboxTypeList,
      scaleTypeList,
      groundtruthAnnoType,
      predictionAnnoType,
      restoreTip: 'Restore default values',

      descPMin: 'The minimum probability of a seed',
      descR: 'probability decay coefficient',
      descAlpha: 'the ratio of pixel could be modified',
      descBeta: 'the ratio of pixel value change for a single pixel',

      descKtime: 'the number of mutator for one seed',
      descTrynumber: 'the number of try times for mutating one seed',
      descMaxiter: 'iteration time',
      descBatchsize: '',

      newTaskId: '',
      downYamlVisible: false,
      previewTabelName: '',

      pixelCurrentMethod: '',
      // 预览时遍历的字符串
      pixelPreviewList: [],
      semanticPreviewList: [],
      corrPreviewList: [],

      // 点击添加前,缓存一下已经增加的攻击方法明，用于验证下一次添加的方法是否重复
      beforeAddPixelAM: [],
      beforeAddSemanticAM: [],
      beforeAddCorr: [],

      // 当前选中的攻击方法名
      currentChoosePAM: '',
      currentChooseSAM: '',
      currentChooseCAM: '',

      pixAddedAttackCache: [],
      semanticAddedAttackCache: [],
      selectedCorr: [],

      // 必须加这个属性，否则页面说属性升级错误，来唯一标识添加的方法id
      pixelAMId: 0,
      pixLeveAttackArr: [],
      semanticLeveAttackArr: [],

      // 纯粹缓存服务器返回的默认值，然后后面进行比较用的。
      pixLAArrForReset: [],
      semanticLAArrForReset: [],
      corrAttacksForReset: [],
      corrAttacks: [],

      ioForm: {
        is_normalize: 1,
        mormalize_type: 'std',
        nms_include: 1,
        letter_box_flag: 1,
        input_size: {
          width: 512,
          height: 512,
        },
        normalize_dict: {
          std: 1,
          mean: 0,
          necessary: 1,
        },
        groundtruth_annnotation_type: 'xywh',
        prediction_annnotation_type: 'xywh',
      },
      iou: 0.5,

      // 8 大参数
      initHyperParameters: null,
      device: '',
      modelType: 'white box',
      pMinPara: '0.7',
      rPara: '20',
      alphaPara: '0.8',
      betaPara: '0.8',

      kTimePara: '5',
      tryNumPara: '30',
      maxIterPara: '500',
      batchSizePara: '8',

      // 黑盒参数
      binSize: 3,

      previewMutationValue: '',
      mutationValue: 'NC',
      firstParaValue: '0.75',
      secondParaValue: '',
      actFnChoosedValue: [],
      actFnValues: ['ReLU', 'Tanh', 'Sigmoid'],
      mutationFirstParasLabel: 'threshold',
      mutationSecondParasLabel: '',

      stepActive: 0,
      modelDivVisiable: true,
      datasetDivVisiable: false,
      configDivVisiable: false,
      previewDivVisiable: false,

      ncParasVisiable: true,
      kmncParasVisiable: false,
      topkParasVisiable: false,
      neuronParasVisiable: false,

      modelForm: {
        modelPath: '',
        modelFramework: 'keras',
        modelDomain: 'computer version',
        modelAlgType: 'classification',
        modelTaskDesc: '',
      },

      modelRules: {
        modelPath: [{ required: true, message: 'please enter an absolute path', trigger: 'blur' }],
        modelFramework: [
          { required: true, message: 'please select table version', trigger: 'change' },
        ],
        modelDomain: [
          { required: true, message: 'Please select algorithm type', trigger: 'change' },
        ],
        modelAlgType: [
          { required: true, message: 'Please select algorithm type', trigger: 'change' },
        ],
        modelTaskDesc: [
          { required: true, message: 'please enter task description', trigger: 'blur' },
        ],
      },

      datasetForm: {
        dataPath: '',
        datasetTable: '',
        datasetTableVersion: '',
        // todo
        // datasetFormat: 'classification',
        bboxType: '0',
        scale: 0,
      },

      datasetRules: {
        dataPath: [{ required: true, message: 'please enter an absolute path', trigger: 'blur' }],
        datasetTable: [
          { required: true, message: 'please select table version', trigger: 'change' },
        ],
        datasetTableVersion: [
          { required: true, message: 'Please select algorithm type', trigger: 'change' },
        ],
        bboxType: {
          required: true,
        },
        scale: {
          required: true,
        },
        // datasetFormat: [
        //   { required: true, message: 'Please select dataset format', trigger: 'change' },
        // ],
      },

      configForm: {
        deviceInfo: 'cpu',
      },

      configRules: {
        deviceInfo: [{ required: true, message: 'please enter an device info', trigger: 'blur' }],
      },

      modelDomains: ['computer version'],
      modelTTypes: ['classification', 'segmentation', 'object detection'],

      tableArr: [],
      versionArr: [],
      // datasetFormatArr: ['classification', 'yolo'],
      modelTypeArr: ['white box', 'black box'],

      // 由于服务器返回的对象格式不满足前端，所以利用服务器返回的格式重新组装一个格式
      pixelLevelAMId: 0,
      semanticLevelAMId: 0,

      diffPicVisible: false,
      currAtk: {},
      atkType: '',

      templates: [],
      createTemplVsb: false,
      templateForm: {},
      hasAddtempl: false,
      isShowCfg: false,
    };
  },
  computed: {
    isWhite() {
      return this.modelType === 'white box';
    },
    isObjDet() {
      return this.modelForm.modelAlgType === 'object detection';
    },
    modelFrameworks() {
      return this.isObjDet ? ['pytorch'] : ['keras', 'pytorch'];
    },
  },
  mounted() {
    this.afterInit();
    this.getTableNames();
    this.resetAllAttackMethod();
    this.getTemplates();
  },

  watch: {},
  methods: {
    ...mapMutations('d2admin/page', ['keepAliveRemove', 'keepAliveClean']),
    ...mapActions('d2admin/page', ['close']),

    taskTypeChange() {
      this.modelForm.modelFramework = '';
    },
    applyTemplate(row) {
      this.isShowCfg = true;
      this.$data = Object.assign(this.$data, JSON.parse(row.content));
    },
    delTemplate(row) {
      api.DelTempl({ id: row.id }).then(ret => {
        const data =
          ret.code === 2000
            ? {
                message: 'Deleted successfully!',
                type: 'success',
              }
            : {
                message: 'Delete failed!',
                type: 'error',
              };
        this.$message(data);
        this.getTemplates();
      });
    },
    getTemplates() {
      api.GetTemplates().then(ret => {
        this.templates = ret.data?.data;
      });
    },
    createTempl(formName) {
      this.$refs[formName].validate(valid => {
        if (!valid) {
          return false;
        }
        api
          .CreateTempl({
            ...this.templateForm,
            init_hyperparameter: JSON.stringify({
              configForm: this.configForm,
              modelType: this.modelType,
              modelForm: this.modelForm,
              mutationValue: this.mutationValue,
              firstParaValue: this.firstParaValue,
              secondParaValue: this.secondParaValue,
              actFnChoosedValue: this.actFnChoosedValue,

              pMinPara: this.pMinPara,
              rPara: this.rPara,
              alphaPara: this.alphaPara,
              betaPara: this.betaPara,
              kTimePara: this.kTimePara,
              tryNumPara: this.tryNumPara,
              maxIterPara: this.maxIterPara,
              batchSizePara: this.batchSizePara,

              pixAddedAttackCache: this.pixAddedAttackCache,
              semanticAddedAttackCache: this.semanticAddedAttackCache,
            }),
          })
          .then(ret => {
            if (ret.code === 2000) {
              this.$message({
                message: 'Adding successfully!',
                type: 'success',
              });
              this.hasAddtempl = true;
            } else {
              this.$message.error({
                message: 'Add failed',
              });
            }
            this.createTemplVsb = false;
          });
      });
    },

    saveParams(data) {
      if (this.atkType === 'pixel') {
        const idx = this.pixAddedAttackCache.findIndex(i => {
          return i.method === data.method;
        });
        this.pixAddedAttackCache[idx] = data;
      } else if (this.atkType === 'semantic') {
        const idx = this.semanticAddedAttackCache.findIndex(i => i.method === data.method);
        this.semanticAddedAttackCache[idx] = data;
      }

      this.diffPicVisible = false;
    },
    getDiffPic(currAtk, type) {
      this.currAtk = currAtk;
      this.atkType = type;

      this.diffPicVisible = true;
    },
    handleVersion(value, paras, idx) {
      const final = value ? value.replace(/\s+/g, '') : '';
      paras.value = final;
    },

    valBatchsize() {
      if (this.batchSizePara.length <= 0) {
        this.$message.error('batch_size value can not be empty!');
        this.$refs.batchSizeRef.focus();
      }
    },
    valMaxiter() {
      if (this.maxIterPara.length <= 0) {
        this.$message.error('max_iter value can not be empty!!');
        this.$refs.maxIterRef.focus();
      }
    },
    valTrynum() {
      if (this.tryNumPara.length <= 0) {
        this.$message.error('try_num value can not be empty!');
        this.$refs.trynumRef.focus();
      }
    },

    valKtime() {
      if (this.kTimePara.length <= 0) {
        this.$message.error('k_time value can not be empty!');
        this.$refs.ktimeRef.focus();
      }
    },

    valBeta() {
      if (this.betaPara.length <= 0) {
        this.$message.error('beta value can not be empty!');
        this.$refs.betaRef.focus();
      } else {
        const value = parseFloat(this.betaPara);
        if (value > 1.0) {
          this.$message.error('beta value must be smaller than 1!');
          this.$refs.betaRef.focus();
        }
      }
    },
    valAlpha() {
      if (this.alphaPara.length <= 0) {
        this.$message.error('alpha value can not be empty!');
        this.$refs.alphaRef.focus();
      } else {
        const value = parseFloat(this.alphaPara);
        if (value > 1.0) {
          this.$message.error('alpha value must be smaller than 1!');
          this.$refs.alphaRef.focus();
        }
      }
    },

    valPMin() {
      if (this.pMinPara.length <= 0) {
        this.$message.error('p_min value can not be empty!');
        this.$refs.pMinRef.focus();
      } else {
        const value = parseFloat(this.pMinPara);
        if (value > 1.0) {
          this.$message.error('p_min value must be smaller than 1!');
          this.$refs.pMinRef.focus();
        }
      }
    },
    valR() {
      if (this.rPara.length <= 0) {
        this.$message.error('r value can not be empty!');
        this.$refs.rRef.focus();
      }
    },
    valMutationFirstPara() {
      console.log('firstparavalue:', this.firstParaValue.length);
      if (this.firstParaValue.length <= 0) {
        this.$message.error('Threshold value can not be empty!');
        this.$refs.mutationFirstParaRef.focus();
      } else {
        const value = parseFloat(this.firstParaValue);
        if (value > 1.0) {
          this.$message.error('Threshold value must be smaller than 1!');
          this.$refs.mutationFirstParaRef.focus();
        }
      }
    },
    valMutationSecondPara() {
      if (this.secondParaValue.length <= 0) {
        this.$message.error('e value can not be empty!');
        this.$refs.mutationSecondParaRef.focus();
      } else {
        const value = parseFloat(this.secondParaValue);
        if (value > 1.0) {
          this.$message.error('e value must be smaller than 1!');
          this.$refs.mutationSecondParaRef.focus();
        }
      }
    },

    blurPAMParams(index, idx) {
      // 真实的输入
      const currentPara = this.pixAddedAttackCache[index].parameters[idx];
      const refKey = 'pixelInputRef' + index + idx;
      let needComma = true;
      let defaultMin = 0;
      let defaultMax = 0;
      // 这个地方需要先获取用户选择的攻击方法名，
      this.pixLAArrForReset.forEach(item => {
        if (item.method === this.currentChoosePAM) {
          const paraObj = item.parameter[idx];
          defaultMin = paraObj.min;
          defaultMax = paraObj.max;
          const commaIndex = paraObj.value.indexOf(',');
          // console.log('commaIndex:', commaIndex)
          // 如果服务器默认值含有逗号，才去按照有逗号验证
          if (commaIndex === -1) {
            needComma = false;
          }
        }
      });

      // 验证是否为空
      if (currentPara.value.length === 0) {
        this.$message.error(currentPara.name + ' value can not be empty!');
        this.$refs[refKey][0].focus();
        return;
      }

      let realMin = 0;
      let realMax = 0;
      // 判断是否有逗号
      if (needComma) {
        // 真实的输入分成两部分，一个最小值，一个最大值
        const rangeArr = currentPara.value.split(',');
        if (rangeArr.length !== 2) {
          this.$message.error(
            'The value of the ' + currentPara.name + ' is invalid and must contain a comma!',
          );
          this.$refs[refKey][0].focus();
        } else {
          if (currentPara.dtype === 'int') {
            realMin = parseInt(rangeArr[0]);
            realMax = parseInt(rangeArr[1]);
          } else if (currentPara.dtype === 'float') {
            realMin = parseFloat(rangeArr[0]);
            realMax = parseFloat(rangeArr[1]);
          }
          if (isNaN(realMin) || isNaN(realMax)) {
            this.$message.error('The entered number is incomplete');
            this.$refs[refKey][0].focus();
          } else {
            // 判断是否在最小和最大区间
            if (
              realMin < defaultMin ||
              realMin > defaultMax ||
              realMax < defaultMin ||
              realMax > defaultMax
            ) {
              this.$message.error(
                currentPara.name + ' must be between ' + defaultMin + ' and ' + defaultMax,
              );
              this.$refs[refKey][0].focus();
            }
          }
        }
      } else {
        let realValue = 0;
        if (currentPara.dtype === 'int') {
          realValue = parseInt(currentPara.value);
        } else if (currentPara.dtype === 'float') {
          realValue = parseFloat(currentPara.value);
        }
        if (realValue < defaultMin || realValue > defaultMax) {
          this.$message.error(
            currentPara.name + ' must be between ' + defaultMin + ' and ' + defaultMax,
          );
          this.$refs[refKey][0].focus();
        }
      }
    },

    blurCorrParams(index, idx) {
      // 真实的输入
      const currentPara = this.selectedCorr[index].parameters[idx];
      const refKey = 'corrInputRef' + index + idx;
      let needComma = true;
      let defaultMin = 0;
      let defaultMax = 0;
      // 这个地方需要先获取用户选择的攻击方法名，
      this.corrAttacksForReset.forEach(item => {
        if (item.method === this.currentChooseCAM) {
          const paraObj = item.parameter[idx];
          defaultMin = paraObj.min;
          defaultMax = paraObj.max;
          const commaIndex = paraObj.value.indexOf(',');
          // console.log('commaIndex:', commaIndex)
          // 如果服务器默认值含有逗号，才去按照有逗号验证
          if (commaIndex === -1) {
            needComma = false;
          }
        }
      });

      // 验证是否为空
      if (currentPara.value.length === 0) {
        this.$message.error(currentPara.name + ' value can not be empty!');
        this.$refs[refKey][0].focus();
        return;
      }

      let realMin = 0;
      let realMax = 0;
      // 判断是否有逗号
      if (needComma) {
        // 真实的输入分成两部分，一个最小值，一个最大值
        const rangeArr = currentPara.value.split(',');
        if (rangeArr.length !== 2) {
          this.$message.error(
            'The value of the ' + currentPara.name + ' is invalid and must contain a comma!',
          );
          this.$refs[refKey][0].focus();
        } else {
          if (currentPara.dtype === 'int') {
            realMin = parseInt(rangeArr[0]);
            realMax = parseInt(rangeArr[1]);
          } else if (currentPara.dtype === 'float') {
            realMin = parseFloat(rangeArr[0]);
            realMax = parseFloat(rangeArr[1]);
          }
          if (isNaN(realMin) || isNaN(realMax)) {
            this.$message.error('The entered number is incomplete');
            this.$refs[refKey][0].focus();
          } else {
            // 判断是否在最小和最大区间
            if (
              realMin < defaultMin ||
              realMin > defaultMax ||
              realMax < defaultMin ||
              realMax > defaultMax
            ) {
              this.$message.error(
                currentPara.name + ' must be between ' + defaultMin + ' and ' + defaultMax,
              );
              this.$refs[refKey][0].focus();
            }
          }
        }
      } else {
        let realValue = 0;
        if (currentPara.dtype === 'int') {
          realValue = parseInt(currentPara.value);
        } else if (currentPara.dtype === 'float') {
          realValue = parseFloat(currentPara.value);
        }
        if (realValue < defaultMin || realValue > defaultMax) {
          this.$message.error(
            currentPara.name + ' must be between ' + defaultMin + ' and ' + defaultMax,
          );
          this.$refs[refKey][0].focus();
        }
      }
    },

    blurSAMParams(index, idx) {
      const currentPara = this.semanticAddedAttackCache[index].parameters[idx];
      const refKey = 'semanticInputRef' + index + idx;
      let needComma = true;
      let defaultMin = 0;
      let defaultMax = 0;
      this.semanticLAArrForReset.forEach(item => {
        if (item.method === this.currentChooseSAM) {
          const paraObj = item.parameter[idx];
          defaultMin = paraObj.min;
          defaultMax = paraObj.max;
          const commaIndex = paraObj.value.indexOf(',');
          // 如果服务器默认值含有逗号，才去按照有逗号验证
          if (commaIndex === -1) {
            needComma = false;
          }
        }
      });

      if (currentPara.value.length === 0) {
        this.$message.error(currentPara.name + ' value can not be empty!');
        // When a ref is used inside a v-for loop,ref is an array of the elements/components
        // To focus the first, I'd do this.$refs['xxxRef'][0].focus()
        this.$refs[refKey][0].focus();
        return;
      }

      if (needComma) {
        const rangeArr = currentPara.value.split(',');

        if (rangeArr.length !== 2) {
          this.$message.error(
            'The value of the ' + currentPara.name + ' is invalid and must contain a comma!',
          );
          this.$refs[refKey][0].focus();
        } else {
          // 判断是否在最小和最大区间
          let realMin = 0;
          let realMax = 0;
          if (currentPara.dtype === 'int') {
            realMin = parseInt(rangeArr[0]);
            realMax = parseInt(rangeArr[1]);
          } else if (currentPara.dtype === 'float') {
            realMin = parseFloat(rangeArr[0]);
            realMax = parseFloat(rangeArr[1]);
          }
          if (isNaN(realMin) || isNaN(realMax)) {
            this.$message.error('The entered number is incomplete');
            this.$refs[refKey][0].focus();
          } else {
            if (
              realMin < defaultMin ||
              realMin > defaultMax ||
              realMax < defaultMin ||
              realMax > defaultMax
            ) {
              this.$message.error(
                currentPara.name + ' must be between ' + defaultMin + ' and ' + defaultMax,
              );
              this.$refs[refKey][0].focus();
            }
          }
        }
      } else {
        let realValue = 0;
        if (currentPara.dtype === 'int') {
          realValue = parseInt(currentPara.value);
        } else if (currentPara.dtype === 'float') {
          realValue = parseFloat(currentPara.value);
        }
        if (realValue < defaultMin || realValue > defaultMax) {
          this.$message.error(
            currentPara.name + ' must be between ' + defaultMin + ' and ' + defaultMax,
          );
          this.$refs[refKey][0].focus();
        }
      }
    },

    valDevice() {
      if (this.configForm.deviceInfo === '') {
        this.$message.error('please enter cpu string or a number!');
        this.$refs.deviceRef.focus();
      } else {
        const reg = new RegExp('^[0-9]*$');
        const isNumber = reg.test(this.configForm.deviceInfo);
        if (this.configForm.deviceInfo.toLowerCase() === 'cpu' || isNumber) {
        } else {
          this.$message.error('please enter cpu string or a number!');
          this.$refs.deviceRef.focus();
        }
      }
    },
    /**
     * 稍后下载
     * */
    downloadLater() {
      this.downYamlVisible = false;
      this.$router.push({
        name: 'robustness',
        params: {},
      });
    },
    /**
     * 重置pixel 攻击方法参数
     * */
    resetPixelParas(index, paramsIdx) {
      const target = this.pixAddedAttackCache[index];
      const methodStr = target.method;
      this.pixLAArrForReset.forEach(item => {
        if (item.method === methodStr) {
          target.parameters[paramsIdx].value = item.parameter[paramsIdx].value;
        }
      });
    },
    resetCorrParas(index, paramsIdx) {
      const target = this.selectedCorr[index];
      const methodStr = target.method;
      this.corrAttacksForReset.forEach(item => {
        if (item.method === methodStr) {
          target.parameters[paramsIdx].value = item.parameter[paramsIdx].value;
        }
      });
    },
    /**
     * 重置semantic 攻击方法参数
     * */
    resetSemanticParas(index, paramsIdx) {
      const target = this.semanticAddedAttackCache[index];
      this.semanticLAArrForReset.forEach(item => {
        if (item.method === target.method) {
          target.parameters[paramsIdx].value = item.parameter[paramsIdx].value;
        }
      });
    },

    /**
     * 下载Yaml文件
     * */
    downloadYaml() {
      this.downYamlVisible = false;
      const query = {
        task_id: this.newTaskId,
      };
      api.downloadYaml(query);
      this.$router.push({
        name: 'robustness',
        params: {},
      });
    },
    /**
     * 重置mutation 参数
     * */
    resetMutationParas() {
      this.firstParaValue = '0.75';
      this.actFnChoosedValue = [];
    },
    /**
     * 重置超参
     * */
    resetRuningParas() {
      this.pMinPara = 0.7;
      this.rPara = 20;
      this.alphaPara = 0.8;
      this.betaPara = 0.8;
      this.kTimePara = 5;
      this.tryNumPara = 30;
      this.maxIterPara = 500;
      this.batchSizePara = 8;

      this.binSize = 3;
    },
    /**
     * 监听 mutation guidance 变化
     * */
    mutationChange(val) {
      this.firstParaValue = '';
      this.secondParaValue = '';
      if (val === 'NC') {
        this.mutationFirstParasLabel = 'Threshold';
        this.mutationSecondParasLabel = '';
        this.firstParaValue = '0.75';
        this.secondParaValue = '';
        this.neuronParasVisiable = false;
      } else if (val === 'KMNC') {
        this.mutationFirstParasLabel = 'K_section';
        this.mutationSecondParasLabel = '';
        this.firstParaValue = '0.5';
        this.secondParaValue = '';
        this.neuronParasVisiable = false;
      } else if (val === 'Top-K') {
        this.mutationFirstParasLabel = 'K';
        this.mutationSecondParasLabel = '';
        this.firstParaValue = '0.5';
        this.secondParaValue = '';
        this.neuronParasVisiable = false;
      } else if (val === 'NeuronSensitivity') {
        this.mutationFirstParasLabel = 'Threshold';
        this.mutationSecondParasLabel = 'e:';
        this.firstParaValue = '0.75';
        this.secondParaValue = '0.5';
        this.neuronParasVisiable = true;
      }
    },

    /**
     * 回退编辑
     * */
    backToEdit(stepIndex) {
      this.stepActive = stepIndex;
      if (stepIndex === 0) {
        this.modelDivVisiable = true;
        this.datasetDivVisiable = false;
        this.configDivVisiable = false;
        this.previewDivVisiable = false;
      } else if (stepIndex === 1) {
        this.modelDivVisiable = false;
        this.datasetDivVisiable = true;
        this.configDivVisiable = false;
        this.previewDivVisiable = false;
      } else if (stepIndex === 2) {
        this.modelDivVisiable = false;
        this.datasetDivVisiable = false;
        this.configDivVisiable = true;
        this.previewDivVisiable = false;
      }
    },

    /**
     * 预览
     * */
    toPreview() {
      this.pixelPreviewList = [];
      this.semanticPreviewList = [];
      this.corrPreviewList = [];
      const isWhite = this.modelType === 'white box';
      const isBlack = this.modelType === 'black box';

      if (isWhite) {
        if (this.actFnChoosedValue.length === 0) {
          this.$message.error('please choose one activate function at least!');
          return;
        }
        if (this.pixAddedAttackCache.length === 0 && this.selectedCorr.length === 0) {
          this.$message.error('Pixel level and corruption select one at least!');
        }
        if (this.semanticAddedAttackCache.length === 0) {
          this.$message.error('please add one semantic level attack method at least!');
          return;
        }
      }

      if (isBlack) {
        if (this.modelForm.modelAlgType === 'classification') {
          if (
            this.pixAddedAttackCache.length === 0 &&
            this.semanticAddedAttackCache.length === 0 &&
            this.selectedCorr.length === 0
          ) {
            this.$message.error(
              'Pixel level and semantic level and corruption select one at least!',
            );
            return;
          }
        }
        if (this.isObjDet) {
          if (this.pixAddedAttackCache.length === 0 && this.selectedCorr.length === 0) {
            this.$message.error('Pixel level and corruption select one at least!');
            return;
          }
        }
      }

      this.stepActive++;
      const pixLevel = [];
      const that = this;
      this.pixAddedAttackCache.forEach(function(ele) {
        const ampArray = [];
        let preStr = '(';
        ele.parameters.forEach(function(amp) {
          const pobj = {
            name: amp.name,
            value: amp.value,
            dtype: amp.dtype,
          };
          preStr += amp.name + ':' + amp.value + ' ';
          ampArray.push(pobj);
        });

        const tempobj = {
          method: ele.method,
          parameters: ampArray,
        };
        preStr = ele.method + ' ' + preStr + ')';
        that.pixelPreviewList.push(preStr);
        pixLevel.push(tempobj);
      });

      const semanticLevel = [];

      this.semanticAddedAttackCache.forEach(function(ele) {
        const ampArray = [];
        let preStr = '(';
        ele.parameters.forEach(function(amp) {
          const pobj = {
            name: amp.name,
            value: amp.value,
            dtype: amp.dtype,
          };
          preStr += amp.name + ':' + amp.value + ' ';
          ampArray.push(pobj);
        });

        const tempobj = {
          method: ele.method,
          parameters: ampArray,
        };
        preStr = ele.method + ' ' + preStr + ')';
        that.semanticPreviewList.push(preStr);
        semanticLevel.push(tempobj);
      });

      const corrLevel = [];

      this.selectedCorr.forEach(function(ele) {
        const ampArray = [];
        let preStr = '(';
        ele.parameters.forEach(function(amp) {
          const pobj = {
            name: amp.name,
            value: amp.value,
            dtype: amp.dtype,
          };
          preStr += amp.name + ':' + amp.value + ' ';
          ampArray.push(pobj);
        });

        const tempobj = {
          method: ele.method,
          parameters: ampArray,
        };
        preStr = ele.method + ' ' + preStr + ')';
        that.corrPreviewList.push(preStr);
        corrLevel.push(tempobj);
      });

      const mutationParas = {};
      if (this.mutationValue === 'NC') {
        mutationParas.threshold = parseFloat(this.firstParaValue);
        mutationParas.act_fn = this.actFnChoosedValue;
      } else if (this.mutationValue === 'KMNC') {
        mutationParas.k_section = parseFloat(this.firstParaValue);
        mutationParas.act_fn = this.actFnChoosedValue;
      } else if (this.mutationValue === 'TopK') {
        mutationParas.k = parseFloat(this.firstParaValue);
        mutationParas.act_fn = this.actFnChoosedValue;
      } else if (this.mutationValue === 'NeuronSensitivity') {
        mutationParas.threshold = parseFloat(this.firstParaValue);
        mutationParas.e = parseFloat(this.secondParaValue);
        mutationParas.act_fn = this.actFnChoosedValue;
      }

      let params = {};

      if (this.isWhite) {
        params = {
          mutation_guidance: this.mutationValue,
          mutation_params: mutationParas,

          p_min: parseFloat(this.pMinPara),
          r: parseInt(this.rPara),
          alpha: parseFloat(this.alphaPara),
          beta: parseFloat(this.betaPara),
          k_time: parseInt(this.kTimePara),
          try_num: parseInt(this.tryNumPara),
          max_iter: parseInt(this.maxIterPara),
          batch_size: parseInt(this.batchSizePara),
        };
      } else {
        params = {
          bin_size: this.binSize,
        };
        if (this.isObjDet) {
          params = {
            ...params,
            input_output_params: this.ioForm,
            iou: this.iou,
            bbox_type: this.datasetForm.bboxType,
            scale: this.datasetForm.scale,
          };
        }
      }

      // todo
      this.initHyperParameters = {
        task_type: this.modelForm.modelAlgType,
        // dataset_format: this.datasetForm.datasetFormat,
        model_framework: this.modelForm.modelFramework,
        domain: this.modelForm.modelDomain,
        device: this.configForm.deviceInfo,
        model_type: this.modelType,
        pixel_level: pixLevel,
        semantic_level: semanticLevel,
        corruption: corrLevel,
        ...params,
      };
      // 提前组装 mutation 需要显示的信息
      let actValueStr = '';
      this.actFnChoosedValue.forEach(function(ele) {
        actValueStr += ele + ' ';
      });

      if (this.mutationSecondParasLabel === '') {
        this.previewMutationValue =
          this.mutationValue +
          '[' +
          this.mutationFirstParasLabel +
          ':' +
          this.firstParaValue +
          ';' +
          'Activate Function:' +
          actValueStr +
          ']';
      } else {
        this.previewMutationValue =
          this.mutationValue +
          '[' +
          this.mutationFirstParasLabel +
          ':' +
          this.firstParaValue +
          ';' +
          this.mutationSecondParasLabel +
          ':' +
          this.secondParaValue +
          actValueStr +
          ']';
      }

      this.previewDivVisiable = true;
      this.configDivVisiable = false;
      this.modelDivVisiable = false;
      this.datasetDivVisiable = false;
    },
    /**
     * 创建鲁棒性任务
     */
    createRobustTask() {
      const that = this;
      const requestBody = {
        table: this.datasetForm.datasetTable,
        table_version: this.datasetForm.datasetTableVersion,
        task_type: '0',
        model_path: this.modelForm.modelPath,
        data_path: this.datasetForm.dataPath,
        init_hyperparameter: this.initHyperParameters,
        algorithm_type: this.modelForm.modelAlgType === 'classification' ? '0' : '1',
        description: this.modelForm.modelTaskDesc,
        machine_info: '',
      };
      api.createTask(requestBody).then(ret => {
        console.log(' ret :', JSON.stringify(ret));
        that.newTaskId = ret.data.task_id;
        that.downYamlVisible = true;
      });
    },
    /**
     * 验证字符输入的是否为文件路径
     */
    validFilePath(filePath) {
      return filePath.startsWith('/');
    },

    /**
     * 第一次请求页面数据
     * initColumns初始化完成后调用
     * 可以用一个空方法覆盖它，阻止初始化后请求数据
     */
    doLoad() {},
    /**
     * 验证Model form
     */
    validModel(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (this.validFilePath(this.modelForm.modelPath)) {
            this.stepActive++;
            this.modelDivVisiable = false;
            this.datasetDivVisiable = true;
            this.configDivVisiable = false;
          } else {
            this.$message.error('Please enter a valid file path!');
          }
        } else {
          return false;
        }
      });
    },

    /**
     * 验证dataset form
     * */
    validDatasetForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (this.validFilePath(this.datasetForm.dataPath)) {
            this.stepActive++;
            this.modelDivVisiable = false;
            this.datasetDivVisiable = false;
            this.configDivVisiable = true;
          } else {
            this.$message.error('Please enter a valid file path!');
          }
        } else {
          return false;
        }
      });
    },
    /**
     * 增加semantic 攻击方法参数
     * */
    addPixelAttact() {
      // 每次添加的时候先加载一个空的对象
      const defaultATM = {
        id: this.pixelAMId,
        method: '',
        parameters: [],
      };
      this.pixAddedAttackCache.push(defaultATM);
      this.pixelAMId++;

      this.beforeAddPixelAM = this.pixAddedAttackCache.map(x => x.method);
    },

    delPixelAttact(index) {
      this.pixAddedAttackCache.splice(index, 1);
    },

    addCorrAttact() {
      // 每次添加的时候先加载一个空的对象
      const defaultATM = {
        id: this.pixelAMId,
        method: '',
        parameters: [],
      };
      this.selectedCorr.push(defaultATM);
      this.pixelAMId++;

      this.beforeAddCorr = this.selectedCorr.map(x => x.method);
    },
    delCorr(index) {
      this.selectedCorr.splice(index, 1);
    },

    addSemanticAttact() {
      // 每次添加的时候先加载一个空的对象
      const defaultATM = {
        id: this.pixelAMId,
        method: '',
        parameters: [],
      };
      this.semanticAddedAttackCache.push(defaultATM);
      this.pixelAMId++;
      this.beforeAddSemanticAM = this.semanticAddedAttackCache.map(x => x.method);
    },

    delSemanticAttact(index) {
      this.semanticAddedAttackCache.splice(index, 1);
    },

    /**
     * 监听切换table
     */
    handleDomainChange(val) {},

    /**
     * 监听切换table
     */
    handlePixelChange(val, index) {
      if (
        this.beforeAddPixelAM.find(function(element) {
          return element === val;
        })
      ) {
        this.$message.error('the method is added already,please choose another one!');
        this.pixAddedAttackCache[index].method = '';
      } else {
        this.currentChoosePAM = val;
        const chooseParams = this.pixLeveAttackArr.find(function(element) {
          return element.method === val;
        });
        this.pixAddedAttackCache[index].parameters = chooseParams.parameters;
      }
    },

    handleCorrChange(val, index) {
      if (
        this.beforeAddCorr.find(function(element) {
          return element === val;
        })
      ) {
        this.$message.error('the method is added already,please choose another one!');
        this.selectedCorr[index].method = '';
      } else {
        this.currentChooseCAM = val;
        const chooseParams = this.corrAttacks.find(function(element) {
          return element.method === val;
        });
        this.selectedCorr[index].parameters = chooseParams.parameters;
      }
    },

    handleSemanticChange(val, index) {
      if (
        this.beforeAddSemanticAM.find(function(element) {
          return element === val;
        })
      ) {
        this.$message.error('the method is added already,please choose another one!');
        this.semanticAddedAttackCache[index].method = '';
      } else {
        this.currentChooseSAM = val;
        const chooseParams = this.semanticLeveAttackArr.find(function(element) {
          return element.method === val;
        });
        this.semanticAddedAttackCache[index].parameters = chooseParams.parameters;
      }
    },
    /**
     * 监听切换table
     */
    handleTableChange(val) {
      if (val === '-1') {
        this.$confirm('Do you want to new table?', 'Warning', {
          confirmButtonText: 'OK',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }).then(() => {
          this.$router.push({ name: 'dataManagement' });
        });
      }
      this.pixelCurrentMethod = val;
      this.table_id = val;
      const finded = this.tableArr.find(function(element) {
        return element.value === val;
      });
      this.previewTabelName = finded.label;
      this.getVersion(val);
    },

    handleModelTypeChange(val) {
      this.resetAllAttackMethod();
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

    resetAllAttackMethod() {
      this.pixLeveAttackArr = [];
      this.pixLAArrForReset = [];
      this.semanticLeveAttackArr = [];
      this.semanticLAArrForReset = [];
      this.corrAttacks = [];
      this.corrAttacksForReset = [];

      this.getAttackMethods(0);
      this.getAttackMethods(1);
      this.getAttackMethods(2);
    },
    /**
     * 获取所有表格列表
     */
    getAttackMethods(attackType) {
      const that = this;
      const query = {
        model_type: that.modelType === 'white box' ? 0 : 1,
        attack_type: attackType,
      };
      api.GetAttackMethods(query).then(ret => {
        for (const item of ret.data) {
          const wrapItem = that.wrapAttackMethod(item);
          if (attackType === 0) {
            that.pixLeveAttackArr.push(wrapItem);
            that.pixLAArrForReset.push(item);
          } else if (attackType === 1) {
            that.semanticLeveAttackArr.push(wrapItem);
            that.semanticLAArrForReset.push(item);
          } else if (attackType === 2) {
            that.corrAttacks.push(wrapItem);
            that.corrAttacksForReset.push(item);
          }
        }
      });
    },

    wrapAttackMethod(item) {
      const paras = item.parameter.map(s => {
        return {
          id: this.pixelLevelAMId++,
          name: s.name,
          value: s.value,
          min: s.min,
          max: s.max,
          dtype: s.dtype,
        };
      });
      const wrapItem = {
        method: item.method,
        parameters: paras,
      };
      return wrapItem;
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
    goDataManagement() {
      this.$router.push({
        path: '/api/prosafeai/data_management',
        query: {},
      });
    },

    /**
     *  隐藏表格
     */
    afterInit() {
      this.crud.options.hide = true;
    },
    /**
     *  获取表格配置
     */
    getCrudOptions() {
      return crudOptions(this);
    },
  },
};
</script>

<style lang="scss" scoped>
.io-form {
  display: grid;
  grid-template-columns: 50% 50%;
  .el-select,
  .el-input {
    width: 160px;
  }
}
.select-filter {
  width: 220px;
}

.dialog-footer {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}

.dialog-body-style {
  display: flex;
  flex-display: row;
  align-items: center;
  padding: 10px 40px 10px 40px;
}

::v-deep .d2-crud-body {
  overflow: auto;
}

.dialog {
  position: relative;
}

.icon-runningpara {
  position: absolute;
  width: 70px;
  bottom: 0;
  right: 0;
  transform: translate(-10%, -90%);
}

.edit-button {
  position: absolute;
  width: 70px;
  top: 4px;
  right: 0;
  transform: translate(-10%, -90%);
}

.addattack {
  margin-top: 10px;
}

.criteria-params {
  background-color: #b9def0;
  margin-top: 10px;
  border-radius: 5px;
  padding: 8px;
}

.config-preview {
  display: flex;
  flex-direction: column;
  background-color: #b9def0;
  margin-top: 10px;
  border-radius: 5px;
  padding: 8px;
}

.model-params {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 5px;
}

.runing-params {
  display: flex;
  background-color: #b9def0;
  margin-top: 10px;
  border-radius: 5px;
  padding: 8px;
  margin-top: 10px;
}
.obj-det-ctn {
  background-color: #b9def0;
  margin-top: 10px;
  border-radius: 5px;
  padding: 8px;
  margin-top: 10px;
}

.params-desc {
  margin-left: 2px;
  color: #999;
}

.hyperpara-label {
  display: flex;
  align-items: center;
}

.hyperpara-half {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-top: 5px;
  justify-content: space-between;
}

.fristpara-input {
  width: 100px;
  padding: 1px;
}

.short-input {
  width: 70px;
  padding: 1px;
}

.el-step__main {
  width: 100% !important;
}

.step-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 30px;
  width: 100%;
  padding: 0px;
}

.content-div {
  display: flex;
  justify-content: center;
  border-style: solid;
  border-color: #f2f2f2;
  border-width: 1px;
  border-radius: 10px;
  height: 100%;
  padding: 20px 30px 20px 30px;
  margin: 20px 30px;
  background-color: #f2f2f2;
}

.content-div span {
  margin-right: 10px;
}
.templHeader {
  font-size: 16px;
  font-weight: 600;
  padding: 12px 0;
}
</style>
