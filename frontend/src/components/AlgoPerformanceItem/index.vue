<template>
  <div>
    <el-alert :title="iasRes"  effect="dark" :closable="false" type="success"></el-alert>
    <div class="center">
      <el-input placeholder="请输入镜像名称" v-model="image_name">
      <template slot="prepend">镜像名称</template></el-input>
    </div>
    <div class="center">
      <el-input placeholder="请输入服务器IP" v-model="server_ip">
      <template slot="prepend">服务器IP</template></el-input>
    </div>
    <div class="center">
      <el-input placeholder="请输入服务器端口" v-model="server_port">
      <template slot="prepend">服务器端口</template></el-input>
    </div>
    <div class="center">
      <el-input placeholder="请输入服务器账号" v-model="server_user">
      <template slot="prepend">服务器账号</template></el-input>
    </div>
    <div class="center">
      <el-input placeholder="请输入服务器密码" v-model="server_passwd">
      <template slot="prepend">服务器密码</template></el-input>
    </div>
    <el-upload
             ref="upload"
             accept=".jpg"
             :file-list="fileList"
             :limit='1'
             :action="uploadUrl"
             :before-upload="getAlgoResourceOccupationData"
             :show-file-list="true"
             :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload()">提交请求</el-button>
            <div slot="tip" class="el-upload__tip">注意:上传文件只支持单个jpg文件</div>
          </el-upload>
  </div>
</template>

<script>
  import { getAlgoResourceOccupation} from "../../api/algoSdk";
    export default {
        inject:['reload'],
        name: "index",
        data(){
          return{
            fileList:[],
            uploadUrl:"",
            image_name:"",
            server_ip:"",
            server_port:"",
            server_user:"",
            server_passwd:"",
            iasRes:"注意:只是查看算法在服务器上的资源占用, 并且部分服务器连接存在失败的情况, 为了保证数据准确性, 请不要操作服务器, 本次运行大约5分钟时间,请不要操作界面"
          }
        },
        methods:{
          dataNotEnough() {
            this.$message.error('输入参数不完整, 请检查输入参数');
          },
          getAlgoResourceOccupationData(file){
            const loading = this.$loading({
            lock: true,
            text: 'Loading',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'});
            let formData = new FormData()
            formData.append('pic_file', file)
            formData.append('server_ip', this.server_ip)
            formData.append('server_port', this.server_port)
            formData.append('server_user', this.server_user)
            formData.append('server_passwd', this.server_passwd)
            formData.append('image_name', this.image_name)
            if (this.server_ip === "" || this.server_port === "" || this.server_user==="" || this.server_passwd==="" || this.image_name===""){
              this.dataNotEnough()
              this.reload();
              loading.close()
              return
            }
            getAlgoResourceOccupation(formData).then((res) => {
              this.isLoding = true
              if(res.errno === "0"){
                this.iasRes = String(res.errmsg)
                if (this.isLoding){loading.close();}
              }
              else{
                this.iasRes = res.errmsg
                if (this.isLoding){loading.close();}
              }
            }).then(res =>{
              this.reload();
            })
          },
          submit() {
             this.$nextTick(() => {
                 this.$refs.upload.submit()
             })
           },
          submitUpload() {
            this.$refs.upload.submit();
          },
        }
    }
</script>

<style scoped>
.center{
  margin: 10px 0;
}
</style>
