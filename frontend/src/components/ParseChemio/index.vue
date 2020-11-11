<template>
  <el-form ref="form" label-width="120px">
    <input ref="chemio-upload-input" name="chemioFile" class="chemio-upload-input" type="file" @change="handleClick">
    <div class="drop" @drop="handleDrop" @dragover="handleDragover" @dragenter="handleDragover">
      <el-input ref="formMessager" v-model="formMessage" class="input-contain-file" type="text" disabled="disabled" style="max-width:70%;height:40px;font-size:20px" />
      <el-button :loading="loading" style="margin-left:16px;" size="mini" type="primary" @click="handleUpload">
        Browse
      </el-button>
      <br>
    </div>
    <el-form-item class="to-type-el-form-item" label="To type">
      <el-radio-group v-model="writeFormat" class="to-type-el-radio-group" @change="handlePropertyChange">
        <el-radio v-for="type in showRadioTypes" :key="type" class="to-type-el-radio" :label="type">{{ type.toUpperCase() }}</el-radio>
      </el-radio-group>
      <br>
      <div>
        <div class="button-promptor">Max Core: </div><el-input v-model="chemioCalcArrays.max_core" class="chemio-property-input" type="number" @change="handlePropertyChange" />
        <!--</div>
      <div>-->
        <div class="button-promptor">Max Memory: </div><el-input v-model="chemioCalcArrays.max_memory" class="chemio-property-input" style="margin-right:0px" type="number" @change="handlePropertyChange" /><span style="margin-right:20px">GB</span>
        <!--</div>
      <div>-->
        <div class="button-promptor">Min Cell Size: </div><el-input v-model="chemioArrays.min_cell_size" class="chemio-property-input" style="margin-right:0px" type="number" @change="handlePropertyChange" /><span style="margin-right:20px">A</span>
      </div>
      <span style="margin-left:50px;">Type: </span><el-select v-model="writeFormat" style="margin-left:0px;border:1px solid black" @change="handlePropertyChange">
        <el-option v-for="type in chemioOutTypes" :key="type" :label="type.toUpperCase()" :value="type" />
      </el-select>
    </el-form-item>
  </el-form>
</template>

<script>
import axios from 'axios'

const defaultChemioOutTypes = ['json', 'gaussian', 'adf', 'cp2k', 'INCAR', 'POSCAR', 'POTCAR', 'orca', 'xyz', 'nwchem', 'gromacs', 'abinit']
const defaultShowRadioTypes = ['gaussian', 'adf', 'POSCAR', 'POTCAR', 'INCAR', 'cp2k', 'orca', 'nwchem']
const defaultWriteFormat = 'gaussian'
const defaultFormMessage = 'Drop quantum chemical file here or'

