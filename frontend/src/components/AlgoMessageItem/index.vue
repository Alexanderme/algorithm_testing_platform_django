<template>
  <div>
    <el-alert :title="iasRes" type="success"  effect="dark" :closable="false"></el-alert>
    <br>
    <el-alert :title="privateKey" type="success"  effect="dark" :closable="false"></el-alert>
    <br>
    <el-alert :title="algo_configs" type="success"  effect="dark" :closable="false"></el-alert>
    <div class="iasResShow">
      <el-input placeholder="请输入内容" v-model="image_name">
        <template slot="prepend">镜像名称</template>
        </el-input>
    </div>
    <el-button type="primary" @click="getSdkOpenCVData()">提交</el-button>
  </div>

</template>

<script>
    import { getSdkOpenCV } from "../../api/algoSdk";
    export default {
        inject:['reload'],
        name: "index",
        data(){
          return{
            image_name:"",
            iasRes:"请输入您需要查看的算法镜像",
            isLoding:false,
            privateKey:"私钥:注意只支持3.0算法",
            algo_configs: "算法配置:注意只支持3.0算法"
          }
        },
        methods:{
            getSdkOpenCVData(){
                const loading = this.$loading({
                lock: true,
                text: 'Loading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'});

                let params = new URLSearchParams()
                params.append('image_name', this.image_name)
                getSdkOpenCV(params).then((res) => {
                  this.isLoding = true
                  if (this.isLoding){loading.close();}
                  if(res){
                        if(res.errno === "0"){
                          this.iasRes = res.errmsg
                          this.privateKey = res.privateKey
                          this.algo_configs = res.algo_config
                        }
                        else{
                          this.iasRes = res.errmsg
                        }
                    }
                    else {
                        this.iasRes = res.errmsg
                    }
                }).then(res =>{
                    this.reload();
                })
            },
        }
    }
</script>

<style scoped>
.iasResShow{
  margin-top: 20px;
}
.el-alert{
    height: auto;
    width: auto;
    white-space:pre
  }

</style>
