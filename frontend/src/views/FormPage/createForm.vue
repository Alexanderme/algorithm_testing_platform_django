<template>
  <div class="create-from">
    <el-form ref="form" :model="formInfo" label-width="60px" label-position="left" size="medium">
      <div class="components-wrap">
        <input-focus v-model="formInfo.title" bolder class="mrb"></input-focus>
        <el-row :gultter="20">
          <el-col :xs="8" :md="6">
            <el-form-item label="作者：">
              <el-select
                v-model="formInfo.author"
                filterable
                remote
                reserve-keyword
                :remote-method="remoteMethod"
                :loading="loading"
                popper-class="author-select"
                placeholder="搜索用户">
                <el-option
                  v-for="item in authorDB"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                  <span style="float: left">{{ item.label }}</span>
                  <span style="float: right;">选择</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="8" :md="6">
            <el-form-item label="来源：">
              <el-select
                v-model="formInfo.source"
                filterable
                placeholder="搜索用户">
                <el-option
                  v-for="item in authorDB2"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                  <span style="float: left">{{ item.label }}</span>
                  <span style="float: right;">选择</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="摘要：" class="mrb create-summary">
          <el-input
            v-model="formInfo.summary"
            type="textarea">
          </el-input>
          <span class="word-counter">{{ summaryCount }}</span>
        </el-form-item>
        <div class="editor-box">
          <p v-for="item in 100" :key="item">editor placeholder{{ item }}</p>
        </div>
      </div>
    </el-form>
  </div>
</template>

<script>
export default {
  components: {
    InputFocus
  },
  data () {
    return {
      platformOpt: [
        {
          label: '运营部',
          value: 'A'
        },
        {
          label: '市场部',
          value: 'B'
        }
      ],
      loading: false,
      formInfo: {
        title: '',
        publicDate: '',
        platform: '',
        author: '',
        source: '',
        summary: ''
      },
      list: [],
      authorDB: [],
      authorMockStates: ['Alabama', 'Alaska', 'Arizona',
        'Arkansas', 'California', 'Colorado',
        'Connecticut', 'Delaware', 'Florida',
        'Georgia', 'Hawaii', 'Idaho', 'Illinois',
        'Indiana', 'Iowa', 'Kansas', 'Kentucky',
        'Louisiana', 'Maine', 'Maryland',
        'Massachusetts', 'Michigan', 'Minnesota',
        'Mississippi', 'Missouri', 'Montana',
        'Nebraska', 'Nevada', 'New Hampshire',
        'New Jersey', 'New Mexico', 'New York',
        'North Carolina', 'North Dakota', 'Ohio',
        'Oklahoma', 'Oregon', 'Pennsylvania',
        'Rhode Island', 'South Carolina',
        'South Dakota', 'Tennessee', 'Texas',
        'Utah', 'Vermont', 'Virginia',
        'Washington', 'West Virginia', 'Wisconsin',
        'Wyoming'],
      authorDB2: [
        {
          label: '王羲之',
          value: '王羲之'
        },
        {
          label: '李白',
          value: '李白'
        }
      ],
      counter: 0
    }
  },
  mounted () {
    this.list = this.authorMockStates.map((item) => {
      return {
        value: item,
        label: item
      }
    })
  },
  methods: {
    publishBtn () {
      this.$message('发布成功')
    },
    remoteMethod (query) {
      if (query !== '') {
        this.loading = true
        setTimeout(() => {
          this.loading = false
          this.authorDB = this.list.filter((item) => {
            return item.label.toLowerCase().indexOf(query.toLowerCase()) > -1
          })
        }, 200)
      } else {
        this.authorDB = []
      }
    }
  },
  computed: {
    summaryCount () {
      return this.formInfo.summary.length <= 0 ? '' : this.formInfo.summary.length + '字'
    }
  }
}
</script>

<style lang="scss">
@import '../../styles/mixin.scss';
.create-from{
  .s-right{
    text-align: right;
  }
  .mrb{
    @include mr(35px);
  }
  .el-select .el-input.is-focus .el-input__inner{
    border-color: $borderColor;
  }
  .el-select .el-input__inner:focus{
    border-color: $borderColor;
  }
  .el-select-dropdown__item.select{
    color: #fff !important;
    background-color: rgb(67, 161, 201) !important;
  }
  .el-form-item__label{
    font-weight: bold;
  }
  .create-summary{
    position: relative;
    .el-textarea__inner{
      min-height: 32px;
      height: 32px;
    }
    textarea{
      padding-right: 40px;
      resize: none;
      border: none;
      border-radius: 0;
      border-bottom: 1px solid #bfcbd9;
    }
    .word-counter{
      @include abs(auto, 0, 0, auto);
      color: #999;
    }
  }
}
</style>
