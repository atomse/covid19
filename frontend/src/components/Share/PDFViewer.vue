<template>
  <div v-show="fileType === 'pdf'" class="pdf">
    <p class="arrow">
      // 上一页
      <span class="turn" :class="{grey: currentPage==1}" @click="changePdfPage(0)">Preview</span>
      {{ currentPage }} / {{ pageCount }}
      // 下一页
      <span :class="{grey: currentPage==pageCount}" class="turn" @click="changePdfPage(1)">Next</span>
    </p>
    // 自己引入就可以使用,这里我的需求是做了分页功能,如果不需要分页功能,只要pdfsrc就可以了
    <pdf :pdfsrc="pdfsrc" :page="currentPage" @num-pages="pageCount=$event" @page-loaded="currentPage=$event" @loaded="loadPdfHandler" />
  </div>
</template>

<script>
import pdf from 'vue-pdf'
export default {
  components: {
    pdf
  },
  props: {
    src: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      currentPage: 0, // pdf文件页码
      pageCount: 0, // pdf文件总页数
      fileType: 'pdf', // 文件类型
      pdfsrc: pdf.createLoadingTask(this.src)
    }
  },
  // created: function() {
  //   // 有时PDF文件地址会出现跨域的情况,这里最好处理一下
  //   this.pdfsrc = pdf.createLoadingTask(this.pdfsrc)
  // },
  method: {
    // 改变PDF页码,val传过来区分上一页下一页的值,0上一页,1下一页
    changePdfPage(val) {
      // console.log(val)
      if (val === 0 && this.currentPage > 1) {
        this.currentPage--
      }
      if (val === 1 && this.currentPage < this.pageCount) {
        this.currentPage++
      }
      // console.log(this.currentPage)
    },
    // pdf加载时
    loadPdfHandler(e) {
      this.currentPage = 1 // 加载的时候先加载第一页
    }

  }
}

</script>