export default {
  props: {
    beforeUpload: Function, // eslint-disable-line
    onSuccess: Function// eslint-disable-line
  },
  data() {
    return {
      loading: false,
      chemioOutTypes: defaultChemioOutTypes,
      showRadioTypes: defaultShowRadioTypes,
      rawFile: null,
      rawFileTicket: null,
      readIndex: ':',
      writeFormat: defaultWriteFormat,
      formMessage: defaultFormMessage,
      chemioArrays: {
        min_cell_size: 21
      },
      chemioCalcArrays: {
        max_core: 4,
        max_memory: 4
      }
    }
  },
  methods: {
    handlePropertyChange(e) {
      // console.log('format:', this.writeFormat)
      this.getChemioParseResult()
    },
    generateData(results) {
      // this.chemioResult.results = results
      this.onSuccess && this.onSuccess(results)
    },
    handleDrop(e) {
      e.stopPropagation()
      e.preventDefault()
      if (this.loading) return
      const files = e.dataTransfer.files
      if (files.length !== 1) {
        this.$message.error('Only support uploading one file!')
        return
      }
      const rawFile = files[0] // only use files[0]
      this.parseNewFile(rawFile)
      e.stopPropagation()
      e.preventDefault()
    },
    handleClick(e) {
      const files = e.target.files
      const rawFile = files[0] // only use files[0]
      this.parseNewFile(rawFile)
    },
    parseNewFile(rawFile) {
      if (!rawFile) return
      this.rawFile = rawFile
      this.setFormMessage(rawFile.name)
      this.$message({
        'message': 'Parsing file: ' + this.rawFile.name + '. Please wait...',
        'type': ''
      })
      this.getChemioParseResult(true)
    },
    setFormMessage(message, containFile = true) {
      this.formMessage = message
      console.log(this.formMessage)
      if (containFile) {
        // this.formMessagerStyle['color'] = 'blue'
        // this.dropStyle['background'] = 'repeating-linear-gradient(45deg,#FFFFFF,#C0C4CC 9rem,transparent 0,transparent 4rem);'
      }
    },
    handleDragover(e) {
      e.stopPropagation()
      e.preventDefault()
      e.dataTransfer.dropEffect = 'copy'
    },
    handleUpload() {
      this.$refs['chemio-upload-input'].click()
    },
    chemioResolver(response, isNewFile = false) {
      // console.log(response)
      // record file ticket for faster changing
      if (response.headers.fileTicket != null) {
        this.fileTicket = response.header.fileTicket
      }
      var res = response.data
      // stringfy result
      var success = res.success
      var message = res.message
      var result = res.data
      if (!success) {
        this.$message.error(message)
      } else {
        this.generateData(result)
        if (isNewFile) {
          this.$message.success('Prasing file:' + this.rawFile.name + 'successfully!')
        }
      }
    },
    chemioErrorHandler(e) {
      console.log(e)
      this.$message.error('File ' + this.rawFile.name + ' Error, Please check your file')
      // this.rawFile = null
      // this.setFormMessage(defaultFormMessage, false)
    },
    getChemioParseResult(isNewFile = false) {
      var protocal = document.location.protocol
      var host = 'io.' + document.location.host
      var path = '/convert'
      var url = protocal + '//' + host + path
      if (process.env.NODE_ENV === 'development') {
        url = document.location.protocol + '//io.autochemistry.com/convert'
        host = 'http://localhost:5001'
        url = host + '/convert'
      }
      var formData = new FormData()
      if (!this.rawFile) {
        return
      }
      if (this.fileTicket != null) {
        formData.append('read_file_ticket', this.rawFileTicket)
      } else {
        formData.append('read_file', this.rawFile)
      }
      formData.append('read_index', this.readIndex)
      formData.append('write_format', this.writeFormat)
      formData.append('data', JSON.stringify(this.chemioArrays))
      formData.append('calc_data', JSON.stringify(this.chemioCalcArrays))
      var config = {
        'header': {
          'Content-Type': 'multipart/form-data',
          'Access-Control-Allow-Origin': 'true'
        }
      }
      // console.log(formData, config)
      const resolver = this.chemioResolver
      const errorHandler = this.chemioErrorHandler
      axios.post(url, formData, config)
        .then(function(response) {
          resolver(response, isNewFile)
        })
        .catch(e => {
          errorHandler(e)
        })
    }
  }
}
</script>

<style scoped>
.chemio-upload-input{
  display: none;
  z-index: -9999;
}
.drop{
  border: 2px dashed #bbb;
  max-width: 600px;
  height: 160px;
  line-height: 160px;
  margin: 0 auto;
  font-size: 24px;
  border-radius: 5px;
  text-align: center;
  color: #bbb;
  position: relative;
}
.el-input__inner{
  color: #141517;
  opacity: 1,
}
input:disabled,textarea:disabled{
    opacity: 1;
    -webkit-text-fill-color: red;
}
.to-type-el-form-item{
  margin:auto;
  margin-top:20px;
  max-width:1000px;
}
.to-type-el-radio{
  height: 38px;
  max-width: 80px;
  line-height: 38px;
  margin-bottom: 20px;
  vertical-align: middle;
}
.chemio-property-input{
  width:70px;
  padding:0;
  margin-right:20px;
}
input.chemio-property-input{
  padding-right:0;
  display: inline;
}
.button-promptor{
  margin-left:30px;
  width:200px;
  position: relative;
  display: inline;
}
</style>
