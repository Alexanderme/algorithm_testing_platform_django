<template>
  <div class="fix-type">
    <el-tabs v-model="activeName">
    <el-tab-pane label="符合标准算法" name="first">
      <el-alert :title="iasRes"  effect="dark" :closable="false" type="success"></el-alert>
      <div class="elinput">
        <el-input placeholder="例如alert_info, 需要和算法一一对应(可以运行'算法文件结果功能'查看)" v-model="alert_info">
          <template slot="prepend">算法INFO字段</template>
        </el-input>
      </div>
      <div class="elinput">
        <el-input placeholder="例如no_clothes, 多个标签以逗号分隔例如no_clothes,clothes" v-model="tag_names">
          <template slot="prepend">比对算法标签</template>
        </el-input>
      </div>
       <div class="elinput">
        <el-input placeholder="请输入算法镜像名称" v-model="image_name">
          <template slot="prepend">镜像名称</template>
        </el-input>
      </div>
      <div class="elinput">
        <el-input placeholder="请输入内容, 例如0.5, 可以不填 默认是0.5" v-model="iou">
          <template slot="prepend">比对IOU</template>
        </el-input>
      </div>
      <div class="elinput">
        <el-input placeholder="请输入内容, 例如修改算法roi或者阈值(需要和算法配置一致,可以运行算法信息查看算法配置), 默认可以不填" v-model="args">
          <template slot="prepend">参数配置</template>
        </el-input>
      </div>
      <div class="elinput">
        <span>如果是GPU安全帽算法请选择:&nbsp;&nbsp;&nbsp;</span>
        <el-radio v-model="radio_hat" label="gpu">GPU</el-radio>
      </div>
      <div>
        <span>注意:因为CPU算法输出比较特殊, 输出内容已做处理, CPU安全帽结果标签为:hat, head  如果为helemt获取其他标签.请单独处理替换标签为hat,head</span>
      </div>
       <div class="elinput">
          <el-upload
           ref="upload"
           accept=".zip"
           :file-list="fileList"
           :limit='1'
           :action="uploadUrl"
           :before-upload="getAlgoPrecisionData"
           :show-file-list="true"
           :auto-upload="false">
          <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
          <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload();getMissRateTaskIdData()">提交请求</el-button>
          <div slot="tip" class="el-upload__tip">注意:动态传参配置参数目前只支持3.0版本, 只能上传打包好的zip文件, 准确率测试只支持图片</div>
        </el-upload>
      </div>
    </el-tab-pane>
    <el-tab-pane label="不符合标准算法" name="second"></el-tab-pane>
      <div class="process">
        <span>运行进度条</span>
        <el-progress :percentage="percentage" :color="customColor"></el-progress>
      </div>
    </el-tabs>
      <div class="alert-button">
        <el-button v-if="false"></el-button>
      </div>
  </div>

</template>

<script>
  import {getMissRateTaskId, getAlgoPrecision} from "../../api/algoSdk";
  export default {
    inject:['reload'],
    data() {
      return {
        fileList:[],
        activeName: 'first',
        alert_info: '',
        tag_names: '',
        iou:"",
        uploadUrl:"",
        iasRes:"1:不支持2.0算法  2:安全帽算法比较特殊已做单独处理 3:目前已验证支持口罩,反光衣,工作帽,火焰,烟雾",
        isLoding:false,
        image_name:"",
        args:"",
        task_id:"",
        percentage: 0,
        customColor: '#409eff',
        is_update:false,
        radio_hat:""
      };
    },
    methods: {
      dataNotEnough() {
        this.$message.error('输入参数不完整, 请检查输入参数');
      },
      getAlgoPrecisionData(file){
          if(this.is_update){
            this.open()
            this.$router.go(0)
          }
          const loading = this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'});
          if (this.tag_names ==="" || this.alert_info==="" || this.image_name===""){
            this.dataNotEnough()
            this.reload();
            return
          }
          let formData = new FormData()
          formData.append('files', file)
          formData.append('tag_names', this.tag_names)
          formData.append('alert_info', this.alert_info)
          formData.append('image_name', this.image_name)
          if (this.args!==""){
             formData.append('args', this.args)
          }
          if (this.iou!=="") {
            formData.append('iou', this.iou)
          }
          if (this.radio_hat!=="") {
            formData.append('hat', this.radio_hat)
          }
          getAlgoPrecision(formData).then((res) => {
            this.task_id = res.task_id
            this.isLoding = true
            if (this.isLoding){loading.close();}
          }).then(res=>{
            this.reload();
          })
      },
     getMissRateTaskIdData(){
            if (this.fun_stop === true){
              this.reload();
              return
            }
            this.timer = window.setInterval(() => {
            setTimeout(() => {
            if (this.task_id !== null) {
              let taskId = {"task_id": this.task_id}
              getMissRateTaskId(taskId).then((res) => {
                if (res.state === "SUCCESS") {
                  this.iasRes = res.result
                  this.increase(res.state)
                  window.clearInterval(this.timer)
                  this.is_update = true
                } else {
                  this.status = res.status;
                  this.increase(this.status)
                }
              })
            }
          }, 1)
        }, 3000);
       },
    increase(status) {
        if (status === "SUCCESS"){
          this.percentage = 100
        }
        else{
          if (typeof(status)=="number"){
            this.percentage = status
          }
        }
        if (this.percentage > 100) {
          this.percentage = 100;
        }
      },
    submit() {
       this.$nextTick(() => {
           this.$refs.upload.submit()
       })
     },
     submitUpload() {
        this.$refs.upload.submit();
      }
    },
    open() {
        this.$alert('已完成一轮测试页面需要刷新, 点击确定页面将会刷新', '刷新页面', {
          confirmButtonText: '确定',
          callback: action => {
            this.$message({
              type: 'info',
              message: `action: ${ action }`
            });
          }
        });
      },
  };
</script>

<style scoped>
  .fix-type{
  margin-left: 20px;
}
.elinput{
  margin: 10px 100px 10px 0;
}
.el-alert {
    height: auto;
    width: auto;
    white-space:pre
}
</style>
