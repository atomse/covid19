<template>
  <div style="height:100%" class="app-container">
    <parse-chemio-component ref="chemioComponent" :on-success="handleSuccess" :before-upload="beforeUpload" />
    <!-- <el-table :data="tableData" border highlight-current-row style="width: 100%;margin-top:20px;">
      <el-table-column v-for="item of tableHeader" :key="item" :prop="item" :label="item" />
    </el-table>-->
    <el-input v-model="chemioResult" type="textarea" class="chemio-result-container" />
    <div class="bottom-button">
      <el-button v-clipboard:copy="chemioResult" v-clipboard:success="clipboardSuccess" class="chemio-button" type="primary" icon="el-icon-share">
        Copy
      </el-button>
      <el-button class="chemio-button" icon="el-icon-edit" type="danger" @click="downloadResult">
        Download
      </el-button>
    </div>
  </div>
</template>

<script>
import ParseChemioComponent from '@/components/ParseChemio/index.vue'
import clip from '@/utils/clipboard' // use clipboard directly
import clipboard from '@/directive/clipboard/index.js' // use clipboard by v-directive

const extension = {
  'json': '.json',
  'gaussian': '.gjf',
  'adf': '.run',
  'cp2k': '.inp',
  'POSCAR': '.vasp',
  'orca': '.inp',
  'xyz': '.xyz',
  'nwchem': '.nw',
  'gromacs': '.gro',
  'abinit': '.abinit'
}

export default {
  name: 'ParseChemio',
  components: { ParseChemioComponent },
  directives: {
    clipboard
  },
  data() {
    return {
      chemioResult: '',
      chemioPlaceHolder: 'You can use `pip install chemio --user --upgrade` to install chemio and use it on Linux'
    }
  },
  methods: {
    beforeUpload(file) {
      const isLt100M = file.size / 1024 / 1024 < 100

      if (isLt100M) {
        return true
      }

      this.$message({
        message: 'Please do not upload files larger than 100m in size.',
        type: 'warning'
      })
      return false
    },
    handleSuccess(results) {
      this.chemioResult = results
    },
    clearResult() {
      this.chemioResult = ''
    },
    handleCopy(text, event) {
      clip(text, event)
    },
    clipboardSuccess() {
      this.$message({
        message: 'Copy successfully',
        type: 'success',
        duration: 1500
      })
    },
    downloadResult() {
      var textToWrite = this.chemioResult
      if (textToWrite.length < 0) return
      var writeFormat = this.$refs.chemioComponent.writeFormat
      var fileNameToSaveAs = writeFormat
      if (extension[writeFormat]) fileNameToSaveAs += extension[writeFormat]
      var textFileAsBlob = new Blob([textToWrite], { 'type': 'application/octet-stream' })
      var downloadLink = document.createElement('a')
      downloadLink.download = fileNameToSaveAs
      downloadLink.innerHTML = ''
      downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob)
      downloadLink.click()
    }
  }
}
</script>

<style>
.chemio-result-container{
  margin: 0 auto;
  border-left:50px solid white;
  border-right:50px solid white;
  border-top: 50px solid white;
  height: 400px;
  text-align: center;
}
.el-textarea__inner{
  width: 100%;
  height: 100%;
  resize: none;
  background-color: #dad4d4;
}
.chemio-button{
  margin-top:20px;
  margin-left:20px;
  margin-right:20px;
}
.el-button + .el-button{
  margin-left:20px;
}
.bottom-button{
  margin: 0  auto;
  margin-bottom: 40px;
  text-align: center;
  position: relative;
}
</style>
